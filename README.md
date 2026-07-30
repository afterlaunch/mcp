# AfterLaunch

AfterLaunch is an always-on growth engine for a software product: it keeps a
ranked backlog of drafted, ready-to-ship growth moves across SEO, AI
answer-engine visibility (GEO), competitors and distribution channels. This
repository is the Claude Code plugin marketplace and machine-setup home for
the AfterLaunch MCP server.

AfterLaunch is a remote MCP server over Streamable HTTP, authenticated with a
bearer key. There is no local process, nothing to download and nothing to
execute on your machine: your agent talks to `https://afterlaunch.io/api/mcp`
and the key is the only credential involved.

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
3. Call `whoami` to confirm the key.
4. Call `list_feed` to read the ranked backlog of prepared growth moves.
5. Ship a move with `ship_move`, or skip it with a reason so the next drafts
   improve.

## Install as a Claude Code plugin

The plugin bundles the MCP server config and a skill that teaches an agent to
read the Feed before improvising growth work:

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
- `skills/afterlaunch-growth/`: the skill and its one-page tool reference.
- `llms-install.md`: machine setup from that file alone, founder approval by
  email included.
- `server.json`: the manifest published to the official MCP registry.
- `assets/logo-400.png`: the 400x400 icon.

## Trust and boundaries

- Remote bearer-auth server: no local process, nothing to execute.
- Reading and acting on moves is free. The tools that spend money say so in
  their descriptions, need the write scope, and are bounded by credits and
  per-tenant spend caps.
- AfterLaunch never posts to a social channel on its own. It drafts; a human
  approves and posts.

Licence: MIT. Maintained by [AfterLaunch](https://afterlaunch.io).
