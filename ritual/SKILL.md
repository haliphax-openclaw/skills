---
name: ritual
description: Facilitates an isolated meeting, or "ritual" between multiple agents or subagents in order to brainstorm, provide feedback, execute concurrent work related to the same task, reach consensus, etc.
---

# Ritual

## Overview

Facilitates an isolated meeting, or "ritual" between multiple agents or subagents in order to brainstorm, provide feedback, execute concurrent work related to the same task, reach consensus, etc. The ritual discussion takes place simultaneously using available `rooms` extension tools.

## Requirements

The `rooms` extension must be installed. See [rooms](https://github.com/haliphax-openclaw/extensions/tree/main/rooms).

## When to Use

When multiple agents need to communicate in the same shared context to brainstorm, provide feedback, execute concurrent work related to the same task/project, reach consensus, etc.

## Workflow

### Step 1: Accept Input

- `id` - The unique identifier of the room ID so that it can be isolated from other rituals. If no ID is provided, one should be chosen by the agent handling the request to initiate a ritual.
- `facilitator` - The agent ID of the agent responsible for facilitating the ritual. This agent can be a member of the ritual as well, but that is not required. The facilitator steers the conversation to remain on topic and surfaces any necessary information or requests to the user. The facilitator should provide regular status updates as to the progress of the ritual, since the user will not be able to see the discussion taking place. If no facilitator is provided, the current agent should assume the role. If an agent ID is provided, a new subagent for that agent ID should be spun up specifically for the ritual. If provided with an existing session ID, connect the live session's agent to the ritual as the facilitator.
- `members` - A list of agents or subagents that will be added to the ritual and expected to participate in the discussion. Existing session IDs can be provided to include current sessions' agents; otherwise, new subagents of the specified agent IDs will be spun up specifically for the ritual.
- `mode` - The spawn mode for subagents created for the ritual. Defaults to `run` (one-shot, internal only — no Discord threads created). Set to `session` for multi-phase rituals that require human input between steps (requires `thread: true` on spawn, which creates Discord threads). Use `run` for simple, single-phase rituals. Use `session` when the facilitator needs to steer agents between phases via `sessions_send` or `subagents(action=steer)`.
- `purpose` - The reason for the ritual. This could be a topic to brainstorm, an issue to troubleshoot, a concept to research, a request for concensus on a decision, or any other topic that would require coordination between multiple entities.

### Step 2: Setup the Room

- If the `facilitator` is not the agent handling the request, then the agent handling the request should hand this process off to the facilitator and step back
- If no `id` was provided, the `facilitator` should generate one
- The `facilitator` should join a new room with the appropriate ID (this will create the room if it doesn't exist)
- If `members` includes subagents, the `facilitator` should spawn any requested subagents using the specified `mode` (default `run`). If `mode` is `session`, pass `thread: true` on the spawn call. Include instructions to read this skill document and await the ritual prompt
- If `members` includes live agents, the `facilitator` should message those agents' sessions with instructions to read this skill document and await the ritual prompt

### Step 3: Perform the Ritual

- Once all ritual members have announced themselves in the room, the `facilitator` should provide them with the ritual prompt
- When the ritual prompt has been received, `members` should begin the discussion requested by the ritual prompt, following instructions from the `facilitator` when provided
- If the `facilitator` is included in `members`, they should participate in the ritual discussion as well as facilitate it
- The `facilitator` should help keep the conversation on track, settle disputes, and regularly surface information about the ritual's progress to the user

### Step 4: Conclude the Ritual

- If a stalemate has been reached or the conversation is carrying on too long, the `facilitator` should request guidance from the user
- When the conversation has concluded (either from consensus or at the user's request), the `facilitator` should provide a summary of the ritual to the user and instruct all `members` to leave the room

## Tool Reference

### Room Tools

These are the core communication tools for the ritual.

- `room_join` — Join a named room (creates it if it doesn't exist). Used by the facilitator and all members during setup.
- `room_send` — Broadcast a message to all other members in the room. Primary communication method during the ritual.
- `room_recv` — Receive pending messages from the room. Members should poll this to read what others have said.
- `room_list` — List rooms you belong to, or list members of a specific room. Useful for the facilitator to verify all members have joined.
- `room_leave` — Leave the room. Used by all participants when the ritual concludes.

### Session Management

These tools handle spawning, messaging, and managing the agents involved.

- `sessions_spawn` — Spawn a new subagent for a given agent ID. Used when `members` or `facilitator` specifies an agent ID rather than an existing session.
- `sessions_send` — Send a message to an existing session. Used when `members` or `facilitator` references a live session ID.
- `sessions_list` — List active sessions. Useful for resolving session references or verifying agent availability.
- `subagents` (list/steer/kill) — Manage subagents spawned for the ritual. The facilitator can steer participants back on track or kill subagents when the ritual concludes.
