# Reactive Data Binding

The A2UI reactive layer lets agents push structured data sources and bind UI components to that data. Filters, aggregates, and repeating templates update automatically as data or selections change.

## Data Sources

A data source is a named collection of rows with typed fields, stored per surface.

```ts
interface DataSource {
  fields: string[]                    // column/field names
  rows: Record<string, unknown>[]     // array of row objects
  primaryKey?: string                 // optional key for incremental merges
}
```

### Pushing data via `dataSourcePush`

The preferred shorthand — no `$sources` nesting required:

```jsonl
{"dataSourcePush":{"surfaceId":"main","sources":{"users":{"fields":["name","role"],"rows":[{"name":"Alice","role":"admin"},{"name":"Bob","role":"viewer"}],"primaryKey":"name"}}}}
```

### Pushing data via `dataModelUpdate`

Include a `$sources` key inside the `data` object. Can mix regular data model keys alongside:

```jsonl
{"dataModelUpdate":{"surfaceId":"main","data":{"title":"Dashboard","$sources":{"users":{"fields":["name","role"],"rows":[]}}}}}
```

### Incremental merge

Send `dataModelUpdate` with `merge: true` and a `primaryKey` to update existing rows by key and append new ones:

```jsonl
{"dataModelUpdate":{"surfaceId":"main","merge":true,"data":{"$sources":{"users":{"rows":[{"name":"Alice","role":"superadmin"},{"name":"Charlie","role":"editor"}]}}}}}
```

## Filter Binding

Filters are driven by Select/MultiSelect components via the `bind` property.

```ts
interface FilterBind {
  source: string | string[]   // data source name(s) to filter
  field: string               // field to filter on
  op?: string                 // filter operation (default: "eq")
  nullValue?: unknown         // value meaning "no filter" / show all
}
```

### Filter operations

| Op | Description | Value type |
|----|-------------|------------|
| `eq` | Exact equality (default) | `string \| number` |
| `contains` | Case-insensitive substring | `string` |
| `gte` | Greater than or equal | `number` |
| `lte` | Less than or equal | `number` |
| `range` | Within `[lo, hi]` | `[number, number]` |
| `in` | Value in array | `unknown[]` |

### Multi-source filtering

Target multiple data sources from one filter by passing an array of source names:

```json
{"bind": {"source": ["agents", "cron"], "field": "agent", "op": "in", "nullValue": ["main", "dev"]}}
```

### nullValue behavior

When the current selection equals `nullValue`, the filter is inactive — all rows pass through. For MultiSelect, array equality is checked. An empty MultiSelect selection also deactivates the filter.

## Display Binding (dataSource prop)

Components like Table, Badge, Text, and Repeat bind to data sources via the `dataSource` prop.

```ts
interface DataSourceBinding {
  source: string              // data source name
  columns?: string[]          // (Table) columns to display
  aggregate?: {               // single aggregate
    fn: 'count' | 'sum' | 'avg' | 'min' | 'max'
    field?: string            // required for sum/avg/min/max
    format?: 'compact'        // optional compact number formatting
  }
  aggregates?: Record<string, {  // named compound aggregates
    fn: string
    field?: string
    format?: 'compact'
    where?: { field: string; op: string; value: unknown }
  }>
  map?: Record<string, string>   // map results to component props
}
```

### Single aggregate

```json
{"dataSource": {"source": "orders", "aggregate": {"fn": "sum", "field": "total", "format": "compact"}, "map": {"text": "{{$value}} total"}}}
```

### Compound aggregates with where clauses

```json
{"dataSource": {"source": "runs", "aggregates": {"$pass": {"fn": "count", "where": {"field": "status", "op": "eq", "value": "pass"}}, "$fail": {"fn": "count", "where": {"field": "status", "op": "eq", "value": "fail"}}}, "map": {"text": "✓ {{$pass}} / ✗ {{$fail}}"}}}
```

### Map syntax

- `{"text": "{{$value}}"}` — single aggregate result
- `{"text": "{{$total}} ({{$pending}} pending)"}` — compound aggregate interpolation
- Compact formatting: 1234 → "1.2K", 1234567 → "1.2M"

## Repeat Templates

The Repeat component renders a template per data source row using `{{field}}` placeholders.

### Transforms

Apply transforms with pipe syntax `{{field | transformName}}`:

| Transform | Description |
|-----------|-------------|
| `percentOfMax` | Value as percentage of the max value for that field across all rows |

```json
{"Repeat": {"dataSource": {"source": "scores"}, "transforms": {"percentOfMax": {"fn": "percentOfMax"}}, "template": {"ProgressBar": {"label": "{{name}}", "value": "{{score | percentOfMax}}"}}}}
```

## Complete Dashboard Example

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":["title","filter","stats","table"]}}},{"id":"title","component":{"Text":{"text":"Agent Dashboard","usageHint":"h2"}}},{"id":"filter","component":{"MultiSelect":{"options":[{"label":"main","value":"main"},{"label":"dev","value":"dev"}],"selected":["main","dev"],"bind":{"source":"agents","field":"name","op":"in","nullValue":["main","dev"]}}}},{"id":"stats","component":{"Row":{"children":["count-badge","token-badge"]}}},{"id":"count-badge","component":{"Badge":{"variant":"info","dataSource":{"source":"agents","aggregate":{"fn":"count"},"map":{"text":"{{$value}} agents"}}}}},{"id":"token-badge","component":{"Badge":{"variant":"success","dataSource":{"source":"agents","aggregate":{"fn":"sum","field":"tokens","format":"compact"},"map":{"text":"{{$value}} tokens"}}}}},{"id":"table","component":{"Table":{"dataSource":{"source":"agents","columns":["name","tokens","status"]},"sortable":true}}}]}}
{"dataSourcePush":{"surfaceId":"main","sources":{"agents":{"fields":["name","tokens","status"],"rows":[{"name":"main","tokens":32300,"status":"idle"},{"name":"dev","tokens":6800,"status":"active"}],"primaryKey":"name"}}}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
```
