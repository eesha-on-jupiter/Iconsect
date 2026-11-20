# Iconsect: Overview

Iconsect gives every component in a [Grasshopper](https://www.grasshopper3d.com/) plugin a matching
icon. It is a Claude Code plugin: four slash commands, one skill and one MCP server that together
take a plugin from "no icons" to PNGs embedded in `Resources.resx`.

## What it produces

- **`icons.json`** at your plugin's root: the single file that describes every icon.
- **Component icons** at 24×24, one PNG per component, in your `Icons/` folder.
- **The ribbon icon** at 16×16, the category icon Grasshopper shows on the tab.
- **Embedded resources**: each PNG written into `Properties/Resources.resx`, with a strongly-typed
  property in `Resources.Designer.cs`, so component code can use `Properties.Resources.[XX]_[Name]`.

## How an icon is built

Every icon is a stack of independent, optional layers:

| Layer | What it is | Where it comes from |
|---|---|---|
| Background shape | A silhouette filled with one colour or a linear gradient | An SVG shipped with the plugin, 30 to choose from |
| Watermark | A faint glyph between the shape and the foreground | [Iconify](https://iconify.design), by `prefix:name` |
| Foreground glyph | The glyph that says what the component does | Iconify, by `prefix:name` |

Leave any layer out. A component with no background at all gets its glyph alone, filling the canvas.

## The shape of a run

1. **`/icon-init`** asks for the plugin name and icon prefix, renders the background options to a
   contact sheet, and writes `icons.json` with the style you pick.
2. You fill in each component's `fg_iconify_id`. Browse [iconify.design](https://iconify.design)
   for the IDs.
3. **`/icon-gen`** renders every icon and embeds it.
4. `dotnet build`, reload Rhino, and the icons are on the canvas.

`/icon-preview` restyles a plugin later. `/icon-embed` embeds PNGs without rendering them, for
hand-made icons.

## Design principles

- **A background is never chosen for you.** The options are rendered so you can see them, and
  nothing is written until you pick. The template's blue gradient is a placeholder that keeps the
  file valid, not a house style.
- **A preview is the real thing.** `preview_backgrounds` goes through the same renderer as
  `generate_icon`, so what you approve is what you get.
- **Set the style once.** Styles resolve `defaults` < `subcategories[sub]` < `components[i]`. A house
  style is inherited by every icon, and any single icon can override it.
- **Shapes are artwork, not code.** Drop an SVG into `backgrounds/` and it is available immediately.
- **Hand-made icons are safe.** Mark a component `"custom": true` and the generator never renders
  or overwrites its PNG.
- **No hidden config.** Every call names your `icons.json`. A missing path fails loudly instead of
  rendering another project's icons.

## Next

- [Commands](commands.md)
- [The `icons.json` reference](icons-json.md)
- [The MCP server](mcp.md)
- [Troubleshooting](troubleshooting.md)
