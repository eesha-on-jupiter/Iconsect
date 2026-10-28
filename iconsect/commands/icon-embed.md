---
description: "Embed already-rendered PNGs from Icons/ into Resources.resx and Resources.Designer.cs — one component or all."
argument-hint: "[component_name]"
---

# /icon-embed [component_name]

Embed icon PNGs into `Resources.resx` + `Resources.Designer.cs` without re-rendering them.

Use this for hand-made (`"custom": true`) icons, which `/icon-gen` deliberately never renders, or to
re-run the embed after it failed — typically because it was attempted off Windows.

---

## Steps

1. Confirm `icons.json` exists at the project root. If not: "No icons.json found. Run /icon-init."
   Stop.

2. **Windows check.** `add_to_resources` shells out to PowerShell's `ResXResourceWriter` and is
   **Windows-only**. On macOS or Linux, say so and stop — the PNGs in `Icons/` are fine, the embed
   just has to happen on a Windows machine.

3. Read `icons.json` for `plugin_prefix`, `resources_path` and `resx_path`, and decide the scope:
   - `$ARGUMENTS` given → that one component.
   - no argument → every component in `icons.json`, plus `[PluginName]Logo` if a `plugin_icon` block
     is configured.

4. **Check the PNG exists** for each name — `[resources_path]/[XX]_[Name].png`. Report any that are
   missing rather than calling the tool: a missing PNG means the icon was never rendered (run
   `/icon-gen`) or a `"custom": true` icon was never drawn.

5. Run MCP: sect-icon-generator → `add_to_resources(component_name, config_path)` for each.
   It is idempotent: an existing resx key is replaced rather than duplicated, and a
   `Resources.Designer.cs` that already declares the property is left alone, so re-running is safe.

6. Print the summary:
   ```
   Embedded.
     Embedded:  [n]
     Already present: [n]
     Missing PNG: [n]
     Failed:    [n]
   ```
   Name every missing PNG and every failure.

7. Remind the user that a `net48` project needs
   `<GenerateResourceUsePreserializedResources>true</GenerateResourceUsePreserializedResources>` and
   a `System.Resources.Extensions` package reference for binary resources, or the build fails with
   MSB3823 the moment the first bitmap lands. Then `dotnet build` and reload Rhino.
