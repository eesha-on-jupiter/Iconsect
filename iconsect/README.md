# Iconsect

> Layered icon generation for Grasshopper plugins: pick a look, render every icon, embed them in
> `Resources.resx`.

Iconsect is a Claude Code plugin that turns an `icons.json` into a consistent set of Grasshopper
component icons: a background shape (solid or gradient), an optional watermark glyph, and a
foreground glyph from [Iconify](https://iconify.design), rendered at 24×24 for components and 16×16
for the ribbon icon, then injected into `Resources.resx` and `Resources.Designer.cs`.

**You pick the style. Iconsect renders and embeds.**

---

## Install

```
/plugin marketplace add eesha-on-jupiter/Iconsect
/plugin install iconsect
```

Then confirm the MCP server is connected:

```
/mcp
# expect: iconsect → sect-icon-generator  (connected)
```

> **Requirements:** Python ≥ 3.10 with `mcp[cli] httpx resvg-py pillow`, installed into the Python
> that Claude Code launches MCP servers with:
> `pip install -r mcps/sect-icon-generator/requirements.txt`
>
> Rendering works on any OS. **Embedding into `Resources.resx` is Windows-only**: it shells out to
> PowerShell's `ResXResourceWriter`.

To skip the per-call approval prompts, allow the server in your project's
`.claude/settings.local.json`:

```json
{ "permissions": { "allow": ["mcp__plugin_iconsect_sect-icon-generator__*"] } }
```

---

## Commands

| Command | What it does |
|---|---|
| `/icon-init` | Create `icons.json`: asks for the plugin name and prefix, previews the options, writes the chosen style |
| `/icon-preview [glyph]` | Render every background shape in each fill style and pick one |
| `/icon-gen [component]` | Render icons from `icons.json` and embed them, for one component or all |
| `/icon-embed [component]` | Embed already-rendered PNGs (incl. hand-made ones) into `Resources.resx` |

A typical first run: `/icon-init` → fill in each component's `fg_iconify_id` → `/icon-gen`.

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

Shapes are **artwork, not code**. Each is an SVG in `mcps/sect-icon-generator/backgrounds/`, addressed
by its filename slug: `bg-icon_Arrow-Square.svg` becomes `"type": "arrow-square"`. Thirty ship with
the plugin.

To add one:

1. Draw it in a **square viewBox** with unfilled geometry. It gets rasterised to a silhouette and
   tinted, so raster `<image>` elements are rejected.
2. Add a `#ed1c24` rect beside the shape marking where the foreground glyph should sit. That rect is
   stripped before rendering and read as the glyph's placement, so **where the icon lands is a
   drawing decision, not a setting**. Boxes may be non-square.
3. Save it as `bg-icon_<Name>.svg` in `backgrounds/`.

It is available immediately, with no code change. Run `/icon-preview` to see it.

A few shapes (`trapezoid`, `saddle-shape`, `database`, `l-border`, `quarter-circle-right`,
`right-triangle`, `half-circle`) put the glyph box partly outside the artwork on purpose; the shape
reads as a base under the glyph rather than a container. Use a dark foreground with these; a white
glyph vanishes where it leaves the shape.

---

## Relationship to PleaseREST

Iconsect is a standalone product. Its icon engine started as the icon layer of
[PleaseREST](https://github.com/eesha-on-jupiter/PleaseREST), and the two are kept at **feature parity**:
whatever one can render, so can the other, but each is named for itself: Iconsect uses the
`sect-` prefix (`sect-icon-generator`, `sect-icons`) where PleaseREST uses `pr-`. The skill and
commands are Iconsect's own and carry no pipeline, phases, or session state.

**Keeping parity.** `server.py`, `icons.template.json` and `backgrounds/` are functionally identical
in both repos and differ only in the server's own name (its docstring header and the `FastMCP(...)`
argument). A change to icon rendering belongs in both: apply it, then diff the two files and confirm
those two lines are the only difference. Both test suites must pass afterwards.

**Author:** Eesha Jain · **Version:** 0.1.0
