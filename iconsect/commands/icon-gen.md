---
description: "Render icons from icons.json and embed them into Resources.resx — one component or all."
argument-hint: "[component_name]"
---

# /icon-gen [component_name]

Render the plugin's icons from `icons.json` and embed each into `Resources.resx`.

Renders what `icons.json` already says — it does not re-author it. Use `/icon-init` to create the
file, `/icon-preview` to change the background style.

---

## Steps

1. Confirm `icons.json` exists at the project root.
   If not: "No icons.json found. Run /icon-init to create one." Stop.

2. Read `icons.json` for `plugin_name`, `plugin_prefix`, `resources_path`, `resx_path` and the
   component list. Note the path — every MCP call takes it as `config_path`.

3. Decide the scope:
   - `$ARGUMENTS` given → that one component only (match on the `name` in `icons.json`; if no match,
     list the available names and stop).
   - no argument → every component in `icons.json`, plus the 16×16 plugin icon.

4. **Check for missing glyphs first.** List any component whose `fg_iconify_id` is still a
   placeholder (`[prefix:name]`) or absent, and ask whether to fill them in now or render the rest.
   A bad Iconify ID is the most common render failure — catching it up front beats failing halfway.

5. **Skip `"custom": true` components.** The generator returns a skip message and never overwrites a
   hand-made `Icons/[XX]_[Name].png` — that is not a failure. They still need `/icon-embed`.
   If the user named a `custom` component explicitly, say it is hand-made and only embed it.

6. Render, per component:
   `generate_icon(component_name, config_path)` → then `add_to_resources(component_name, config_path)`
   Report progress as each one lands.

7. Render the plugin icon last, as a separate step, when no component argument was given, and only
   if `icons.json` has a `plugin_icon` block with a real `fg_iconify_id`:
   `generate_plugin_icon(config_path)` → `add_to_resources("[PluginName]Logo", config_path)`
   That is the 16×16 ribbon/category icon at resource `[XX]_[PluginName]Logo` — the name to pass to
   `AddCategoryIcon` in your assembly class.

8. Print the summary:
   ```
   Icons rendered.
     Rendered:  [n]
     Skipped:   [n] (custom — hand-made PNG kept)
     Embedded:  [n]
     Failed:    [n]
   ```
   List any failure with its message and the component it belongs to.

9. **Quick review.** List the files in `Icons/` and ask: "Glance at Icons/ and say 'ok', or name any
   to redo." Re-render named ones from an edited `icons.json`.

10. Remind the user that a changed icon needs `dotnet build` and a Rhino reload before it shows up in
    Grasshopper.

> `add_to_resources` shells out to PowerShell and is **Windows-only**. On macOS the PNGs are still
> written and step 6's embed reports a clear error — do the embed on Windows.
