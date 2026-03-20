# Pushing Component & Surface Updates

Use `updateComponents` to create or modify the component tree on an A2UI surface. This is for structural changes — layout, new components, filter options, component properties.

## When to use
- Creating a new surface from scratch
- Adding, removing, or rearranging components
- Changing component properties (filter options, labels, bindings)
- Changing the root component

## JSONL Commands

### `updateComponents`

Create or update components on a surface. Components are merged by ID — only include components you're changing. Each entry uses a flat shape: the component type is a string in `component`, and props are top-level siblings.

```jsonl
{"updateComponents":{"surfaceId":"main","components":[{"id":"root","component":"Column","children":["hello"]},{"id":"hello","component":"Text","text":"Hello from Canvas","variant":"h1"}]}}
```

### `createSurface`

Set the root component and activate A2UI rendering. Required once when creating a new surface.

```jsonl
{"createSurface":{"surfaceId":"main","root":"root"}}
```

### `deleteSurface`

Remove a surface entirely.

```jsonl
{"deleteSurface":{"surfaceId":"main"}}
```

## Pushing

```bash
# From a JSONL file (recommended — avoids shell escaping issues)
mcporter call canvas-web.canvas_push session=<agent-id> file=<path-to-file>

# Inline payload
mcporter call canvas-web.canvas_push session=<agent-id> payload='{"updateComponents":{...}}'
```

### Incremental updates

Push only the components that changed — the server merges by component ID:

```bash
mcporter call canvas-web.canvas_push session=<agent-id> \
  payload='{"updateComponents":{"surfaceId":"main","components":[{"id":"my-badge","component":"Badge","text":"Updated","variant":"success"}]}}'
```

Unchanged components are preserved. Do not re-push the entire surface when only a few components need updating.

## Minimal new surface

A complete surface needs at minimum an `updateComponents` followed by `createSurface`:

```jsonl
{"updateComponents":{"surfaceId":"main","components":[{"id":"root","component":"Column","children":["hello"]},{"id":"hello","component":"Text","text":"Hello from Canvas","variant":"h1"}]}}
{"createSurface":{"surfaceId":"main","root":"root"}}
```

## Component validation

When `updateComponents` is processed, each component is validated against the schema defined in its catalog's `catalog.json`. Validation checks required props, prop types, and flags unknown props.

- Components with **errors** (missing required props, type mismatches) are rejected and not applied
- Components with **warnings** (unknown props, unknown component types) are accepted
- Valid and invalid components can coexist in the same batch — valid ones are processed, invalid ones are skipped

The validation response includes `componentErrors` and `componentWarnings` arrays with per-component details.

## Component reference

See [components.md](components.md) for the full list of available components, their JSONL schemas, and props.
