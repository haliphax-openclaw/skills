---

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
name: canvas

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
description: Interact with the OpenClaw Canvas web server for visual UI surfaces. Use when pushing A2UI JSONL dashboards, serving static HTML/CSS/JS files, querying canvas state from the SQLite cache, or switching between iframe and A2UI rendering modes. Covers session-scoped canvas URLs, static file storage, JSONL persistence, and all available A2UI components.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
---

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
# Canvas Web Server

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
The Canvas web server ([haliphax-openclaw/openclaw-canvas-web](https://github.com/haliphax-openclaw/openclaw-canvas-web)) registers as a node with the OpenClaw gateway and serves two types of content per agent session:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
1. **Static files** (iframe mode) — HTML/CSS/JS served from the agent's workspace

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
2. **A2UI surfaces** (component mode) — Declarative UI pushed via JSONL commands

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Requirements

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- `jq` binary available on the system (for encoding JSONL payloads)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- `sqlite3` binary available on the system (for querying A2UI surface state)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- OpenClaw Canvas web server running and connected to the gateway (appears as "Canvas Web Server" in `openclaw nodes status`)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Required Configuration

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Store the following in your `TOOLS.md` file:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```markdown

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Canvas

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Canvas Base URL:** <base-url>  (e.g. https://example.com/canvas)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Ask your human for the canvas base URL if you don't have it. All canvas session URLs are derived from this value.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Your Canvas Session

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Each agent has a personal canvas session URL:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
<CANVAS_BASE_URL>/session/<agent-id>/

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
The session name matches your agent ID. All A2UI pushes and static files are scoped to this session.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Static File Storage

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Static canvas files live in your workspace's `canvas/` directory:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
~/.openclaw/workspaces/<agent-id>/canvas/

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
The server maps agent IDs to workspace canvas directories and serves files at `/_c/<session>/<path>`.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### File organization

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Long-lived JSONL files** — Store in `canvas/jsonl/` for dashboards and surfaces you want to persist and re-push across sessions

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Temporary JSONL files** — Store in `canvas/tmp/` for short-lived session work, experiments, and one-off surfaces

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
> **Note:** The `jsonl/` and `tmp/` subdirectories are ignored by the file watcher by default. Files placed there won't trigger iframe reloads. This is configurable via the `OPENCLAW_CANVAS_IGNORE_DIRS` environment variable.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
~/.openclaw/workspaces/<agent-id>/canvas/

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
├── index.html               # static HTML served via iframe

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
├── jsonl/

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
│   └── dashboard.jsonl      # persistent dashboard definition

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
├── tmp/

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
│   ├── debug-surface.jsonl  # temporary experiment

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
│   └── test-layout.jsonl    # one-off layout test

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Pushing A2UI Surfaces

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Use `openclaw nodes invoke` to push JSONL content to your canvas session. The `session` parameter is required to scope the push to your canvas URL.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```bash

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
# Build the payload and push

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
PAYLOAD=$(cat canvas/dashboard.jsonl | jq -Rs '.')

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
openclaw nodes invoke \

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
  --node "Canvas Web Server" \

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
  --command "canvas.a2ui.pushJSONL" \

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
  --params "{\"session\":\"<agent-id>\",\"payload\":$PAYLOAD}"

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Without `session`, the push defaults to `main` and renders on the main agent's canvas.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### Incremental updates

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Push only the components that changed — the server merges by component ID:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```bash

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
echo '{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"my-badge","component":{"Badge":{"text":"Updated","variant":"success"}}}]}}' > /tmp/update.jsonl

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
PAYLOAD=$(cat /tmp/update.jsonl | jq -Rs '.')

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.a2ui.pushJSONL" \

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
  --params "{\"session\":\"<agent-id>\",\"payload\":$PAYLOAD}"

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### Other canvas commands

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Command | Description |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
|---------|-------------|

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.present` | Show the canvas panel |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.hide` | Hide the canvas panel |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.navigate` | Navigate to a path or URL |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.eval` | Execute JavaScript in the canvas |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.snapshot` | Capture a screenshot |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.a2ui.push` | Push A2UI JSONL (alias for pushJSONL) |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.a2ui.pushJSONL` | Push A2UI JSONL payload |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `canvas.a2ui.reset` | Clear all A2UI surfaces (pass `session` to clear one session) |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Switching Between Iframe and A2UI

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
The canvas view auto-switches based on content:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **A2UI mode** activates when a surface has a `root` set (via `beginRendering`) and no static file subpath is in the URL

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Iframe mode** activates when navigating to a static file path (e.g., `/session/<agent-id>/index.html`)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
To force iframe mode, navigate to a specific file. To force A2UI mode, push a surface with `beginRendering`.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
To clear A2UI and return to iframe:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```bash

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
openclaw nodes invoke --node "Canvas Web Server" --command "canvas.a2ui.reset" \

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
  --params "{\"session\":\"<agent-id>\"}"

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Querying State from SQLite

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
A2UI surface state is persisted in a SQLite cache at:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
~/.openclaw-canvas/a2ui-cache.db

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Table: `a2ui_surfaces`

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Column | Type | Description |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
|--------|------|-------------|

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `surfaceId` | TEXT (PK) | Surface identifier |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `components` | TEXT (JSON) | Component map `{ id: component }` |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `root` | TEXT | Root component ID |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `dataModel` | TEXT (JSON) | Data model including `$sources` |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Query examples:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```bash

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
# List all surfaces

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT surfaceId, root FROM a2ui_surfaces"

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
# Dump a surface's components

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT components FROM a2ui_surfaces WHERE surfaceId='main'" | jq .

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
# Check data sources

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
sqlite3 ~/.openclaw-canvas/a2ui-cache.db "SELECT json_extract(dataModel, '$.\$sources') FROM a2ui_surfaces WHERE surfaceId='main'" | jq .

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## JSONL Command Reference

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
Every A2UI push is a newline-delimited sequence of JSON commands:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Command | Purpose |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
|---------|---------|

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `surfaceUpdate` | Create or update components on a surface |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `beginRendering` | Set the root component and activate A2UI rendering |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `dataModelUpdate` | Update the data model (use `$sources` key for data sources) |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `dataSourcePush` | Shorthand for pushing data sources without `$sources` nesting |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| `deleteSurface` | Remove a surface |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### Minimal surface

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```jsonl

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":["hello"]}}},{"id":"hello","component":{"Text":{"text":"Hello from Canvas","usageHint":"h1"}}}]}}

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
{"beginRendering":{"surfaceId":"main","root":"root"}}

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
```

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
## Components and Reactive Data Binding

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
For the full list of available A2UI components, their JSONL schemas, and use cases, see:

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- [references/components.md](references/components.md) — Full component reference (layout, containers, display, inputs)

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- [references/reactive.md](references/reactive.md) — Data sources, filtering, aggregates, and Repeat templates

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- [references/deep-linking.md](references/deep-linking.md) — `openclaw://` URL scheme for triggering agent runs from canvas content

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### Component summary

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Category | Components |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
|----------|-----------|

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Layout | Column, Row, Stack, Spacer, Divider |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Containers | Accordion (collapsible panels), Tabs (switchable tabbed panels) |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Display | Text, Badge, Image, ProgressBar, Table, Repeat |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
| Input | Button, Checkbox, Select, MultiSelect, Slider |

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
### Key features

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).


> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Sorting** — Table and Repeat support optional `sortable` prop. Tables sort by clicking column headers (⬆/⬇); Repeat includes a sort direction dropdown.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Filtering** — Select and MultiSelect bind to data sources for reactive filtering. Clearing a MultiSelect shows all data (empty selection = no filter).

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Reactive props** — Accordion `expanded` and Tabs `active` props react to surface updates, allowing agents to programmatically toggle panels or switch tabs.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
- **Deep linking** — HTML content can include `openclaw://` links that trigger agent runs via a confirmation dialog.

> **Important:** The OpenClaw gateway must have access to the SQLite database file. If the canvas web server and gateway run on separate hosts, ensure the database is accessible via a shared filesystem (NFS mount, Docker volume, bind mount, etc.).
