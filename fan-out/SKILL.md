---
name: fan-out
description: Fan out a list of tasks to subagents with unified tracking and status updates.
---

# Fan-Out

## Overview

This skill distributes work across multiple subagents with unified status tracking. It creates a to-do list, spawns subagents, maintains a live discussion post of task status, steers subagents when they encounter known issues, and summarizes outputs when complete. Subagents can be spawned asynchronously to complete tasks in parallel.

## When to Use

- User provides multiple tasks ("help me do X, Y, and Z")
- A to-do list exists and each item should become an independent subagent
- Long-running tasks benefit from parallel execution rather than sequential
- Need unified tracking and summary of multiple workers

## Workflow

### Step 1: Accept Input

- `tasks`: Bullet list or comma-separated list of task descriptions
- `async`: Whether the tasks should be completed asynchronously (parallel subagents)

For item names in the to-do list, use the task content directly.

### Step 2: Create To-Do List

For the list ID:
- Use current `agentId` if working on agent-specific tasks
- Generate a project slug based on task content
- Create new list with descriptive slug

For the list name:
- Use a short description of the project

**Create new list:**
```
mcporter call todo.todo_list_create key=<list_id> name="<name>"
```

**Add items:**
```
mcporter call todo.todo_item_add key=<list_id> content="<task description>"
```

Each item returns a unique `item_id` for tracking.

### Step 3: Spawn Subagents Asynchronously

For each to-do item, spawn a subagent using `sessions_spawn`:

```
sessions_spawn(
  task="<task description>",
  label="fanout-<list_id>-<item_short_id>",
  runtime="subagent",
  mode="run",
  cleanup="keep"  # Keep for status polling
)
```

**Key settings:**
- `runtime="subagent"` - Spawns isolated subagent session
- `mode="run"` - One-shot execution
- `cleanup="keep"` - Retain session for status checks
- `label` - Trackable identifier for steering/polling

Store mapping: `item_id` → `session_key`

### Step 4: Maintain Live Status Post

Post the initial status to a single message, then **edit that same message in-place** as tasks progress. Do not add new messages for each update—edit the original to keep the channel clean. When a task completes, the status post reflecting this is enough. Save additional output for the summary.

Track:
- All tasks and their current status (pending/running/completed/failed)
- Elapsed time for each task
- Errors or blockers encountered

Format as a list with emoji for status:
```
**Fan-Out Status: some-list-id**

- 🕰️ task-id-1 (1m13s)
- ⚡️ task-id-2 (15s)
- ❌ task-id-3 (5m3s)
- ✅ task-id-4 (8s)
- 🚫 task-id-5 (10m)
```

Emoji key:
- 🕰️ pending (not started)
- ⚡️ running
- 🚫 canceled
- ❌ failed
- ✅ succeeded

Edit this same message periodically as subagents progress.

### Step 5: Poll and Steer Subagents

**Poll status:**
```
subagents(action="list", recentMinutes=10)
```

For each subagent, check:
- Is it still running?
- Did it encounter a known issue the parent agent can help with?
- Has it exceeded expected time?

**Steering:**
If a subagent is blocked on something the parent agent has context for:

```
subagents(
  action="steer",
  target="<session_key>",
  message="<guidance based on parent agent context>"
)
```

Examples:
- "Use the todo MCP server: `mcporter call todo.todo_list_create key=...`"
- "The repo is at /path/to/repo - don't re-clone it"
- "Credentials are in env vars, not in code"

### Step 6: Aggregate Results

When all subagents complete (or are killed for inactivity):

1. **Collect outputs:**
   - Poll each session for final status
   - Fetch session history if needed

2. **Summarize:**
   - Group by status (success/failed/canceled/timeout)
   - Include individual task durations and total duration
   - Extract key outputs from each
   - Note any patterns or common blockers

3. **Final report:**
   ```
   **Fan-Out Complete: <list_id>**

   **✅ Succeeded (<n>):**
   - <task> (<duration>): <result summary>

   **❌ Failed (<n>):**
   - <task> (<duration>): <error>

   **🚫 Canceled (<n>):**
   - <task> (<duration>): <reason>

   **Total Duration:** <time>
   ```

## Example Usage

Tasks to fan out:
- Fix bug in auth module
- Update README
- Run tests

**Execution flow:**
1. Create list (agent generates name)
2. Spawn subagents for each task (in parallel if `async` is requested)
3. Post initial status to channel
4. Poll every 5-10s for updates
5. If subagent encounters issues, steer it with context
6. When all complete, post summary

## Key Commands Reference

| Action | Command |
|--------|---------|
| Create list | `mcporter call todo.todo_list_create key=<id> name=<name>` |
| Add items | `mcporter call todo.todo_item_add key=<id> content="..."` |
| Spawn subagent | `sessions_spawn(task="...", runtime="subagent", cleanup="keep")` |
| List subagents | `subagents(action="list", recentMinutes=10)` |
| Steer subagent | `subagents(action="steer", target="<key>", message="...")` |
| Kill subagent | `subagents(action="kill", target="<key>")` |
| Get session history | `sessions_history(sessionKey="<key>")` |
| Update todo status | `mcporter call todo.todo_item_update key=<list_id> item_id=<item_id> status=<status>` |

Note: You may need to supply additional arguments to `mcporter` (such as `--config` to specify the configuration file path).

## Best Practices

- Use descriptive list_id that links to project/task
- Keep task descriptions clear and actionable
- Set reasonable cleanup="keep" for status tracking
- Execute tasks in parallel whenever possible to save time
- Poll every 5-10s for updates
- Edit status post in-place—never add new messages for updates
- Steer proactively when you see common blockers
- Always aggregate results at the end
