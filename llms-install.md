# Install AfterLaunch from this file alone

This file is the agent-onboarding acceptance test: an agent should be able to
set AfterLaunch up end to end from this file, with the founder approving by
email and no browser session required. There is no package to install and no
local process to run; AfterLaunch is a remote MCP server over Streamable HTTP,
authenticated with a bearer key.

## 1. Add the MCP server

```
claude mcp add afterlaunch --transport http https://afterlaunch.io/api/mcp --header "Authorization: Bearer $AFTERLAUNCH_API_KEY"
```

Any MCP client that supports a remote Streamable HTTP server with an
`Authorization: Bearer` header works. The generic config is:

```json
{
  "url": "https://afterlaunch.io/api/mcp",
  "headers": { "Authorization": "Bearer $AFTERLAUNCH_API_KEY" }
}
```

## 2. If there is no key yet, run onboarding

Read `https://afterlaunch.io/llms.txt`, then:

1. POST `https://afterlaunch.io/api/v1/onboard/start` with
   `{ "url": "<the product's URL>", "email": "<the founder's email>",
   "agent_label": "<your name>" }`.
2. Poll `https://afterlaunch.io/api/v1/onboard/poll` with the returned device
   code until the founder approves.

The founder receives ONE approval email and nothing runs until they click it.
Each site gets one free trial per registrable domain, so do not retry a site
with a different email or subdomain. If onboarding refuses, the founder can sign
in at `https://afterlaunch.io` and mint a key from Settings.

## 3. Confirm it works

Call `whoami`. It returns the product run the key is bound to, the tier and the
scopes. If it succeeds, the install is complete.

## 4. What to do next

Read `skills/afterlaunch-growth/SKILL.md` in this repository. It teaches the
loop: confirm with `whoami`, open the session with `get_standup`, pull the
moves the founder has already said yes to with `list_queue` (claim each with
`pick_up_job`, report with `report_job`), read the board with `list_feed` and
`get_move` before improvising, act on moves with `ship_move` / `skip_move` /
`undo_move` / `update_draft` / `archive_move`, write what you learn back with
`record_insight`, and confirm with the founder before any tool that spends
money (`refresh_scan`, `replenish_feed`, `run_loop`).
