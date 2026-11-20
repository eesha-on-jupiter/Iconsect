# Iconsect Changelog

Tracks changes to Iconsect itself (the commands, the skill and the MCP server) that change what a
render produces. `plugin.json`'s `version` is the source of truth.

Bump `plugin.json`'s `version` and add an entry here whenever a change would make an existing
`icons.json` render differently, or change what gets embedded. See `CLAUDE.md`.

## 0.1.0 (2026-10-28)

First public release.

- **Four commands.** `/icon-init` creates `icons.json`, `/icon-preview` shows the background
  options, `/icon-gen` renders and embeds, `/icon-embed` embeds existing PNGs.
- **One skill.** `sect-icons` covers picking a look, authoring `icons.json`, and rendering.
- **One MCP server.** `sect-icon-generator` renders layered icons (background shape, optional
  watermark, foreground glyph from Iconify) at 24×24 for components and 16×16 for the ribbon, and
  embeds them into `Resources.resx` and `Resources.Designer.cs`.
- **30 background shapes**, each an SVG that also carries its own glyph placement.
- **252 tests** for the MCP server.
