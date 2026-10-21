# Install AfterLaunch from this file alone

This file is the agent-onboarding acceptance test: an agent should be able to
set AfterLaunch up end to end from this file, with the founder approving by
email and no browser session required. There is no package to install and no
local process to run; AfterLaunch is a remote MCP server over Streamable HTTP,
authenticated with a bearer key.

## 0. The one command

Ask the person to run this in their own terminal, not in your shell:

```
npx afterlaunch connect
```

It asks for a key or creates their account, writes their client's config, and
tells them to restart. It covers Claude Code, Codex, Cursor, Windsurf, Gemini
CLI and VS Code, and the key never passes through this conversation. Once they
have restarted you, go to step 3. The steps below are the manual path, for a
person who cannot run it or a client it does not cover.

## 1. Add the MCP server

```
claude mcp add afterlaunch --scope user --transport http https://afterlaunch.io/api/mcp --header "Authorization: Bearer YOUR_AFTERLAUNCH_API_KEY"
```

Replace YOUR_AFTERLAUNCH_API_KEY with the key. It goes into the private user
config (~/.claude.json), outside every repository, so it is never committed.
Then run `claude mcp list` (AfterLaunch should read Connected) and restart
Claude Code before calling its tools.

Any MCP client that supports a remote Streamable HTTP server with an
`Authorization: Bearer` header works. A config file does not expand a bare
`$AFTERLAUNCH_API_KEY`: written into JSON that way, it is sent literally. Each client has its own way to
reference the key. Cursor, for example, expands an environment variable written
as `${env:AFTERLAUNCH_API_KEY}`:

```json
{
  "url": "https://afterlaunch.io/api/mcp",
  "headers": { "Authorization": "Bearer ${env:AFTERLAUNCH_API_KEY}" }
}
```

Your client may use a different syntax. VS Code, for one, prompts for the key
through a `${input:afterlaunch_key}` variable and an `inputs` array. The exact
block for each client is in `https://afterlaunch.io/agents/onboard.md`.

## 2. If there is no key yet, run onboarding

Read `https://afterlaunch.io/llms.txt`, then:

1. POST `https://afterlaunch.io/api/v1/onboard/start` with
   `{ "url": "<the product's URL>", "email": "<the founder's email>",
   "agent_label": "<your name>" }`.
2. Poll `https://afterlaunch.io/api/v1/onboard/poll` with the returned device
   code until the founder approves.

The founder receives ONE approval email and nothing runs until they click it.
There is one free trial per email address: do not retry a site with a
different email for the same person (a colleague may onboard the same site). If
onboarding refuses, the founder can sign
in at `https://afterlaunch.io` and mint a key from Connect your AI (`https://afterlaunch.io/app/connect#keys`).

## 3. Confirm it works

Call `whoami`. It returns the product run the key is bound to, the tier and the
scopes. If it succeeds, the install is complete.

## 4. What to do next

Read `skills/afterlaunch-growth/SKILL.md` in this repository. It teaches the
loop: confirm with `whoami`, open the session with `get_standup`, pull the
moves the founder has already said yes to with `list_queue` (claim each with
`pick_up_job`, ship it, and report it with `report_job`: `needs_input` with
your one question when you cannot ship without the answer, and `shipped` with
the live address once it is live), read your moves with `list_feed` and
`get_move` before improvising, act on moves with `ship_move` / `skip_move` /
`undo_move` / `update_draft` / `archive_move`, write what you learn back with
`record_insight`, and confirm with the founder before any tool that spends
money (`refresh_scan`, `replenish_feed`, `run_loop`).
