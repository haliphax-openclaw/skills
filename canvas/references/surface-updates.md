# Pushing Component & Surface Updates

Use `surfaceUpdate` to create or modify the component tree on an A2UI surface. This is for structural changes — layout, new components, filter options, component properties.

## When to use
- Creating a new surface from scratch
- Adding, removing, or rearranging components
- Changing component properties (filter options, labels, bindings)
- Changing the root component

## JSONL Commands

### `surfaceUpdate`

Create or update components on a surface. Components are merged by ID — only include components you're changing.

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":["hello"]}}},{"id":"hello","component":{"Text":{"text":"Hello from Canvas","usageHint":"h1"}}}]}}
```

### `beginRendering`

Set the root component and activate A2UI rendering. Required once when creating a new surface.

```jsonl
{"beginRendering":{"surfaceId":"main","root":"root"}}
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
mcporter call canvas-web.canvas_push session=<agent-id> payload='{"surfaceUpdate":{...}}'
```

### Incremental updates

Push only the components that changed — the server merges by component ID:

```bash
mcporter call canvas-web.canvas_push session=<agent-id> \
  payload='{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"my-badge","component":{"Badge":{"text":"Updated","variant":"success"}}}]}}'
```

Unchanged components are preserved. Do not re-push the entire surface when only a few components need updating.

## Minimal new surface

A complete surface needs at minimum a `surfaceUpdate` followed by `beginRendering`:

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":["hello"]}}},{"id":"hello","component":{"Text":{"text":"Hello from Canvas","usageHint":"h1"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
```

## Component reference

See [components.md](components.md) for the full list of available components, their JSONL schemas, and props.
