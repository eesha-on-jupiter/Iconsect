# Commands

Four commands, all run from the root of the Grasshopper plugin you are making icons for.

| Command | Writes | Needs `icons.json` |
|---|---|---|
| [`/icon-init`](#icon-init) | `icons.json`, `Icons/_preview/` | no, it creates it |
| [`/icon-preview [glyph]`](#icon-preview-glyph) | `Icons/_preview/`, and `defaults.background` if you pick | no |
| [`/icon-gen [component]`](#icon-gen-component) | PNGs in `Icons/`, `Resources.resx`, `Resources.Designer.cs` | yes |
| [`/icon-embed [component]`](#icon-embed-component) | `Resources.resx`, `Resources.Designer.cs` | yes |

A typical first run is `/icon-init`, then fill in each component's `fg_iconify_id`, then `/icon-gen`.

---

## `/icon-init`

Creates `icons.json`. Run it once per plugin.

1. If an `icons.json` already exists, it shows the current name, prefix and background, and asks
   whether to keep it or start over. It never overwrites without confirmation.
2. Asks for the basics, suggesting values it can read from the project:

   | Setting | Example | Default |
   |---|---|---|
   | Plugin name | `MiroConnect` | from the `.csproj` |
   | Plugin prefix | `MC` | none, you choose |
   | Icons folder | `Icons` | `Icons` |
   | resx path | `Properties/Resources.resx` | `Properties/Resources.resx` |

3. Renders every background option to `Icons/_preview/contact-sheet.png` and asks for a fill style
   and a shape. See [the three background styles](icons-json.md#the-background-styles).
4. Writes `icons.json` with your style, and a `components` array seeded from the component classes
   it finds in the project.

Every icon embeds as `[prefix]_[Name]`, so the prefix is worth choosing carefully.

## `/icon-preview [glyph]`

Renders every background shape in gradient, solid and no-background, so a look gets chosen rather
than inherited. Run it before authoring icons, or any time you want to restyle a plugin.

- **`glyph`** is an Iconify ID such as `mdi:database`, used as the sample foreground. It defaults to
  `mdi:star`. A glyph from your plugin's own domain reads better than a placeholder.
- It is read-only unless you pick something. If you do, it sets `defaults.background` and leaves
  every per-subcategory and per-component override alone.
- With no `icons.json` yet, it hands you the snippet and suggests `/icon-init`.

Tell it your brand colours and it previews in those. Ask to compare a few shapes and it narrows the
sheet to them.

`Icons/_preview/` is scratch. Delete it, or git-ignore it.

## `/icon-gen [component]`

Renders icons from `icons.json` and embeds each one. It renders what the file says and does not
re-author it.

- **No argument:** every component, then the 16×16 ribbon icon.
- **`component`:** that one component, matched on its `name` in `icons.json`.

Before rendering, it lists any component whose `fg_iconify_id` is missing or still a placeholder and
asks whether to fill those in or render the rest. A bad Iconify ID is the most common render
failure.

Components marked `"custom": true` are skipped, which is not a failure. They still need
`/icon-embed`.

It ends with a summary of rendered, skipped, embedded and failed, then asks you to glance at
`Icons/` and name any to redo.

> A changed icon needs `dotnet build` and a Rhino reload before it shows up in Grasshopper.

## `/icon-embed [component]`

Embeds PNGs that already exist in `Icons/`, without rendering. Use it for:

- hand-made (`"custom": true`) icons, which `/icon-gen` never renders
- re-running an embed that failed, usually because it was attempted off Windows

It checks that each `[Icons]/[XX]_[Name].png` exists before calling the tool, and reports missing
ones by name. The embed is idempotent: an existing resx key is replaced, not duplicated, so
re-running is safe.

> Embedding is **Windows-only**. On macOS or Linux the command says so and stops. Your PNGs are
> fine; the embed has to happen on a Windows machine.
