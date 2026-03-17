# A2UI Components Reference

All components are specified as JSONL within `surfaceUpdate` commands. Each component has an `id` and a `component` object keyed by type name.

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"my-id","component":{"ComponentType":{...props}}}]}}
```

## Layout Components

### Column

Vertical stack of child components. Use as the root layout or to group elements vertically.

```json
{"Column": {"children": ["child-id-1", "child-id-2", "child-id-3"]}}
```

| Prop | Type | Description |
|------|------|-------------|
| `children` | `string[]` | Ordered list of child component IDs |

### Row

Horizontal layout of child components with gap spacing. Use for side-by-side elements like filter controls, stat badges, or title + version.

```json
{"Row": {"children": ["left-item", "spacer", "right-item"]}}
```

| Prop | Type | Description |
|------|------|-------------|
| `children` | `string[]` | Ordered list of child component IDs |

### Stack

Generic container for layered/stacked children. Similar to Column but for overlay-style layouts.

```json
{"Stack": {"children": ["background", "foreground"]}}
```

| Prop | Type | Description |
|------|------|-------------|
| `children` | `string[]` | Ordered list of child component IDs |

### Spacer

Flexible space that pushes siblings apart in a Row or Column. No props.

```json
{"Spacer": {}}
```

Use case: Push a version label to the right side of a Row while a filter stays left.

### Divider

Horizontal rule separator. No props.

```json
{"Divider": {}}
```

Use case: Visual separation between dashboard sections.

## Display Components

### Text

Text display with semantic HTML tag hints. Supports static text or data source binding.

```json
{"Text": {"text": "Dashboard Title", "usageHint": "h1"}}
{"Text": {"text": {"literalString": "Also valid"}, "usageHint": "body"}}
```

| Prop | Type | Description |
|------|------|-------------|
| `text` | `string` or `{ literalString: string }` | Display text |
| `usageHint` | `string` | HTML tag: `h1`–`h6`, `body` (→ `<p>`), `label` (→ `<span>`) |
| `dataSource` | `DataSourceBinding` | Bind to data source for dynamic text |

Use cases: Headings, labels, section titles, dynamic counters.

### Badge

Inline colored badge with variant styling. Supports static text or aggregate data binding.

```json
{"Badge": {"text": "3 active", "variant": "success"}}
```

| Prop | Type | Description |
|------|------|-------------|
| `text` | `string` | Static display text |
| `variant` | `string` | `info` (default), `success`, `warning`, `error` |
| `dataSource` | `DataSourceBinding` | Bind with aggregates for dynamic values |

Data-bound example:

```json
{"Badge": {"variant": "info", "dataSource": {"source": "users", "aggregate": {"fn": "count"}, "map": {"text": "{{$value}} users"}}}}
```

Use cases: Status indicators, KPI counters, summary stats.

### Image

Displays an image. URLs referencing `openclaw-canvas://` paths are rewritten to the canvas file server.

```json
{"Image": {"src": "https://example.com/logo.png", "alt": "Logo"}}
```

| Prop | Type | Description |
|------|------|-------------|
| `src` | `string` | Image URL (http/https or canvas-relative path) |
| `alt` | `string` | Alt text |

### ProgressBar

Horizontal progress bar with optional label. Value is clamped 0–100.

```json
{"ProgressBar": {"label": "Upload: 75%", "value": 75}}
```

| Prop | Type | Description |
|------|------|-------------|
| `value` | `number` | Progress percentage (0–100) |
| `label` | `string` | Optional label above the bar |

Use cases: Token usage bars, completion tracking, health indicators. Commonly used inside Repeat templates.

## Data Components

### Table

Tabular data display. Two modes: static (headers + rows) or data-source-bound.

**Static:**

```json
{"Table": {"headers": ["Name", "Status"], "rows": [["Alice", "Active"], ["Bob", "Idle"]]}}
```

**Data source:**

```json
{"Table": {"dataSource": {"source": "users", "columns": ["name", "role", "email"]}, "sortable": true}}
```

| Prop | Type | Description |
|------|------|-------------|
| `headers` | `string[]` | Static column headers |
| `rows` | `unknown[][]` | Static row data (array of arrays) |
| `dataSource` | `DataSourceBinding` | Bind to filtered data source |
| `sortable` | `boolean` | Enable click-to-sort on column headers |

Sorting cycles: unsorted → ascending (⬆) → descending (⬇) → unsorted.

Use cases: Agent session lists, cron job tables, CI run history.

### Repeat

Iterates over data source rows and renders a template component per row. Supports sorting and transforms.

```json
{"Repeat": {"dataSource": {"source": "agents"}, "template": {"ProgressBar": {"label": "{{name}} — {{tokens}}", "value": "{{usage_pct}}"}}, "emptyText": "No data", "sortable": true, "sortField": "usage_pct"}}
```

| Prop | Type | Description |
|------|------|-------------|
| `dataSource` | `DataSourceBinding` | Data source to iterate |
| `template` | `Record<string, object>` | Component template with `{{field}}` placeholders |
| `transforms` | `Record<string, { fn: string }>` | Named transforms (e.g., `percentOfMax`) |
| `emptyText` | `string` | Shown when no rows match filters |
| `sortable` | `boolean` | Show sort direction dropdown |
| `sortField` | `string` | Field to sort by (required when sortable) |

Supported template components: `ProgressBar`, `Text`, `Badge`.

Use cases: Per-agent token bars, score leaderboards, dynamic lists.

## Interactive Components

### Select

Single-selection dropdown. Emits `a2ui.selectChange` on change. Supports filter binding.

```json
{"Select": {"options": [{"label": "All", "value": ""}, {"label": "Active", "value": "active"}], "selected": "", "bind": {"source": "items", "field": "status", "nullValue": ""}}}
```

| Prop | Type | Description |
|------|------|-------------|
| `options` | `{ label: string, value: string }[]` | Dropdown options |
| `selected` | `string` | Current value |
| `bind` | `FilterBind` | Filter binding (see reactive.md) |

### MultiSelect

Multi-selection dropdown. Same component as Select but with array values. Use `op: "in"` for filter binding.

```json
{"MultiSelect": {"options": [{"label": "Admin", "value": "admin"}, {"label": "Editor", "value": "editor"}], "selected": ["admin", "editor"], "bind": {"source": ["users", "logs"], "field": "role", "op": "in", "nullValue": ["admin", "editor"]}}}
```

| Prop | Type | Description |
|------|------|-------------|
| `options` | `{ label: string, value: string }[]` | Dropdown options |
| `selected` | `string[]` | Currently selected values |
| `bind` | `FilterBind` | Filter binding (source can be string or string[]) |

### Button

Clickable button. Emits `a2ui.buttonClick` with `componentId` on click.

```json
{"Button": {"label": "Refresh"}}
```

| Prop | Type | Description |
|------|------|-------------|
| `label` | `string` | Button text |

### Checkbox

Toggle checkbox. Emits `a2ui.checkboxChange` with `componentId` and `checked` state.

```json
{"Checkbox": {"label": "Show inactive", "checked": false}}
```

| Prop | Type | Description |
|------|------|-------------|
| `label` | `string` | Checkbox label |
| `checked` | `boolean` | Current state |

### Slider

Range input. Emits `a2ui.sliderChange` with `componentId` and numeric `value`.

```json
{"Slider": {"label": "Threshold", "min": 0, "max": 100, "value": 50}}
```

| Prop | Type | Description |
|------|------|-------------|
| `label` | `string` | Optional label |
| `min` | `number` | Minimum value (default: 0) |
| `max` | `number` | Maximum value (default: 100) |
| `value` | `number` | Current value |
