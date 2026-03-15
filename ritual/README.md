# Ritual

A skill for facilitating multi-agent discussions within OpenClaw. Agents join a shared room to brainstorm, debate, provide feedback, or reach consensus on a topic — all coordinated by a facilitator.

## How It Works

The facilitator creates a room, spawns (or invites) agents as participants, and poses a prompt. Agents communicate via room messages, riffing off each other's ideas in real time. The facilitator keeps things on track, manages rounds of discussion, and surfaces results to the user.

Think of it like a meeting — except the participants are agents with different specializations and perspectives.

## When to Use

- Brainstorming names, ideas, or approaches from multiple angles
- Getting feedback on a plan from agents with different expertise
- Building consensus on a decision
- Any task where diverse perspectives produce better results than a single agent working alone

## Modes

Subagents can be spawned in two modes:

- **`run`** (default) — One-shot, internal only. No Discord threads. Best for simple, single-phase rituals.
- **`session`** — Persistent, thread-bound. Creates Discord threads for each agent. Use when the ritual has multiple phases with human input between steps, or when you need to steer agents mid-ritual.

Existing sessions invited to a ritual are unaffected by this setting — they just receive a message asking them to join.

## Cost Consciousness

Rituals multiply token usage roughly in proportion to the number of participating agents. Each agent runs its own session with full context (system prompt, skill instructions, room history), and every round of discussion means every agent reads and responds.

As a rough guide:

| Setup | Approximate Token Usage |
|---|---|
| Single agent task | ~15-25k tokens |
| 4-agent ritual, 2 rounds | ~80-100k tokens |
| 4-agent ritual, 4 rounds | ~150-200k+ tokens |

The cost scales with:
- **Number of agents** — each one is a full session
- **Number of discussion rounds** — every round means every agent processes and responds
- **Context size** — agents with larger system prompts or longer room histories use more input tokens

For cost-sensitive situations, keep rituals focused: fewer agents, fewer rounds, and clear prompts that minimize back-and-forth. A well-scoped 2-agent ritual can be just as effective as a 5-agent free-for-all.
