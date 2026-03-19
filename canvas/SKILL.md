---
name: canvas
description: Interact with the OpenClaw Canvas web server for visual UI surfaces. Use when pushing A2UI JSONL dashboards, serving static HTML/CSS/JS files, querying canvas state from the SQLite cache, or switching between iframe and A2UI rendering modes. Covers session-scoped canvas URLs, static file storage, JSONL persistence, and all available A2UI components.
---

# Canvas Web Server

The Canvas web server ([haliphax-openclaw/openclaw-canvas-web](https://github.com/haliphax-openclaw/openclaw-canvas-web)) registers as a node with the OpenClaw gateway and serves two types of content per agent session:

1. **Static files** (iframe mode) — HTML/CSS/JS served from the agent's workspace
2. **A2UI surfaces** (component mode) — Declarative UI pushed via JSONL commands

## Requirements

- `canvas-web` MCP server configured in mcporter (see `~/openclaw-canvas-web/mcp/`)
- `sqlite3` binary available on the system (for querying A2UI surface state)
- OpenClaw Canvas web server running and connected to the gateway (appears as "Canvas Web Server" in `openclaw nodes status`)

## Required Configuration

Store the following in your `TOOLS.md` file:

```markdown
## Canvas
- **Canvas Base URL:** <base-url>  (e.g. https://example.com/canvas)
```

Ask your human for the canvas base URL if you don't have it. All canvas session URLs are derived from this value.

## Your Canvas Session

Each agent has a personal canvas session URL:

```
<CANVAS_BASE_URL>/<agent-id>/
```

The session name matches your agent ID. All A2UI pushes and static files are scoped to this session.

## Static File Storage

Static canvas files live in your workspace's `canvas/` directory:

```
~/.openclaw/workspaces/<agent-id>/canvas/
```

The server maps agent IDs to workspace canvas directories and serves files at `/_c/<session>/<path>`.

### File organization

- **Long-lived JSONL files** — Store in `canvas/jsonl/` for dashboards and surfaces you want to persist and re-push across sessions. Files here are **auto-pushed** — the server watches this directory and automatically pushes A2UI commands when `.jsonl` files are created or modified. No need to call mcporter.
- **Temporary JSONL files** — Store in `canvas/tmp/` for short-lived session work, experiments, and one-off surfaces

> **Note:** The `jsonl/` and `tmp/` subdirectories are ignored by the iframe file watcher by default (no iframe reloads). The `jsonl/` directory has its own dedicated watcher that auto-pushes A2UI content instead.

```
~/.openclaw/workspaces/<agent-id>/canvas/
├── index.html               # static HTML served via iframe
├── jsonl/
│   └── dashboard.jsonl      # persistent dashboard definition
├── tmp/
│   ├── debug-surface.jsonl  # temporary experiment
│   └── test-layout.jsonl    # one-off layout test
```

## Pushing Content to the Canvas

Choose the right approach based on your task:

- **Updating data** (new rows, refreshed content, data-bound text): Read [references/data-sources.md](references/data-sources.md)
- **Updating components** (layout changes, new components, filter options, new surfaces): Read [references/surface-updates.md](references/surface-updates.md)

For most dashboard refreshes, a `dataSourcePush` is all you need — no component changes required.

### Other canvas commands

| MCP Tool | Description |
|----------|-------------|
| `canvas_push` | Push A2UI JSONL payload |
| `canvas_reset` | Clear all A2UI surfaces for a session |
| `canvas_show` | Show the canvas panel. Accepts an optional `target` param for external URL navigation. |
| `canvas_hide` | Hide the canvas panel |
| `canvas_navigate` | Navigate to a path, URL, or `openclaw-canvas://` URI (see below) |
| `canvas_eval` | Execute JavaScript in the canvas (pass code via `javaScript` param) |
| `canvas_snapshot` | Capture a screenshot (returns `{ format, base64 }`) |

All tools accept an optional `session` parameter.

### Navigation URL schemes

`canvas_navigate` supports three URL types:

- **Relative path** — navigates within the current session's canvas directory (e.g., `index.html`)
- **External URL** (`http://`, `https://`, `data:`) — loads the URL in the canvas iframe directly. Deep link and snapshot scripts are injected automatically into `data:` URLs.
- **`openclaw-canvas://` URI** — session-scoped navigation. Format: `openclaw-canvas://<session>/<path>`. The session is extracted from the URI and the canvas switches to that session's file.

```bash
# Navigate to another agent's canvas file
mcporter call canvas-web.canvas_navigate url="openclaw-canvas://developer/dashboard.html"

# Navigate to an external URL
mcporter call canvas-web.canvas_navigate url="https://example.com/report.html"
```

## Switching Between Iframe and A2UI

The canvas view auto-switches based on content:

- **A2UI mode** activates when a surface has a `root` set (via `createSurface`) and no static file subpath is in the URL
- **Iframe mode** activates when navigating to a static file path (e.g., `/<agent-id>/index.html`)

To force iframe mode, navigate to a specific file. To force A2UI mode, push a surface with `createSurface`.

To clear A2UI and return to iframe:

```bash
mcporter call canvas-web.canvas_reset session=<agent-id>
```

## Theming

Surfaces support DaisyUI theming via the `theme` property on `createSurface`. The value is a DaisyUI theme name string applied as `data-theme` on the renderer container.

### Setting a theme

Include `theme` in your `createSurface` JSONL command:

```json
{"createSurface": {"surfaceId": "main", "theme": "synthwave"}}
```

If omitted, the default theme is `dark`.

### Available themes

Any [DaisyUI theme](https://daisyui.com/docs/themes/) is valid. Common options:

| Theme | Description |
|-------|-------------|
| `dark` | Default dark theme |
| `light` | Light theme |
| `cyberpunk` | Bright yellow/pink retro-futuristic |
| `synthwave` | Dark purple/navy with neon accents |
| `retro` | Warm vintage palette |
| `dracula` | Dark with purple/pink highlights |
| `business` | Professional dark theme |

### Switching themes

Push a new `createSurface` with a different `theme` value. The theme updates live without a page refresh:

```json
{"createSurface": {"surfaceId": "main", "theme": "cyberpunk"}}
```

### Persistence

Theme and `catalogId` are persisted in the SQLite cache. Both survive server restarts and are included in surface replay on client reconnect.

### Catalog ID

Surfaces accept an optional `catalogId` URI identifying the component catalog in use. When omitted, the default is `https://haliphax-openclaw.github.io/a2ui/1.0/catalog/all`.

```json
{"createSurface": {"surfaceId": "main", "theme": "dark", "catalogId": "https://haliphax-openclaw.github.io/a2ui/1.0/catalog/basic"}}
```

Catalog namespace: `https://haliphax-openclaw.github.io/a2ui/1.0/`

| URI | Description |
|-----|-------------|
| `.../catalog/all` | All built-in and 3rd party components (default) |
| `.../catalog/basic` | A2UI basic components only |
| `.../catalog/extended` | All built-in components |

## Querying State from SQLite

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).

A2UI surface state is persisted in a SQLite cache at:

```
~/.openclaw-canvas/a2ui-cache.db
```

Table: `a2ui_surfaces`

| Column | Type | Description |
|--------|------|-------------|
| `session` | TEXT (PK) | Session name (matches agent ID) |
| `surfaceId` | TEXT (PK) | Surface identifier |
| `components` | TEXT (JSON) | Component map `{ id: component }` |
| `root` | TEXT | Root component ID |
| `dataModel` | TEXT (JSON) | Data model including `$sources` |
| `theme` | TEXT | DaisyUI theme name |
| `catalogId` | TEXT | Catalog URI |

The primary key is the composite `(session, surfaceId)`.

Query examples:

```bash
# List all surfaces across all sessions
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT session, surfaceId, root FROM a2ui_surfaces"

# List surfaces for a specific agent session
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT surfaceId, root FROM a2ui_surfaces WHERE session='<agent-id>'"

# Dump a surface's components
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT components FROM a2ui_surfaces WHERE session='<agent-id>' AND surfaceId='main'" | jq .

# Check data sources
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT json_extract(dataModel, '$.\$sources') FROM a2ui_surfaces WHERE session='<agent-id>' AND surfaceId='main'" | jq .
```

## JSONL Commands

A2UI content is pushed as newline-delimited JSON commands. For full details and examples:

- **Component/surface commands** (`updateComponents`, `createSurface`, `deleteSurface`): See [references/surface-updates.md](references/surface-updates.md)
- **Data commands** (`dataSourcePush`, `updateDataModel`): See [references/data-sources.md](references/data-sources.md)

### Validation feedback

`canvas_push` returns per-command validation results. Each command in the batch gets a result with `ok`, `command`, `index`, and `error` (on failure). Use this to detect and fix issues without guessing.

Example response for a batch with one valid and one invalid command:

```json
{
  "ok": true,
  "results": [
    { "ok": true, "command": "createSurface", "index": 0 },
    { "ok": false, "command": "updateComponents", "index": 1, "error": "updateComponents: components must be an array" }
  ],
  "errors": [
    { "ok": false, "command": "updateComponents", "index": 1, "error": "updateComponents: components must be an array" }
  ]
}
```

The `errors` array is a convenience filter — same entries as the failed results. If `errors` is empty, all commands succeeded.

Common validation errors:
- `createSurface: missing surfaceId`
- `updateComponents: components must be an array`
- `Unrecognized command`

When errors are returned, fix the failing commands and re-push. The valid commands in the batch are still processed — only the invalid ones are skipped.

> **Streaming interface:** Scripts and non-agent consumers can also connect directly to the canvas server's WebSocket and stream JSONL commands with per-command validation feedback in real-time. This is not available through agent tool calls, which use the batch interface described above.

## Components and Reactive Data Binding

For the full list of available A2UI components, their JSONL schemas, and use cases, see:

- [references/components.md](references/components.md) — Full component reference (layout, containers, display, inputs)
- [references/reactive.md](references/reactive.md) — Data sources, filtering, aggregates, and Repeat templates
### Component summary

| Category | Components |
|----------|-----------|
| Layout | Column, Row, Stack, Spacer, Divider |
| Containers | Accordion (collapsible panels), Tabs (switchable tabbed panels) |
| Display | Text, Badge, Image, ProgressBar, Table, Repeat |
| Input | Button, Checkbox, Select, MultiSelect, Slider |

### Key features

- **Sorting** — Table and Repeat support optional `sortable` prop. Tables sort by clicking column headers (⬆/⬇); Repeat includes a sort direction dropdown.
- **Formatting** — Table supports column-level display formatters via the `formatters` prop (e.g., `boolean` for ✅/❌ rendering).
- **Filtering** — Select and MultiSelect bind to data sources for reactive filtering. Clearing a MultiSelect shows all data (empty selection = no filter).
- **Reactive props** — Accordion `expanded` and Tabs `active` props react to surface updates, allowing agents to programmatically toggle panels or switch tabs.

## Deep Linking

Both iframe content and A2UI components can take advantage of the canvas URL schemes:

- **`openclaw://`** — triggers agent runs via a confirmation dialog. See [references/deep-linking.md](references/deep-linking.md) for the full URL format, parameters, and security details.
- **`openclaw-canvas://`** — session-relative content references (e.g., images served from an agent's canvas directory).
