# Troubleshooting

## The MCP server shows "not connected"

**Symptom:** `/mcp` lists `iconsect → sect-icon-generator` as failed or not connected, immediately,
on a fresh install. The commands and the skill load fine.

**Cause:** `plugin.json` launches the server with `"command": "python"`. On macOS and most Linux
distributions there is no `python` on PATH, only `python3`. On Windows a bare `python` can resolve
to the Microsoft Store stub, which exits without running anything.

**Fix:** make `python` resolve to a real Python ≥ 3.10 for the shell Claude Code launches.

- **macOS / Linux:** install via `pyenv`, `uv` or Homebrew, or add a shim:
  `ln -s "$(command -v python3)" ~/.local/bin/python` with `~/.local/bin` on PATH. A shell *alias*
  does not work, because MCP servers are launched directly and not through your interactive shell.
- **Windows:** install from python.org. If `python` opens the Microsoft Store, turn off
  **Settings → Apps → App execution aliases → python.exe / python3.exe**.

Then check the dependencies:

```
python -c "import mcp, httpx, resvg_py, PIL; print('deps ok')"
```

Missing modules: `pip install -r iconsect/mcps/sect-icon-generator/requirements.txt`.

## The MCP server shows "not loaded"

**Cause:** a settings file references the server under the bare name `mcp__sect-icon-generator__*`,
or lists it under `enabledMcpServers` / `enabledMcpjsonServers`. Those are for project `.mcp.json`
servers. Iconsect's server comes from `plugin.json`, so its tools are namespaced
`mcp__plugin_iconsect_sect-icon-generator__*`.

**Fix:** use the plugin-scoped name in any `settings.local.json`, and remove the server from any
`enabledMcpServers` list. The change takes effect in the next session.

## The plugin loads with no commands and no error

**Cause:** a manifest schema error, most often `skills` or `commands` arrays added to `plugin.json`.
Those folders are auto-discovered at the plugin root, and listing them loads the plugin empty and
silent.

**Fix:** run `claude plugin validate <path-to-iconsect>`. It names the offending key.

## An icon fails to render

**Most common cause:** a bad Iconify ID. IDs are `prefix:name`, such as `mdi:magnify`. Check the
exact ID at [iconify.design](https://iconify.design); a placeholder left as `[prefix:name]` fails
the same way. `/icon-gen` lists missing and placeholder glyphs before it starts.

**Also check:** rendering fetches each glyph from `api.iconify.design`, so it needs network access.
Behind a proxy or offline, every icon fails the same way.

## A white glyph disappears on the shape

**Cause:** `trapezoid`, `saddle-shape`, `database`, `l-border`, `quarter-circle-right`,
`right-triangle` and `half-circle` put the glyph partly outside the artwork on purpose.

**Fix:** give icons on those shapes a dark `fg_color`, or pick a container shape such as `square`,
`circle`, `hexagon`, `octagon`, `rounded-square`, `bubble`, `flower` or `diamond`.

## The icon looks bleached, with a dark border at the corners

**Cause:** a watermark (`background.icon`) fills the whole canvas by default. A near-solid glyph at
that size washes over the entire tile, except the corners it cannot reach.

**Fix:** lower its `opacity`, pick a lighter-weight glyph, or give it a small `align.fit` so it
reads as a motif.

## Embedding fails on macOS or Linux

**Cause:** `add_to_resources` is Windows-only. It shells out to PowerShell's `ResXResourceWriter`.

**Fix:** the PNGs are already written and are fine. Run `/icon-embed` on a Windows machine, or add
the PNGs to `Resources.resx` from Visual Studio.

## The net48 (Rhino 7) build fails once an icon is embedded

**Symptom:** the project builds while `Resources.resx` is empty. After the first icon is embedded,
`dotnet build -f net48` fails with `MSB3823` and `MSB3822`. `net7.0-windows` builds fine, which
hides it.

**Fix:** add both of these to the `.csproj` and rebuild:

```xml
<GenerateResourceUsePreserializedResources>true</GenerateResourceUsePreserializedResources>
<PackageReference Include="System.Resources.Extensions" Version="8.0.0" />
```

## The new icon does not show in Grasshopper

Icons are compiled into the `.gha`. Run `dotnet build`, then reload Rhino.

## The ribbon icon is missing or resolves to null

**Cause:** a name mismatch. The ribbon icon embeds as `[XX]_[PluginName]Logo`.

**Fix:** pass that exact resource to `AddCategoryIcon`, and check that `Resources.Designer.cs` is in
the `[PluginName].Properties` namespace your code references.

## Too many permission prompts

Allow the server in your project's `.claude/settings.local.json`:

```json
{ "permissions": { "allow": ["mcp__plugin_iconsect_sect-icon-generator__*"] } }
```

The file must be inside `.claude/`. One at the project root is ignored.
