---
description: "Render every background shape in each fill style so you can see the options and pick one."
argument-hint: "[iconify_id]"
---

# /icon-preview [iconify_id]

Show the background options — every shape in `backgrounds/`, rendered in gradient, solid, and with
no background at all — so a look gets chosen rather than inherited.

Read-only unless you pick something. Run it before authoring icons, or any time you want to change
the plugin's style.

---

## Steps

1. If `icons.json` exists at the project root, read `plugin_prefix`, `resources_path` and the
   current `defaults.background` from it, and say what the plugin is using now. If it doesn't exist,
   that's fine — the preview needs no config.

2. Pick the preview glyph. Use `$ARGUMENTS` if the user supplied an Iconify ID (`prefix:name`);
   otherwise default to `mdi:star`. A glyph from the plugin's own domain reads better than a
   placeholder.

3. Run MCP: sect-icon-generator →
   `preview_backgrounds(output_dir="Icons/_preview", fg_iconify_id=<glyph>, styles="gradient,solid,none")`
   Add `bg_icon_iconify_id=<glyph>` on a second pass to show the watermark layer. Pass
   `fill` / `gradient_from` / `gradient_to` / `gradient_angle` when the user already has brand
   colours in mind — the defaults are a neutral blue, not a house style.
   Narrow with `shapes="circle,hexagon,square"` if the user only wants to compare a few.

4. Show the returned catalog and point at `Icons/_preview/contact-sheet.png` — one labelled grid of
   every tile. Individual `preview_<slug>_<style>.png` files sit beside it.

5. **Ask the user to choose.** Never pick for them:
   ```
   Icon backgrounds — pick a look:

     Fill style   gradient   two-colour linear gradient behind the glyph
                  solid      one flat colour behind the glyph
                  none       no background at all — the glyph alone, edge to edge

     Shape        any of the [n] slugs in the catalog (ignored if you pick "none")

     Watermark    optional — a faint Iconify silhouette between the shape and the glyph

   Which style, and which shape?
   ```

6. **Warn about the dark-foreground shapes.** `trapezoid`, `saddle-shape`, `database`, `l-border`,
   `quarter-circle-right`, `right-triangle` and `half-circle` place the glyph partly outside the
   artwork by design — a white glyph will disappear where it leaves the shape, so those need a dark
   `fg_color`.

7. Write the choice, if `icons.json` exists. Set `defaults.background` (and `defaults.fg_color` when
   a foreground colour was picked):
   - gradient → `{ "shape": { "type": "<slug>", "gradient": { "from": "#…", "to": "#…", "angle": 135 } } }`
   - solid → `{ "shape": { "type": "<slug>", "fill": "#…" } }`
   - none → `{}`
   Leave every per-subcategory and per-component override alone — this sets the house default only.
   If there is no `icons.json` yet, hand the snippet back and suggest `/icon-init`.

8. Say what's next:
   - no `icons.json` yet → "Run /icon-init to create it with this style."
   - icons already rendered → "Run /icon-gen to re-render with the new style."

9. `Icons/_preview/` is scratch — mention it can be deleted, and should be git-ignored rather than
   committed.
