# Iconsect: Claude Code Plugin
> *Layered icon generation for Grasshopper plugins: pick a look, render every icon, embed them in `Resources.resx`.*

## What this plugin is

Iconsect turns an `icons.json` into a consistent set of Grasshopper component icons. Each icon is a
background shape (solid or gradient), an optional watermark glyph and a foreground glyph from
Iconify, rendered at 24×24 for components and 16×16 for the ribbon, then embedded into
`Resources.resx` and `Resources.Designer.cs`.

You pick the style. Iconsect renders and embeds.

> **User docs:** [`README.md`](README.md) and the [`docs/`](docs/) folder (overview, commands,
> `icons.json` reference, MCP server, troubleshooting). This `CLAUDE.md` is the contributor
> reference. Keep both in sync when a command, the skill or a tool changes.
>
> **Shipped context:** a `CLAUDE.md` at the plugin root is *not* loaded when the plugin is
> installed. Claude Code only ships skills, commands and the MCP server. Anything a user's session
> needs to know lives in [`skills/sect-icons/SKILL.md`](skills/sect-icons/SKILL.md).

> **Versioning:** bump `.claude-plugin/plugin.json`'s `version` and add a
> [`CHANGELOG.md`](CHANGELOG.md) entry whenever a change would make an existing `icons.json` render
> differently or change what gets embedded. Doc wording and typo fixes need neither.

---

## Inventory

**Commands** (`commands/`)

- `/icon-init`: create `icons.json`; asks for name and prefix, previews, writes the chosen style
- `/icon-preview [glyph]`: render every background shape in each fill style, and pick one
- `/icon-gen [component]`: render from `icons.json` and embed, one component or all
- `/icon-embed [component]`: embed existing PNGs without rendering

**Skill** (`skills/`)

- `sect-icons`: the full icon workflow and the `icons.json` schema. Every command loads it.

**MCP server** (`mcps/sect-icon-generator/`)

- `preview_backgrounds(output_dir, ...)`: contact sheet of every shape × style; needs no config
- `list_background_shapes()`: the slugs in `backgrounds/`
- `generate_icon(component_name, config_path, subcategory?, iconify_id?)`: one 24×24 icon
- `generate_plugin_icon(config_path)`: the 16×16 ribbon icon
- `add_to_resources(component_name, config_path)`: embed into resx + Designer.cs (Windows only)

---

## Rules that must hold

- **A background is never chosen for the user.** Every path that writes `defaults.background` runs
  `preview_backgrounds` first and waits for an explicit fill style and shape.
- **`config_path` is required.** There is no default config. A missing path raises.
- **`"custom": true` icons are never rendered or overwritten.** They are still embedded.
- **Shapes are artwork.** Glyph placement comes from the `#ed1c24` rect in each SVG, resolved by
  fill colour and not by Illustrator's unstable `cls-N` class names. Never hardcode a shape list in
  code; the set is whatever is in `backgrounds/`.
- **`plugin.json` lists only `mcpServers`.** `commands/` and `skills/` are auto-discovered. Listing
  them is a schema error that loads the plugin empty and silent. Check with
  `claude plugin validate iconsect`.
- **MCP tools are plugin-namespaced:** `mcp__plugin_iconsect_sect-icon-generator__*`.

---

## Parity with PleaseREST

The icon engine is shared with [PleaseREST](https://github.com/eesha-on-jupiter/PleaseREST), whose
equivalents are `pr-icon-generator` and the `pr-icons` skill. The two are kept at feature parity.

`server.py`, `icons.template.json` and `backgrounds/` are functionally identical in both repos and
differ only in the server's own name (its docstring header and the `FastMCP(...)` argument).

**Changing icon rendering?** Apply it in both repos, diff the two `server.py` files to confirm only
the name lines differ, and run both test suites. Entry points are not shared: Iconsect has its own
four commands, PleaseREST drives icons through its pipeline.

---

## Tests

```
cd tests
pip install -r requirements.txt
pytest
```

252 tests for the MCP server, in `tests/sect-icon-generator/`. They live at the repo root, outside
the plugin folder, so they are not shipped on install.

When the count changes, update it in the repo `README.md`, this plugin's `README.md` and
`CHANGELOG.md`.
