---
name: canvas
description: Interact with the OpenClaw Canvas web server for visual UI surfaces. Use when pushing A2UI JSONL dashboards, serving static HTML/CSS/JS files, querying canvas state from the SQLite cache, or switching between iframe and A2UI rendering modes. Covers session-scoped canvas URLs, static file storage, JSONL persistence, and all available A2UI components.
---

# Canvas Web Server

The Canvas web server ([haliphax-openclaw/openclaw-canvas-web](https://github.com/haliphax-openclaw/openclaw-canvas-web)) registers as a node with the OpenClaw gateway and serves two types of content per agent session:

1. **Static files** (iframe mode) — HTML/CSS/JS served from the agent's workspace
2. **A2UI surfaces** (component mode) — Declarative UI pushed via JSONL commands

## Requirements

- `jq` binary available on the system (for encoding JSONL payloads)
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
<CANVAS_BASE_URL>/session/<agent-id>/
```

The session name matches your agent ID. All A2UI pushes and static files are scoped to this session.

## Static File Storage

Static canvas files live in your workspace's `canvas/` directory:

```
~/.openclaw/workspaces/<agent-id>/canvas/
```

The server maps agent IDs to workspace canvas directories and serves files at `/_c/<session>/<path>`.

### File organization

- **Long-lived JSONL files** — Store in `canvas/jsonl/` for dashboards and surfaces you want to persist and re-push across sessions
- **Temporary JSONL files** — Store in `canvas/tmp/` for short-lived session work, experiments, and one-off surfaces

> **Note:** The `jsonl/` and `tmp/` subdirectories are ignored by the file watcher by default. Files placed there won't trigger iframe reloads. This is configurable via the `OPENCLAW_CANVAS_IGNORE_DIRS` environment variable.

```
~/.openclaw/workspaces/<agent-id>/canvas/
├── index.html               # static HTML served via iframe
├── jsonl/
│   └── dashboard.jsonl      # persistent dashboard definition
├── tmp/
│   ├── debug-surface.jsonl  # temporary experiment
│   └── test-layout.jsonl    # one-off layout test
```

## Pushing A2UI Surfaces

Use `openclaw nodes invoke` to push JSONL content to your canvas session. The `session` parameter is required to scope the push to your canvas URL.

```bash
# Build the payload and push
PAYLOAD=$(cat canvas/dashboard.jsonl | jq -Rs '.')
openclaw nodes invoke \
  --node "Canvas Web Server" \
  --command "canvas.a2ui.pushJSONL" \
  --params "{\"session\":\"<agent-id>\",\"payload\":$PAYLOAD}"
```

Without `session`, the push defaults to `main` and renders on the main agent's canvas.

### Incremental updates

Push only the components that changed — the server merges by component ID:

```bash
echo '{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"my-badge","component":{"Badge":{"text":"Updated","variant":"success"}}}]}}' > /tmp/update.jsonl
PAYLOAD=$(cat /tmp/update.jsonl | jq -Rs '.')
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.a2ui.pushJSONL" \
  --params "{\"session\":\"<agent-id>\",\"payload\":$PAYLOAD}"
```

### Other canvas commands

| Command | Description |
|---------|-------------|
| `canvas.present` | Show the canvas panel. Accepts an optional `target` or `url` param — if it's an http/https/data URL, the canvas navigates to that external URL directly. |
| `canvas.hide` | Hide the canvas panel |
| `canvas.navigate` | Navigate to a path, URL, or `openclaw-canvas://` URI (see below) |
| `canvas.eval` | Execute JavaScript in the canvas (pass code via `javaScript` param) |
| `canvas.snapshot` | Capture a screenshot (returns `{ format, base64 }`) |
| `canvas.a2ui.push` | Push A2UI JSONL (alias for pushJSONL) |
| `canvas.a2ui.pushJSONL` | Push A2UI JSONL payload |
| `canvas.a2ui.reset` | Clear all A2UI surfaces (pass `session` to clear one session) |

### Navigation URL schemes

`canvas.navigate` supports three URL types:

- **Relative path** — navigates within the current session's canvas directory (e.g., `index.html`)
- **External URL** (`http://`, `https://`, `data:`) — loads the URL in the canvas iframe directly. Deep link and snapshot scripts are injected automatically into `data:` URLs.
- **`openclaw-canvas://` URI** — session-scoped navigation. Format: `openclaw-canvas://<session>/<path>`. The session is extracted from the URI and the canvas switches to that session's file.

```bash
# Navigate to another agent's canvas file
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.navigate" \
  --params '{"url":"openclaw-canvas://developer/dashboard.html"}'

# Navigate to an external URL
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.navigate" \
  --params '{"url":"https://example.com/report.html"}'
```

## Switching Between Iframe and A2UI

The canvas view auto-switches based on content:

- **A2UI mode** activates when a surface has a `root` set (via `beginRendering`) and no static file subpath is in the URL
- **Iframe mode** activates when navigating to a static file path (e.g., `/session/<agent-id>/index.html`)

To force iframe mode, navigate to a specific file. To force A2UI mode, push a surface with `beginRendering`.

To clear A2UI and return to iframe:

```bash
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.a2ui.reset" \
  --params "{\"session\":\"<agent-id>\"}"
```

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

## JSONL Command Reference

Every A2UI push is a newline-delimited sequence of JSON commands:

| Command | Purpose |
|---------|---------|
| `surfaceUpdate` | Create or update components on a surface |
| `beginRendering` | Set the root component and activate A2UI rendering |
| `dataModelUpdate` | Update the data model (use `$sources` key for data sources) |
| `dataSourcePush` | Shorthand for pushing data sources without `$sources` nesting |
| `deleteSurface` | Remove a surface |

### Minimal surface

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":["hello"]}}},{"id":"hello","component":{"Text":{"text":"Hello from Canvas","usageHint":"h1"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
```

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
