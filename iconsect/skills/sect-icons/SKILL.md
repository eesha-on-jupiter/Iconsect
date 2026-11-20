---
name: sect-icons
description: Make icons for a Grasshopper plugin. Shows the background options and gets an explicit pick, authors icons.json, then renders every icon and embeds it into Resources.resx via the sect-icon-generator MCP. Load when creating, restyling, re-rendering or embedding Grasshopper component icons.
---

# Skill: Icon authoring

Owns a Grasshopper plugin's icon set — from picking a look, through `icons.json`, to rendered PNGs
embedded in `Resources.resx`.

The icon source is **Iconify** (`iconify.design`) — every glyph is referenced by its Iconify ID,
`prefix:name` (e.g. `mdi:magnify`, `ph:plus-bold`, `lucide:table`). Background **shapes** are
different: they are SVG artwork shipped with the MCP, addressed by filename slug.

---

## Step 1 — show the options and let the user pick (mandatory)

**Never choose a background for the user.** Before writing a single line of `icons.json`:

```
preview_backgrounds(output_dir="Icons/_preview", fg_iconify_id="<a glyph from this plugin's domain>",
                    styles="gradient,solid,none")
```

That renders every shape in `backgrounds/` in each fill style through the real render path, writes
`Icons/_preview/contact-sheet.png` (one labelled grid) plus a PNG per tile, and returns a catalog
with paste-ready snippets. Show it, then ask for a **fill style** and a **shape** — and optionally a
watermark and colours.

The template's blue gradient rounded-square is a **placeholder that keeps the file valid, not a
house style**. A plugin whose icons all sit on a gradient blob nobody asked for is the failure this
step prevents. `/icon-preview` is this step as a standalone command.

### The four background treatments

Exactly what the renderer supports — quote these verbatim when offering the choice:

```json
// gradient — two-colour linear gradient behind the glyph
"background": { "shape": { "type": "<slug>", "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } } }

// solid — one flat colour behind the glyph
"background": { "shape": { "type": "<slug>", "fill": "#2D6CDF" } }

// none / transparent — no background at all; the glyph alone, filling the canvas
"background": {}

// watermark — optional extra layer, on top of any shape, under the foreground glyph
"background": { "shape": { "type": "<slug>", "fill": "#2D6CDF" },
                "icon":  { "iconify_id": "prefix:name", "color": "#FFFFFF", "opacity": 0.45 } }
```

## Step 2 — scaffold `icons.json`

Copy `mcps/sect-icon-generator/icons.template.json` to the project root as `icons.json` and delete
every `_`-prefixed documentation key. Write the **user's chosen style** into `defaults` (and
`plugin_icon`), replacing the placeholder. Then add one entry per component, grouped by subcategory,
each with a **suggested** `fg_iconify_id` following the glyph rules below — the user edits these.

`icons.json` lives at the project root, and **every MCP call takes its path as `config_path`**.
There is no default config: omitting `config_path` raises rather than silently rendering another
project's icons.

## Step 3 — let the user specify

Present `icons.json` and ask the user to confirm or change each icon. The background is built from
**independent optional layers** — any combination:
- the **foreground** Iconify glyph (`fg_iconify_id`) — itself optional
- a background **`shape`** (solid or gradient) — optional
- a background **`icon`** (an Iconify glyph behind the foreground) — optional
- **no background** — omit both, or set `"background": {}`
- colours / gradients for the shape, the bg icon, and the foreground

Wait for approval before rendering. The user may say "I'll pick the background icons" — let them
fill `icon.iconify_id` per subcategory.

## Step 4 — render and embed

Per component: `generate_icon(component_name, config_path)` → `add_to_resources(component_name, config_path)`.
Then once, as a separate final step, the whole-plugin icon:
`generate_plugin_icon(config_path)` → `add_to_resources("[PluginName]Logo", config_path)`.

- Component icons render at **24×24** px → resource `[XX]_[ComponentName]`, referenced in component
  code as `Properties.Resources.[XX]_[ComponentName]`.
- The plugin / ribbon category icon renders at **16×16** px → resource `[XX]_[PluginName]Logo`
  (`[XX]` = `plugin_prefix`, e.g. MiroConnect → `MC_MiroConnectLogo`). Pass `"[PluginName]Logo"` to
  `add_to_resources` — it prepends the prefix.

**Resource-name convention.** Every embedded icon is `[plugin_prefix]_[Name]`, reachable from C# as
`Properties.Resources.[plugin_prefix]_[Name]` once `Resources.Designer.cs` is in the
`[PluginName].Properties` namespace. Wire the 16×16 logo as the ribbon category icon yourself, in
your `GH_AssemblyInfo` / `GH_AssemblyPriority` class:

```csharp
Instances.ComponentServer.AddCategoryIcon("[TabName]", Properties.Resources.[XX]_[PluginName]Logo);
```

and expose a component's icon with `protected override Bitmap Icon => Properties.Resources.[XX]_[ComponentName];`

**`add_to_resources` is Windows-only.** It shells out to PowerShell's `ResXResourceWriter`; on macOS
it returns a clear error. The PNGs are still written, so rendering works anywhere — only the resx
embed needs Windows. A binary resource in a `net48` project also needs
`<GenerateResourceUsePreserializedResources>true</GenerateResourceUsePreserializedResources>` and a
`System.Resources.Extensions` package reference, or the build fails with MSB3823.

---

## icons.json schema

```json
{
  "plugin_name": "[PluginName]",
  "plugin_prefix": "[XX]",
  "resources_path": "Icons",
  "resx_path": "Properties/Resources.resx",

  "defaults": {
    "size": 24,
    "fg_color": "#FFFFFF",
    "background": {
      "shape": {                                         // OPTIONAL — omit for no shape
        "type": "rounded-square",                        // any slug; preview_backgrounds() shows them
        "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 }
        // or solid instead of gradient:  "fill": "#444444"
      }
      // "icon": { ... }  also OPTIONAL — see subcategory example
    }
  },

  "plugin_icon": {
    "size": 16,
    "fg_iconify_id": "[prefix:name]",
    "fg_color": "#FFFFFF",
    "background": { "shape": { "type": "rounded-square",
                              "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } } }
  },

  "subcategories": {
    "[Subcategory]": {
      "background": {
        "shape": { "type": "rounded-square", "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } },
        "icon":  { "iconify_id": "[prefix:name]", "color": "#FFFFFF", "opacity": 0.45 }  // bg glyph (solid silhouette, blended)
      },
      "fg_color": "#FFFFFF"
    }
  },

  "components": [
    { "name": "FindBoard", "subcategory": "[Subcategory]",
      "fg_iconify_id": "mdi:magnify" },

    { "name": "GlyphOnly", "subcategory": "[Subcategory]",
      "fg_iconify_id": "mdi:eye",
      "background": {} },                                 // no background — glyph alone

    { "name": "ShapeOnly", "subcategory": "[Subcategory]",
      "fg_iconify_id": "mdi:plus",
      "background": { "shape": { "type": "circle", "fill": "#2D6CDF" } },
      "fg": { "from": "#FFFFFF", "to": "#BBD0FF", "angle": 90 } },  // optional fg gradient

    { "name": "HandDrawn", "subcategory": "[Subcategory]",
      "custom": true }                                     // hand-made Icons/[XX]_HandDrawn.png — generator skips it
  ]
}
```

**`"custom": true`** — the icon is hand-made. Drop `Icons/[XX]_[Name].png` (24×24) in yourself;
`generate_icon` returns a skip message and never overwrites it, `add_to_resources` still embeds it.
Use this for any icon a batch re-render must leave alone.

**Resolution order:** `defaults` < `subcategories[sub]` < `components[i]`. Anything omitted inherits;
set `"background": {}` on a component to override down to no background (an explicit empty block
clears the inherited layers; only an *omitted* key inherits). Inside `background`, `"icon": {}` drops
an inherited bg icon while keeping your own `shape`. A component-level solid `fg_color` overrides an
inherited `fg` gradient.

**Background = optional layers (mix freely):**
- `shape` — a background SVG from `backgrounds/`; `fill` for solid **or** `gradient` for a linear
  gradient. Omit for no shape.
  - `align` — optional `{ fit, anchor }` to size and position the shape within the canvas. Default
    fits the whole canvas, centred.
- `icon` — an Iconify glyph (`iconify_id`) drawn behind the foreground as a **solid silhouette**
  (interior holes of outline icons are filled in automatically). Sits on top of `shape` if both are
  present (**foreground glyph on a background icon on a shape**). Omit for no bg icon.
  - `color` — fill colour (default `"#FFFFFF"`). Use a light colour; it blends with the shape below
    via `opacity`.
  - `opacity` — `0..1` (default `0.45`). Toward 1.0 for a prominent bg icon, toward 0 for a faint
    watermark.
  - `gradient` — `{ "from": hex, "to": hex, "angle": deg }` instead of `color` for a gradient fill.
  - `align` — optional `{ fit, anchor }`, same as `shape.align`, to size/position it independently.
- both omitted (or `background: {}`) → **no background**, foreground glyph alone.

**Foreground:** a hex (`fg_color`) or a gradient (`fg`) — and the glyph itself is optional. Glyphs
are silhouette-tinted, so white / light / gradient foregrounds all render correctly.

**Shapes** — values for `shape.type`. Every shape is an SVG in the MCP's `backgrounds/` folder;
**call `preview_backgrounds()` to see them rendered, or `list_background_shapes()` for the names
alone** rather than trusting this list. The slug is the filename minus the `bg-icon_` prefix,
lowercased (`bg-icon_Arrow-Square.svg` → `arrow-square`). As shipped (30):

`1-arch`, `3-arches`, `arrow-square`, `block`, `bookmark`, `bubble`, `canvas`, `chevron`, `circle`,
`cloud`, `copy`, `cut-square`, `database`, `diamond`, `document`, `ellipse`, `file`, `flower`,
`half-circle`, `hexagon`, `l-border`, `octagon`, `pentagon`, `quarter-circle-right`,
`right-triangle`, `rounded-rectangle`, `rounded-square`, `saddle-shape`, `square`, `trapezoid`.

**Adding a shape** — draw it in a square viewBox with unfilled geometry, add its glyph box (below),
save as `bg-icon_<Name>.svg` in `backgrounds/`. It works immediately, with no code change. Raster
`<image>` elements are rejected, since a bitmap can't be tinted.

**Glyph placement is drawn, not computed.** Each background SVG carries a `#ed1c24` rect marking
where the foreground glyph goes, authored in Illustrator next to the shape. The renderer strips that
rect before drawing (it never appears in output) and uses it as the glyph area. So placement is a
design decision living in the artwork — there is nothing to tune in `icons.json` for it, and adding a
shape means drawing its box, not writing config. Resolution is by *fill colour*, not Illustrator's
`cls-N` class names, which are unstable across re-exports.

- Boxes may be **non-square** (Document's is wider than tall). A square glyph fits the shorter side,
  centred in the box.
- **Background icon, no shape** (just `background.icon`) → the bg icon fills the canvas and the
  foreground glyph sits at 85%, centred.
- **No background at all** (`background: {}` or omitted) → the glyph **fills the canvas edge to
  edge**: it is trimmed to its own ink first, then scaled until its longer side reaches the canvas,
  aspect preserved. Iconify glyphs carry padding inside their viewBox — `mdi:plus` draws in only
  ~58% of it — so without the trim a glyph-only icon would render noticeably small.

**Some shapes need a dark foreground.** `trapezoid`, `saddle-shape`, `database`, `l-border`,
`quarter-circle-right`, `right-triangle` and `half-circle` place the glyph box *partly outside* the
artwork on purpose — the shape reads as a base or accent beneath the glyph rather than a container.
A white glyph on these disappears where it leaves the shape. Pick a dark `fg_color` for any
subcategory using them, or choose a container shape (`square`, `circle`, `hexagon`, `octagon`,
`rounded-square`, `bubble`, `flower`, `diamond`, …) if you want white-on-colour.

Override the foreground per component / subcategory / defaults with an optional `glyph` block:
```json
"glyph": { "fit": 0.7, "anchor": [0.5, 0.5] }
```
`fit` = glyph's longest side as a fraction of the canvas; `anchor` = `[ax, ay]` in 0..1 (0.5,0.5 =
centred, higher = toward right/bottom). Everything stays optional.

**Every layer is independently alignable** — foreground glyph, background shape, and background icon
each take their own `{ fit, anchor }` block:
```json
"background": {
  "shape": { "type": "circle", "fill": "#2D6CDF", "align": { "fit": 0.9, "anchor": [0.5, 0.5] } },
  "icon":  { "iconify_id": "mdi:star", "align": { "fit": 0.6, "anchor": [0.8, 0.2] } }
},
"glyph": { "fit": 0.7, "anchor": [0.3, 0.6] }
```
All three default to the full-bleed / shape-aware behaviour, so `align` is only needed when you want
to depart from it.

---

## Glyph selection rules (suggested defaults)
- GET / read → outline glyph (e.g. `mdi:magnify`, `ph:eye`)
- POST / create → filled glyph with a plus (e.g. `mdi:plus-circle`)
- PATCH / update → a pencil / refresh (e.g. `mdi:pencil`)
- DELETE → a minus / trash (e.g. `mdi:trash-can`)
- JSON builder / aggregator → structural glyph (e.g. `lucide:table`, `ph:brackets-curly`)
- Preset (`GH_ValueList`) → list / menu glyph
- Auth → lock / key glyph
- Utilities → wrench / tool glyph

## Design quality bar
- One consistent background treatment per subcategory; the foreground glyph communicates function
  at 24px
- Pick a per-plugin palette referencing the platform's identity, adapted for a dense technical
  Grasshopper context (high contrast, modern). Gradients should be subtle (two close hues), not garish
- When unsure, **show the preview and ask** — do not fall back to a gradient blob. A useful prompt is
  "gradient reads as branded, solid reads as flat and modern, none reads as a plain toolbar glyph"
- There is no drop-shadow layer — depth comes from the background shape/gradient choice, not a shadow

## Rules
- **A background is never chosen for the user.** Run `preview_backgrounds` and get an explicit
  fill-style + shape decision before `icons.json` is written
- `icons.json` lives at the project root; every MCP call passes its path as `config_path`
- `icons.json` is re-read from disk on every call, so edits are always picked up
- Component icons 24×24, plugin/category icon 16×16
- Every icon is user-approved before rendering; after a batch render, show the files in `Icons/` for
  a quick glance ("ok" / name any to redo)
- `"custom": true` icons are never rendered or overwritten — but they still need embedding

---

## Parity with PleaseREST

The icon engine is shared with **PleaseREST** (https://github.com/eesha-on-jupiter/PleaseREST), a
separate product whose equivalents are `pr-icon-generator` and the `pr-icons` skill. The two are kept
at **feature parity**: `server.py`, `icons.template.json` and `backgrounds/` are functionally
identical and differ only in naming: the server's own name (its docstring header and the
`FastMCP(...)` argument) and the skill names mentioned in comments and template notes. Rendering behaviour, the schema, and the four background treatments must stay the same in
both. Entry points do not: Iconsect uses its own four commands, PleaseREST drives icons through its
pipeline.

**Changing icon rendering?** Apply it in both repos, diff the two `server.py` files to confirm only
the naming lines differ, and run both test suites.
