# AfterLaunch

AfterLaunch is an always-on growth engine for a software product: it keeps a
ranked backlog of drafted, ready-to-ship growth moves across SEO, AI
answer-engine visibility (GEO), competitors and distribution channels. This
repository is the Claude Code plugin marketplace and machine-setup home for
the AfterLaunch MCP server.

AfterLaunch is a remote MCP server over Streamable HTTP, authenticated with a
bearer key. There is no local process, nothing to download and nothing to
execute on your machine: your agent talks to `https://afterlaunch.io/api/mcp`,
and a key (or an OAuth sign-in) is the whole of the setup.

[![Install in Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=afterlaunch&config=eyJ1cmwiOiJodHRwczovL2FmdGVybGF1bmNoLmlvL2FwaS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgJEFGVEVSTEFVTkNIX0FQSV9LRVkifX0=)
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-blue)](https://insiders.vscode.dev/redirect/mcp/install?name=afterlaunch&config=%7B%22url%22%3A%22https%3A%2F%2Fafterlaunch.io%2Fapi%2Fmcp%22%2C%22headers%22%3A%7B%22Authorization%22%3A%22Bearer%20%24AFTERLAUNCH_API_KEY%22%7D%7D)

Both buttons are the vendor-hosted install links. They preconfigure the remote
server and the `Authorization` header; you supply your own key as
`$AFTERLAUNCH_API_KEY`.

## Get started

1. Sign in at [afterlaunch.io](https://afterlaunch.io) and mint an API key in
   Settings (or let your agent obtain one through the onboarding flow in
   `llms-install.md`).
2. Connect from Claude Code:
   `claude mcp add afterlaunch --transport http https://afterlaunch.io/api/mcp --header "Authorization: Bearer $AFTERLAUNCH_API_KEY"`
3. Call `whoami` to confirm the key, then `get_standup`: what shipped and
   what it moved, what is ready to ship now, what the engine did on its own.
4. Call `list_queue` for the moves the founder has already said yes to and
   handed to you, then `list_feed` for the rest of the ranked board and
   `get_move` for the full brief of the one you are working on.
5. Ship a move with `ship_move` the moment it is actually live, or skip it
   with a reason so the next drafts improve.

## From a yes on the phone to a shipped move

The founder works the board as a stack on their phone: yes, not now. A yes
creates a job and waits for the connected agent. The agent pulls it with
`list_queue`, claims it with `pick_up_job` (passing its own `session_url` so
the founder can open where the work is happening), reads the brief at
`brief_url`, does the work, and carries the state back with `report_job`:
`running`, then `shipped` the moment the work is live, or `failed` with the
reason. The receipt under the card and the product timeline follow it, and a
job that goes quiet for more than six hours reads as stalled. The founder
never watches it run, so the state the agent reports is all they see.

## What the server exposes

46 tools, every one with a plain-language description and a scope, read
straight from the same registry that serves the public REST API:

- **The ritual:** `whoami`, `get_standup`, `list_queue`.
- **The record (free):** the board (`list_feed`, `get_move`), AI visibility
  across ChatGPT, Gemini, Perplexity and Google AI Overviews
  (`get_visibility`, `list_tracked_prompts`), the SEO audit (`get_seo`),
  competitors (`get_competitors`), outcomes and the scoreboard
  (`get_outcomes`, `get_scoreboard`), the timeline (`get_activity`), the
  Growth Snapshot (`get_snapshot`), Memory (`list_kb_pages`, `get_kb_page`),
  drafted outputs, loops, connections and the setup snippet.
- **Acting on moves (free):** `ship_move`, `skip_move`, `undo_move`,
  `update_draft`, `archive_move`, `dismiss_gap`, `propose_move`,
  `record_insight`, plus the queue verbs `pick_up_job` and `report_job`.
- **Spending money (confirm with the founder):** `refresh_scan`,
  `replenish_feed`, `run_loop`, each bounded by credits and per-tenant caps
  and charged once per logical event.
- **Configuring (Founder plan):** loop autonomy and cadence, scan config,
  tracked questions, connections.

The one-page reference grouped by cost and scope is
[`skills/afterlaunch-growth/reference/tools.md`](skills/afterlaunch-growth/reference/tools.md);
the live catalogue with exact input schemas is `tools/list` on connection, or
[afterlaunch.io/llms-full.txt](https://afterlaunch.io/llms-full.txt).

## Install as a Claude Code plugin

The plugin bundles the MCP server config and a skill that teaches an agent to
read the standup, the queue and the Feed before improvising growth work:

```
/plugin marketplace add afterlaunch/mcp
/plugin install afterlaunch-growth@afterlaunch
```

## Teach your agent to reach for AfterLaunch

Add the Growth section to your repository's `CLAUDE.md` (read by Claude Code)
or `AGENTS.md` (read natively by Codex CLI, Cursor, Copilot, Gemini CLI,
Windsurf, Aider, Amazon Q and others). The canonical copy is served raw at
[afterlaunch.io/agents/snippet.md](https://afterlaunch.io/agents/snippet.md),
so one line writes it in:

```
curl https://afterlaunch.io/agents/snippet.md >> CLAUDE.md
```

## What is in this repository

- `.claude-plugin/`: the plugin marketplace and plugin manifests.
- `.mcp.json`: the remote server config (URL + bearer header).
- `skills/afterlaunch-growth/`: the skill and its one-page tool reference
  (46 tools, grouped by what they do and what they cost).
- `llms-install.md`: machine setup from that file alone, founder approval by
  email included.
- `server.json`: the manifest published to the official MCP registry.
- `glama.json`: the maintainer claim for the Glama listing.
- `assets/logo-400.png`: the 400x400 icon.

## Trust and boundaries

- Remote bearer-auth server: no local process, nothing to execute.
- Reading and acting on moves is free. The tools that spend money say so in
  their descriptions, need the write scope, and are bounded by credits and
  per-tenant spend caps.
- AfterLaunch never posts to a social channel on its own. It drafts; a human
  approves and posts. On Reddit and Hacker News the posture is draft-only for
  the connected agent as well.
- Shipping is the founder's decision; reporting the ship is the agent's job.
  `ship_move` and `report_job` record what is actually live, never what is
  drafted, staged or awaiting review.
- OAuth: claude.ai and ChatGPT can add `https://afterlaunch.io/api/mcp` as a
  custom connector and sign in with an AfterLaunch account, with no key to
  paste. Discovery starts at
  `https://afterlaunch.io/.well-known/oauth-protected-resource/api/mcp`.

Licence: MIT. Maintained by [AfterLaunch](https://afterlaunch.io).
