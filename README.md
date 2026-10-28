# Iconsect

> *Layered icon generation for Grasshopper plugins: pick a look, render every icon, embed them in `Resources.resx`.*

Iconsect is a Claude Code plugin that turns an `icons.json` into a consistent set of Grasshopper
component icons. Each icon is a background shape (solid or gradient), an optional watermark glyph
and a foreground glyph from [Iconify](https://iconify.design), rendered at 24×24 for components and
16×16 for the ribbon, then injected into `Resources.resx` and `Resources.Designer.cs`.

**You pick the style. Iconsect renders and embeds.**

`4 commands · 1 skill · 1 MCP server · 30 background shapes · 252 tests`

---

## Install

```
/plugin marketplace add eesha-on-jupiter/Iconsect
/plugin install iconsect
```

Confirm the MCP server came up:

```
/mcp
# expect: iconsect → sect-icon-generator  (connected)
```

**Local development:** point Claude Code at the plugin folder instead:

```
claude --plugin-dir /path/to/Iconsect/iconsect
```

### Requirements

| Needed for | What |
|---|---|
| The MCP server | **Python ≥ 3.10**, reachable as `python` on PATH, with `mcp[cli] httpx resvg-py pillow` (`pip install -r iconsect/mcps/sect-icon-generator/requirements.txt`) |
| Embedding into `Resources.resx` | **Windows**: it shells out to PowerShell's `ResXResourceWriter`. Rendering works on any OS |

> The server is launched as literally `python`. On macOS/Linux that is often only `python3`, and on
> Windows it can resolve to the Microsoft Store stub. Either shows up as the server "not connected".

To skip the per-call approval prompts, allow the server in your project's
`.claude/settings.local.json`:

```json
{ "permissions": { "allow": ["mcp__plugin_iconsect_sect-icon-generator__*"] } }
```

---

## Quick start

```
/icon-init
```

It asks for the plugin name and icon prefix, renders the background options so you can see them,
and writes `icons.json` with the style you pick. Fill in each component's `fg_iconify_id`, then:

```
/icon-gen
```

---

## Commands

| Command | What it does |
|---|---|
| `/icon-init` | Create `icons.json`: asks for the plugin name and prefix, previews the options, writes the chosen style |
| `/icon-preview [glyph]` | Render every background shape in each fill style and pick one |
| `/icon-gen [component]` | Render icons from `icons.json` and embed them, for one component or all |
| `/icon-embed [component]` | Embed already-rendered PNGs (including hand-made ones) into `Resources.resx` |

---

## Skill

| Skill | Covers |
|---|---|
| `sect-icons` | Shows the background options, gets an explicit pick, authors `icons.json`, renders and embeds every icon |

---

## MCP server

### `sect-icon-generator`: renders and embeds the icons

| Tool | |
|---|---|
| `preview_backgrounds(output_dir, fg_iconify_id?, styles?, shapes?, size?, ...)` | Render every background shape in every fill style to a contact sheet, so the options can be **seen** before anything is chosen |
| `list_background_shapes()` | The shapes currently available |
| `generate_icon(component_name, config_path?, subcategory?, iconify_id?)` | One 24×24 component icon |
| `generate_plugin_icon(config_path?)` | The 16×16 ribbon icon |
| `add_to_resources(component_name, config_path?)` | Embed a PNG into `Resources.resx` + `Resources.Designer.cs` (Windows only) |

---

## The three background styles

A background is never chosen for you. `/icon-preview` renders all of them so you can see the real
thing before picking:

```json
// gradient: two-colour linear gradient behind the glyph
"background": { "shape": { "type": "hexagon", "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } } }

// solid: one flat colour behind the glyph
"background": { "shape": { "type": "hexagon", "fill": "#2D6CDF" } }

// none: no background at all; the glyph alone, filling the canvas
"background": {}
```

Plus an optional **watermark** layer on top of any shape, under the foreground glyph:

```json
"background": { "shape": { "type": "hexagon", "fill": "#2D6CDF" },
                "icon":  { "iconify_id": "mdi:cloud", "color": "#FFFFFF", "opacity": 0.45 } }
```

Styles resolve `defaults` < `subcategories[sub]` < `components[i]`, so a house style set once is
inherited by every icon, and any single icon can override it. Set `"custom": true` on a component to
protect a hand-made PNG; the generator skips it and never overwrites it.

---

## Adding a background shape

Shapes are **artwork, not code**. Each is an SVG in `iconsect/mcps/sect-icon-generator/backgrounds/`,
addressed by its filename slug: `bg-icon_Arrow-Square.svg` becomes `"type": "arrow-square"`. Thirty
ship with the plugin.

To add one:

1. Draw it in a **square viewBox** with unfilled geometry. It gets rasterised to a silhouette and
   tinted, so raster `<image>` elements are rejected.
2. Add a `#ed1c24` rect beside the shape marking where the foreground glyph should sit. That rect is
   stripped before rendering and read as the glyph's placement, so **where the icon lands is a
   drawing decision, not a setting**. Boxes may be non-square.
3. Save it as `bg-icon_<Name>.svg` in `backgrounds/`.

It is available immediately, with no code change. Run `/icon-preview` to see it.

---

## Relationship to PleaseREST

Iconsect is a standalone product. Its icon engine started as the icon layer of
[PleaseREST](https://github.com/eesha-on-jupiter/PleaseREST), and the two are kept at **feature
parity**: whatever one can render, so can the other. Iconsect uses the `sect-` prefix
(`sect-icon-generator`, `sect-icons`) where PleaseREST uses `pr-`, and its skill and commands carry
no pipeline, phases or session state.

---

## Repo layout

```
Iconsect/
├── .claude-plugin/marketplace.json   the marketplace manifest, read by /plugin marketplace add
├── iconsect/                         the plugin itself
│   ├── .claude-plugin/plugin.json    plugin manifest (name, version, MCP server)
│   ├── commands/                     4 slash commands
│   ├── skills/sect-icons/            the icon skill
│   ├── mcps/sect-icon-generator/     the MCP server (Python), template and 30 background SVGs
│   └── README.md                     the plugin's own readme
└── tests/                            252 tests for the MCP server
```

**Tests**

```
cd tests
pip install -r requirements.txt
pytest
```

---

## License

MIT. Copyright (c) 2026 Eesha Jain. See [LICENSE](LICENSE).
