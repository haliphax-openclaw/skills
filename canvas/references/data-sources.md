# Pushing Data Source Updates

Use `dataSourcePush` or `dataModelUpdate` to update data that powers reactive components (Tables, Badges, Text, ProgressBar, Repeat, filtered Selects). This is for data changes — no component structure changes needed.

## Auto-push via file watcher

The simplest way to push data is to write a `.jsonl` file to your `canvas/jsonl/` directory. The server watches this directory and automatically pushes A2UI commands when files are created or modified — no mcporter call needed.

```bash
# Just write the file — the server handles the rest
echo '{"dataSourcePush":{"surfaceId":"main","sources":{"users":{"fields":["name"],"rows":[{"name":"Alice"}]}}}}' > ~/.openclaw/workspaces/<agent-id>/canvas/jsonl/users-data.jsonl
```

Multiple `.jsonl` files can target the same `surfaceId` (e.g., `dashboard-layout.jsonl` for components, `dashboard-data.jsonl` for data). They merge in the SQLite cache.

The watcher debounces writes (300ms) to avoid pushing partial file content.

## When to use
- Refreshing data displayed in Tables, Repeat, Badges, or data-bound Text/ProgressBar components
- Pushing new rows to existing data sources
- Updating narrative text stored in data sources (via Text template interpolation)
- Incrementally merging new data with existing rows

## JSONL Commands

### `dataSourcePush`

Shorthand for pushing data sources. Preferred for most data updates.

```jsonl
{"dataSourcePush":{"surfaceId":"main","sources":{"users":{"fields":["id","name","role"],"rows":[{"id":"1","name":"Alice","role":"admin"}],"primaryKey":"id"}}}}
```

Multiple sources can be pushed in a single command:

```jsonl
{"dataSourcePush":{"surfaceId":"main","sources":{"users":{...},"tasks":{...},"content":{...}}}}
```

### `dataModelUpdate`

Lower-level command. Data sources go under the `$sources` key. Supports `merge: true` for incremental updates by primary key.

```jsonl
{"dataModelUpdate":{"surfaceId":"main","data":{"$sources":{"users":{"fields":["id","name"],"rows":[{"id":"1","name":"Alice"}],"primaryKey":"id"}}}}}
```

#### Incremental merge

When `merge: true` is set and the source has a `primaryKey`, existing rows are updated by key and new rows are appended:

```jsonl
{"dataModelUpdate":{"surfaceId":"main","merge":true,"data":{"$sources":{"users":{"rows":[{"id":"1","name":"Alice Updated"},{"id":"3","name":"Charlie"}]}}}}}
```

## Pushing

```bash
# From a JSONL file
mcporter call canvas-web.canvas_push session=<agent-id> file=<path-to-file>

# Inline payload
mcporter call canvas-web.canvas_push session=<agent-id> payload='{"dataSourcePush":{...}}'
```

## Data source schema

```ts
interface DataSource {
  fields: string[]                    // column/field names
  rows: Record<string, unknown>[]     // array of row objects
  primaryKey?: string                 // optional key for incremental merges
}
```

## Reactive data binding

Components that support data binding update automatically when their bound data source changes:

| Component | Data binding support |
|-----------|---------------------|
| Text | `{{field}}` template interpolation against first filtered row, `{{$value}}`/`{{$key}}` for aggregates |
| ProgressBar | `{{field}}` template interpolation in `label` and `value` props |
| Badge | Aggregate display with `map` templates |
| Table | Column display from data source rows |
| Repeat | Template rendering per row with `{{field}}` placeholders |
| Select/MultiSelect | Filter binding via `bind` prop |

For full details on filtering, aggregates, and reactive binding, see [reactive.md](reactive.md).
