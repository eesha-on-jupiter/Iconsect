# Iconsect

> *Layered icon generation for Grasshopper plugins: pick a look, render every icon, embed them in `Resources.resx`.*

Iconsect is a Claude Code plugin that gives every component in a Grasshopper plugin a matching icon:
a background shape (solid or gradient), an optional watermark glyph and a foreground glyph from
[Iconify](https://iconify.design), rendered at 24×24 for components and 16×16 for the ribbon, then
embedded into `Resources.resx` and `Resources.Designer.cs`.

> This is the plugin folder's readme. The **[repository readme](../README.md)** is the full
> reference: every command, the skill and every MCP tool in one page.

**You pick the style. Iconsect renders and embeds.**

---

## Install

Iconsect is a standard Claude Code plugin (manifest at `.claude-plugin/plugin.json`).

**From a marketplace**

```
/plugin install iconsect --marketplace eesha-on-jupiter/Iconsect
```

On Claude Code older than 2.1.275, do it in two steps:

```
/plugin marketplace add eesha-on-jupiter/Iconsect   # this repo carries .claude-plugin/marketplace.json
/plugin install iconsect
```

**Local development:** point Claude Code at the plugin folder:

```
claude --plugin-dir /path/to/Iconsect/iconsect
```

After install, confirm the MCP server is connected (it loads from `plugin.json`):

```
/mcp
# expect: iconsect → sect-icon-generator  (connected)
```

> **Requirements:** Python ≥ 3.10 with `mcp[cli] httpx resvg-py pillow`
> (`pip install -r mcps/sect-icon-generator/requirements.txt`). The server is launched as
> **`python`**, so that exact command must resolve to a real Python ≥ 3.10 on PATH. On macOS/Linux
> it is often only `python3`, and on Windows it can hit the Microsoft Store stub; both show up as
> the server "not connected" (see [troubleshooting](docs/troubleshooting.md)).
>
> Rendering works on any OS and needs network access to Iconify. **Embedding into `Resources.resx`
> is Windows-only**: it shells out to PowerShell's `ResXResourceWriter`.

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

Answer the questions (plugin name, icon prefix), look at the contact sheet it renders, and pick a
fill style and a shape. It writes `icons.json`. Fill in each component's `fg_iconify_id`, then run
`/icon-gen`, `dotnet build`, and reload Rhino.

---

## Commands

| Command | What it does |
|---|---|
| `/icon-init` | Create `icons.json`: asks for the plugin name and prefix, previews the options, writes the chosen style |
| `/icon-preview [glyph]` | Render every background shape in each fill style and pick one |
| `/icon-gen [component]` | Render icons from `icons.json` and embed them, for one component or all |
| `/icon-embed [component]` | Embed already-rendered PNGs (including hand-made ones) into `Resources.resx` |

Full reference: [docs/commands.md](docs/commands.md).

---

## Documentation

- [Overview](docs/index.md)
- [Commands](docs/commands.md)
- [The `icons.json` reference](docs/icons-json.md)
- [The MCP server](docs/mcp.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## What's inside

`4 commands · 1 skill · 1 MCP server · 30 background shapes`. Contributor notes are in
[`CLAUDE.md`](CLAUDE.md), including how the icon engine is kept at parity with
[PleaseREST](https://github.com/eesha-on-jupiter/PleaseREST); what changed and when is in
[`CHANGELOG.md`](CHANGELOG.md).

**Author:** Eesha Jain · **Version:** 0.1.0
