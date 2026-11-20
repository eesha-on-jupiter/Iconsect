# The `icons.json` reference

`icons.json` lives at the root of your Grasshopper plugin and describes every icon. `/icon-init`
creates it. It is re-read from disk on every render, so edits are always picked up.

## A complete example

```json
{
  "plugin_name": "MiroConnect",
  "plugin_prefix": "MC",
  "resources_path": "Icons",
  "resx_path": "Properties/Resources.resx",

  "defaults": {
    "size": 24,
    "fg_color": "#FFFFFF",
    "background": {
      "shape": { "type": "rounded-square",
                 "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } }
    }
  },

  "plugin_icon": {
    "size": 16,
    "fg_iconify_id": "mdi:view-dashboard",
    "fg_color": "#FFFFFF",
    "background": { "shape": { "type": "rounded-square", "fill": "#2D6CDF" } }
  },

  "subcategories": {
    "Boards": {
      "background": {
        "shape": { "type": "hexagon", "fill": "#2D6CDF" },
        "icon":  { "iconify_id": "mdi:cloud", "color": "#FFFFFF", "opacity": 0.45 }
      }
    }
  },

  "components": [
    { "name": "FindBoard",  "subcategory": "Boards", "fg_iconify_id": "mdi:magnify" },
    { "name": "GlyphOnly",  "subcategory": "Boards", "fg_iconify_id": "mdi:eye", "background": {} },
    { "name": "HandDrawn",  "subcategory": "Boards", "custom": true }
  ]
}
```

## Top-level keys

| Key | Meaning |
|---|---|
| `plugin_name` | Used for the ribbon icon's resource name, `[XX]_[PluginName]Logo` |
| `plugin_prefix` | Prepended to every resource: `[XX]_[ComponentName]` |
| `resources_path` | Folder the PNGs are written to, relative to `icons.json` |
| `resx_path` | The `.resx` to embed into, relative to `icons.json` |
| `defaults` | The house style every icon inherits |
| `plugin_icon` | The 16×16 ribbon icon. It has its own glyph, colours and background |
| `subcategories` | Style overrides shared by every component in a subcategory |
| `components` | One entry per icon |

## Resolution order

```
defaults  <  subcategories[sub]  <  components[i]
```

Anything omitted is inherited. To remove an inherited layer, set it to an explicit empty block:

| You write | Result |
|---|---|
| `background` omitted | Inherits the background from the subcategory or defaults |
| `"background": {}` | No background at all, the glyph alone |
| `"background": { "shape": {...}, "icon": {} }` | Your own shape, with the inherited watermark dropped |

A component-level solid `fg_color` beats an inherited `fg` gradient.

## The background styles

`/icon-preview` renders all of these so you can see them before choosing.

```json
// gradient: two-colour linear gradient behind the glyph
"background": { "shape": { "type": "hexagon", "gradient": { "from": "#2D6CDF", "to": "#1B3A8B", "angle": 135 } } }

// solid: one flat colour behind the glyph
"background": { "shape": { "type": "hexagon", "fill": "#2D6CDF" } }

// none: no background at all; the glyph alone, filling the canvas
"background": {}

// watermark: an optional extra layer on top of any shape, under the foreground glyph
"background": { "shape": { "type": "hexagon", "fill": "#2D6CDF" },
                "icon":  { "iconify_id": "mdi:cloud", "color": "#FFFFFF", "opacity": 0.45 } }
```

### `background.shape`

| Key | Meaning |
|---|---|
| `type` | A shape slug. See [Shapes](#shapes) |
| `fill` | A hex colour, for a solid shape |
| `gradient` | `{ "from": hex, "to": hex, "angle": degrees }`, instead of `fill` |
| `align` | Optional `{ "fit", "anchor" }` to size and position the shape. See [Alignment](#alignment) |

### `background.icon` (the watermark)

| Key | Default | Meaning |
|---|---|---|
| `iconify_id` | | The glyph, as `prefix:name`. Drawn as a solid silhouette |
| `color` | `#FFFFFF` | Fill colour. A light colour blends best with the shape below |
| `opacity` | `0.45` | `0` to `1`. Lower is fainter |
| `gradient` | | `{ "from", "to", "angle" }`, instead of `color` |
| `align` | | Optional `{ "fit", "anchor" }` |

A watermark with no shape fills the canvas, and the foreground glyph sits at 85%, centred.

> A full-bleed, near-solid watermark washes out the whole tile rather than reading as a motif. If
> the icon looks bleached with a dark border at the corners, lower the `opacity` or give the
> watermark a small `align.fit`.

## The foreground

| Key | Meaning |
|---|---|
| `fg_iconify_id` | The glyph, as `prefix:name`, for example `mdi:magnify`, `ph:plus-bold`, `lucide:table` |
| `fg_color` | A hex colour |
| `fg` | `{ "from", "to", "angle" }`, a gradient instead of `fg_color` |
| `glyph` | Optional `{ "fit", "anchor" }` to override where the glyph sits |

Glyphs are tinted as silhouettes, so white, light and gradient foregrounds all render correctly.
Each glyph is trimmed to its own ink before placing, so Iconify's internal padding does not make an
icon render small.

## Alignment

The shape, the watermark and the foreground glyph each take their own optional block:

```json
"background": {
  "shape": { "type": "circle", "fill": "#2D6CDF", "align": { "fit": 0.9, "anchor": [0.5, 0.5] } },
  "icon":  { "iconify_id": "mdi:star", "align": { "fit": 0.6, "anchor": [0.8, 0.2] } }
},
"glyph": { "fit": 0.7, "anchor": [0.3, 0.6] }
```

- **`fit`** is the layer's longest side as a fraction of the canvas.
- **`anchor`** is `[x, y]` from `0` to `1`. `[0.5, 0.5]` is centred; higher values move right and down.

You rarely need these. By default the foreground glyph lands in the box drawn into the shape's own
artwork.

## Hand-made icons

```json
{ "name": "HandDrawn", "subcategory": "Boards", "custom": true }
```

Drop `Icons/[XX]_HandDrawn.png` (24×24) in yourself. `/icon-gen` skips it and never overwrites it.
Run `/icon-embed` to embed it.

## Shapes

Thirty ship with the plugin. `/icon-preview` shows them rendered.

`1-arch`, `3-arches`, `arrow-square`, `block`, `bookmark`, `bubble`, `canvas`, `chevron`, `circle`,
`cloud`, `copy`, `cut-square`, `database`, `diamond`, `document`, `ellipse`, `file`, `flower`,
`half-circle`, `hexagon`, `l-border`, `octagon`, `pentagon`, `quarter-circle-right`,
`right-triangle`, `rounded-rectangle`, `rounded-square`, `saddle-shape`, `square`, `trapezoid`.

**Seven need a dark foreground.** `trapezoid`, `saddle-shape`, `database`, `l-border`,
`quarter-circle-right`, `right-triangle` and `half-circle` put the glyph partly outside the artwork
on purpose, so the shape reads as a base under the glyph rather than a container. A white glyph
vanishes where it leaves the shape.

### Adding a shape

Shapes are SVG files in `mcps/sect-icon-generator/backgrounds/`. The slug is the filename without
the `bg-icon_` prefix, lowercased: `bg-icon_Arrow-Square.svg` becomes `"type": "arrow-square"`.

1. Draw it in a **square viewBox** with unfilled geometry. It is rasterised to a silhouette and
   tinted, so raster `<image>` elements are rejected.
2. Add a `#ed1c24` rect marking where the foreground glyph should sit. The rect is stripped before
   rendering and read as the glyph's placement. It may be non-square.
3. Save it as `bg-icon_<Name>.svg` in `backgrounds/`.

It is available immediately, with no code change.

## Using the icons in C#

Every embedded icon is `Properties.Resources.[XX]_[Name]`.

```csharp
// a component's icon
protected override Bitmap Icon => Properties.Resources.MC_FindBoard;

// the ribbon icon, in your GH_AssemblyPriority class
Instances.ComponentServer.AddCategoryIcon("MiroConnect", Properties.Resources.MC_MiroConnectLogo);
```
