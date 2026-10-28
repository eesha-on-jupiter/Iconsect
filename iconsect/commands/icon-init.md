---
description: "Create icons.json for this project — asks for the plugin name and prefix, previews the background options, and writes the chosen style."
---

# /icon-init

Set up icon generation for a Grasshopper plugin: create `icons.json` at the project root, with a
background style the user actually picked.

Run this once per plugin. Use `/icon-preview` afterwards to change the look, `/icon-gen` to render.

---

## Steps

1. Check for an existing `icons.json` at the project root.
   If one exists: show its `plugin_name`, `plugin_prefix` and current `defaults.background`, then
   ask whether to keep it (stop, suggest `/icon-preview` to restyle) or start over. Never overwrite
   without confirmation — it holds every icon the user chose.

2. Ask for the basics, suggesting values read from the project where you can (the `.csproj` name,
   the folder name, an existing `Properties/Resources.resx`):
   - **Plugin name** — e.g. `MiroConnect`
   - **Plugin prefix** — the short resource prefix, e.g. `MC` (every icon embeds as `[XX]_[Name]`)
   - **Icons folder** — default `Icons`
   - **resx path** — default `Properties/Resources.resx`

3. Load skill: `sect-icons`.

4. **Pick the look.** Run MCP: sect-icon-generator →
   `preview_backgrounds(output_dir="Icons/_preview", fg_iconify_id=<a glyph from this plugin's domain>,
   styles="gradient,solid,none")`
   Show the returned catalog, point at `Icons/_preview/contact-sheet.png`, and ask for a fill style
   and a shape:
   ```
   Icon backgrounds — pick a look:

     Fill style   gradient   two-colour linear gradient behind the glyph
                  solid      one flat colour behind the glyph
                  none       no background at all — the glyph alone, edge to edge

     Shape        any of the [n] slugs in the catalog (ignored if you pick "none")

     Watermark    optional — a faint Iconify silhouette between the shape and the glyph

   Which style, and which shape?
   ```
   Never pick for them. Ask for colours too if they haven't said.

5. **Warn about the dark-foreground shapes.** If the pick is `trapezoid`, `saddle-shape`,
   `database`, `l-border`, `quarter-circle-right`, `right-triangle` or `half-circle`, say these place
   the glyph partly outside the artwork by design — a white glyph disappears where it leaves the
   shape, so use a dark `fg_color`.

6. Write `icons.json` at the project root, starting from
   `mcps/sect-icon-generator/icons.template.json` and deleting every `_`-prefixed documentation key.
   Fill in the answers from step 2, the chosen style in `defaults.background` and `plugin_icon`, and
   a `components` array — seeded from the project's existing component classes if you can find them,
   otherwise left empty with one commented example for the user to copy.

7. Show the file and say what's next:
   ```
   icons.json written.
     Style:      [gradient|solid|none] · [shape]
     Components: [n]

   Next: fill in each component's fg_iconify_id (browse iconify.design), then /icon-gen.
   ```
