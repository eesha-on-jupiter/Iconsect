# The MCP server

One server ships with the plugin and loads from `plugin.json`:

```json
"mcpServers": {
  "sect-icon-generator": { "command": "python", "args": ["${CLAUDE_PLUGIN_ROOT}/mcps/sect-icon-generator/server.py"] }
}
```

> **Dependencies:** Python ≥ 3.10 with `mcp[cli]`, `httpx`, `resvg-py` and `pillow`, installed into
> the Python that Claude Code launches MCP servers with:
> `pip install -r mcps/sect-icon-generator/requirements.txt`

Verify it is connected with `/mcp`. If it is not, see [troubleshooting](troubleshooting.md).

The commands call these tools for you. You rarely call one directly.

---

## `sect-icon-generator`

| Tool | Purpose |
|---|---|
| `preview_backgrounds(output_dir, fg_iconify_id?, styles?, shapes?, size?, fill?, gradient_from?, gradient_to?, gradient_angle?, fg_color?, bg_icon_iconify_id?)` | Render every shape in each fill style so the options can be **seen** before choosing |
| `list_background_shapes()` | The shape slugs currently available |
| `generate_icon(component_name, config_path, subcategory?, iconify_id?)` | One 24×24 component icon |
| `generate_plugin_icon(config_path)` | The 16×16 ribbon icon |
| `add_to_resources(component_name, config_path)` | Embed a PNG into `Resources.resx` and `Resources.Designer.cs` |

`config_path` is the path to your plugin's `icons.json`. It is required on every call that takes it.
There is no default config, so a missing path raises instead of rendering another project's icons.

### `preview_backgrounds`

Needs no `icons.json`. It takes its colours as arguments, so it works before a plugin has any config.

| Argument | Default | Meaning |
|---|---|---|
| `output_dir` | required | Where the PNGs and the contact sheet are written. Created if needed |
| `fg_iconify_id` | `mdi:star` | The sample foreground glyph |
| `styles` | `gradient,solid,none` | Any comma-separated subset |
| `shapes` | every shape | Comma-separated slugs, to compare a few |
| `size` | `128` | Tile size in pixels. Previews are larger than the real 24px icons |
| `fill` | `#2D6CDF` | Colour for the `solid` style |
| `gradient_from`, `gradient_to`, `gradient_angle` | `#2D6CDF`, `#1B3A8B`, `135` | The `gradient` style's ramp |
| `fg_color` | `#FFFFFF` | The sample glyph's colour |
| `bg_icon_iconify_id` | none | A watermark glyph, shown on every shape |

It writes `preview_<slug>_<style>.png` per tile, one `preview_none.png` for the no-background
option, and a labelled `contact-sheet.png`. It returns a catalog with paste-ready `icons.json`
snippets.

### `generate_icon` and `generate_plugin_icon`

`generate_icon` writes `[resources_path]/[XX]_[ComponentName].png`. `generate_plugin_icon` reads the
`plugin_icon` block and writes `[XX]_[PluginName]Logo.png`.

A component marked `"custom": true` is skipped with a message. Its PNG is never overwritten.

### `add_to_resources`

Pass a component name such as `FindBoard`, or `[PluginName]Logo` for the ribbon icon. The prefix is
added for you.

- **Idempotent.** An existing resx key is replaced, not duplicated. A `Resources.Designer.cs` that
  already declares the property is left alone.
- **Windows-only.** It shells out to PowerShell's `ResXResourceWriter`. On macOS and Linux it
  returns a clear error and the PNG is left in place.

---

## How rendering works

- Layers are composed in order: background shape, then watermark, then foreground glyph. Each is
  optional.
- Everything is drawn at 4× and downscaled with LANCZOS, which keeps edges clean at 24px.
- Glyphs are fetched from Iconify as SVG, reduced to a silhouette and tinted. That is why any
  colour or gradient works, on any glyph.
- The foreground glyph is trimmed to its own ink before placing, so it fills its target area: the
  full canvas with no background, or the glyph box drawn into the shape's artwork.
- There is no drop-shadow layer. Depth comes from the shape and gradient you choose.
- `icons.json` is re-read from disk on every call and never cached.

Rendering needs network access to `api.iconify.design` for the glyphs.
