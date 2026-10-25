# AfterLaunch MCP server

AfterLaunch watches how AI search and Google find your product, and hands you the next growth move with a draft ready. This repository is the home of its remote MCP server: connect Claude, ChatGPT, Claude Code, Codex or Cursor and your own AI can read the ranked moves, check AI visibility, take a move through to shipped and report it live.

- **Server URL:** `https://afterlaunch.io/api/mcp` (Streamable HTTP, nothing to install or run locally)
- **Tools:** 58 (see the list below)
- **Sign-in:** OAuth 2.0 for Claude and ChatGPT, or an API key for coding agents
- **Cost:** the free scan and the first 14 days cost nothing and need no card; then one plan, $149 a month
- **Licence:** MIT

[![Install in Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=afterlaunch&config=eyJ1cmwiOiJodHRwczovL2FmdGVybGF1bmNoLmlvL2FwaS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgJHtlbnY6QUZURVJMQVVOQ0hfQVBJX0tFWX0ifX0=)

The Cursor button opens Cursor's own confirmation screen with the server filled in. It reads your key from the `AFTERLAUNCH_API_KEY` environment variable, so no key is ever written into a link or a file.

## What an agent can do with it

- **Read the ranked growth moves.** `list_feed` returns the backlog across SEO, AI visibility, competitors and distribution. `get_move` opens one with its evidence, source material, instructions and a prepared draft.
- **Read AI visibility.** `get_visibility` shows how ChatGPT, Gemini, Perplexity and Google AI Overviews answer the customer questions you track, with share of voice, the sources they cite and the gaps where rivals are named and you are not. `get_seo`, `get_competitors` and `get_scoreboard` cover the rest of the record.
- **Take a move and ship it.** `accept_move`, `update_draft`, then `ship_move` once the work is live. Moves handed to the agent arrive through `list_queue`, `pick_up_job` and `report_job`.
- **Report it live.** `ship_move` records what is live and a receipt follows on the timeline. Later, `get_outcomes` and `get_scoreboard` show what it earned.

A good first session is two calls: `whoami` to confirm which product the key drives, then `get_standup` for what shipped, what is ready now and what the engine did on its own.

## Get started

Run this in your own terminal:

```
npx afterlaunch connect
```

It finds your client, takes your key or creates your account, writes the config and tells you to restart. It covers Claude Code, Codex, Cursor, Windsurf, Gemini CLI and VS Code, and the key never passes through a chat. The steps below are the manual path.

## Install the plugin

The plugin bundles the server config and three skills: `afterlaunch-growth`, which teaches the agent to read the standup, the queue and the Feed before improvising growth work, plus `roughen` and `findable` from [afterlaunch/skills](https://github.com/afterlaunch/skills). Create an API key first at [afterlaunch.io/app/connect#keys](https://afterlaunch.io/app/connect#keys), or run `npx afterlaunch connect`.

### Install in Claude Code

```
/plugin marketplace add afterlaunch/mcp
/plugin install afterlaunch-growth@afterlaunch
```

When you enable the plugin, Claude Code asks for your AfterLaunch API key. It masks the field and keeps the key in your system's secure credential store, not in a settings file, and sends it only as the bearer header to `https://afterlaunch.io/api/mcp`.

### Install in Cursor

Install AfterLaunch Growth from the Cursor Marketplace, then set `AFTERLAUNCH_API_KEY` under Plugins, Configure on the plugin. The plugin's `mcp.json` holds only the `${AFTERLAUNCH_API_KEY}` placeholder, never the key. To use the server without the plugin, use the install button above or the manual config under Cursor below.

For the manual configs below (Cursor and Codex), export the key in your shell before you open the client:

```sh
export AFTERLAUNCH_API_KEY=al_your_key_here
```

## Connect in one minute

You need a scanned product first. Run the free scan at [afterlaunch.io](https://afterlaunch.io), because connecting needs a scanned product. The server URL is the same everywhere:

```
https://afterlaunch.io/api/mcp
```

Never put a key in that URL, and never paste a key into a chat.

### Claude (web and mobile)

1. Open Customize, then Connectors, and add a custom connector.
2. Paste `https://afterlaunch.io/api/mcp` as the server URL and press Add.
3. Open AfterLaunch under Connectors, press Connect, and approve.

You sign in with your AfterLaunch account, so there is no key to create. Add it once on claude.ai and it is available in the mobile app. Free Claude plans allow one custom connector. On a Team or Enterprise plan an owner adds it once in organisation settings.

### ChatGPT

1. Open Settings, then Security and login, and turn on Developer mode.
2. In Plugins, press the plus button to create a developer-mode app.
3. Paste `https://afterlaunch.io/api/mcp` as the app's endpoint.
4. Choose OAuth for authentication and create the app.
5. Sign in to AfterLaunch and approve.

### Claude Code

Create an API key at [afterlaunch.io/app/connect#keys](https://afterlaunch.io/app/connect#keys), then run:

```sh
claude mcp add afterlaunch --scope user --transport http https://afterlaunch.io/api/mcp --header "Authorization: Bearer YOUR_AFTERLAUNCH_API_KEY"
```

Replace YOUR_AFTERLAUNCH_API_KEY with the key. It goes into your private user config (`~/.claude.json`), outside every repository, so it is never committed. Or [install the plugin](#install-in-claude-code), which asks for the key itself.

### Codex

```sh
codex mcp add afterlaunch --url https://afterlaunch.io/api/mcp --bearer-token-env-var AFTERLAUNCH_API_KEY
```

Codex reads the key from `AFTERLAUNCH_API_KEY` in your environment and sends it as a bearer header. The token never lands on disk.

### Cursor

Use the install button above, or add this to `.cursor/mcp.json` (per project) or `~/.cursor/mcp.json` (every project):

```json
{
  "mcpServers": {
    "afterlaunch": {
      "url": "https://afterlaunch.io/api/mcp",
      "headers": {
        "Authorization": "Bearer ${env:AFTERLAUNCH_API_KEY}"
      }
    }
  }
}
```

Cursor expands the placeholder from your shell, so set `AFTERLAUNCH_API_KEY` before you open the project.

### Other clients

The onboarding guide at [afterlaunch.io/agents/onboard.md](https://afterlaunch.io/agents/onboard.md) carries the exact command or config for VS Code, Windsurf, Gemini CLI and Cline too, and says which have been checked. It is written for an AI to read, so you can also just tell your agent to follow it. No account yet? An agent that can run commands can start one for you: it sends your site address and email, you approve one email, and the key is handed over once. The steps are in that same guide.

## Tools

58 tools, read from the product's action registry on 22 October 2026. The registry holds four more (`run_loop`, `set_loop_autonomy`, `set_loop_cadence`, `set_scan_config`), but they are listed only to an administrator account, so an ordinary connection does not see them. The live catalogue with exact input schemas is `tools/list` on connection, and the one-page reference in this repository is [`skills/afterlaunch-growth/reference/tools.md`](skills/afterlaunch-growth/reference/tools.md).

Scopes: 26 tools need `read`, 26 need `act`, 3 need `write` and 3 need `config`.

### Start a session

| Tool | Scope | What it does |
|---|---|---|
| `whoami` | read | Confirms the key works and shows which product it drives, its scopes, plan and trial end. |
| `get_standup` | read | One call: what shipped and what it moved, the top moves ready now, and what the engine did on its own. |
| `get_enrollment` | read | The product run summary: product URL, plan, trial end, time zone and delivery settings. |
| `get_setup_snippet` | read | The paste-ready growth section for a repository CLAUDE.md or AGENTS.md. |

### Read the ranked growth moves

| Tool | Scope | What it does |
|---|---|---|
| `list_feed` | read | The ranked backlog of prepared moves across SEO, AI visibility, competitors and distribution. |
| `get_move` | read | One move in full: evidence, source material, instructions and the prepared draft. |

### Read AI visibility, SEO and the record

| Tool | Scope | What it does |
|---|---|---|
| `get_visibility` | read | How ChatGPT, Gemini, Perplexity and Google AI Overviews answer the tracked questions: share of voice, cited sources, gaps, trend. |
| `list_tracked_prompts` | read | The customer questions every AI visibility reading is taken against (up to 50 on the Founder plan). |
| `get_seo` | read | The site-wide SEO audit: issue groups by severity, weekly score trend, page performance, links and authority. |
| `get_competitors` | read | The competitor roster with measured stats for you and each rival. |
| `get_snapshot` | read | The Growth Snapshot the run started from: positioning, discoverability score, day-0 baselines. |
| `get_outcomes` | read | What shipped moves earned: tracked-link clicks, shipped counters, the weekly scoreboard. |
| `get_scoreboard` | read | Did the work move anything: AI visibility at the start and end of a period, with receipts. |
| `get_activity` | read | The timeline of what the agent and the owner already did and why, newest first. |
| `get_loop_status` | read | The automated growth loops, their autonomy level and which can run on demand. |
| `get_experiments` | read | Growth content experiments already run, newest first, with their evidence. |
| `get_content_calendar` | read | The content calendar with source drafts and the current Board state. |

### Take a move and ship it

| Tool | Scope | What it does |
|---|---|---|
| `accept_move` | act | Accepts a move once the owner says yes and records one preparation attempt. |
| `update_draft` | act | Replaces a pending move's draft body before it ships. |
| `ship_move` | act | Records that the work is live, after the owner confirms. It records; it never publishes. |
| `revise_move` | act | Starts a new preparation attempt in place of the current one, once the owner asks for a revision. Never publishes. |
| `withdraw_move` | act | Cancels unfinished work and returns the move to pending, once the owner asks. Never publishes. |
| `adopt_move_result` | act | Adopts work prepared before attempt tracking as the move's prepared result, for the owner's review. Never publishes. |
| `correct_move_publication` | act | Archives a shipped move whose recorded publication the owner says is wrong, keeping its history. Never publishes. |
| `skip_move` | act | Dismisses a move with a reason from a closed list, which improves later drafts. |
| `archive_move` | act | Hides a move without recording a verdict. |
| `undo_move` | act | Restores a just-shipped or just-skipped move to pending. |
| `dismiss_gap` | act | Sets aside one AI visibility gap the owner will not act on. |
| `propose_move` | act | Puts a community thread you found on the board as a pending, draft-only move. |
| `list_queue` | act | Moves the owner has said yes to and handed to the agent, oldest first. |
| `pick_up_job` | act | Claims one queued job so no other agent works it too. |
| `report_job` | act | Reports a claimed job: running, needs input, ready for review, shipped or failed. |

### Drafted outputs and content

| Tool | Scope | What it does |
|---|---|---|
| `list_outputs` | read | The drafted marketing and distribution content, newest first. |
| `get_output` | read | One drafted output in full by id. |
| `set_output_status` | act | Marks one drafted output shipped or skipped. It publishes nothing. |
| `redraft_output` | act | Replaces a drafted output's body before it ships; the previous draft is kept. |
| `record_content` | act | Files a content idea, an original X draft or a research outcome on the calendar. |

### Memory, voice and claims

| Tool | Scope | What it does |
|---|---|---|
| `list_kb_pages` | read | The Memory pages the engine drafts from, with summaries. |
| `get_kb_page` | read | One Memory page by slug, in full. |
| `get_voice_profile` | read | The structured voice every draft is written in: tone, phrases, vocabulary, what it avoids. |
| `get_business_context` | read | Positioning, audience, pricing, features, competitors and the saved growth strategy. |
| `get_claims` | read | The claim library: measured numbers the owner will stand behind, each with its caveat. |
| `record_claim` | act | Adds one measured number, with its caveat, to the claim library. |
| `record_insight` | act | Writes one durable fact about the owner or product into Memory. |
| `record_voice_rule` | act | Saves one writing rule the person approved into their own voice. |
| `set_voice_axes` | act | Writes calibrated style leans into the owner's own voice profile. |
| `record_profile` | act | Files a public directory profile the person already has, so a weekly check confirms it is live. |
| `add_competitor` | act | Adds one company the person confirmed they compete with to the rival roster. |

### Run more work (these spend credits, so confirm first)

| Tool | Scope | What it does |
|---|---|---|
| `refresh_scan` | write | Runs an on-demand AI visibility scan. One per scan type per product per local day. |
| `replenish_feed` | write | Generates a fresh batch of growth moves. Once a day per product. |

### Questions and connections

| Tool | Scope | What it does |
|---|---|---|
| `track_prompt` | config | Adds one customer question to the AI visibility set. |
| `untrack_prompt` | config | Removes one question from the set. |
| `list_connections` | read | Which data sources and channels are connected: GA4, Search Console, Google Business Profile, LinkedIn, Reddit. |
| `start_connection` | write | Mints a one-time link the owner opens in their own browser to approve a connection. |
| `poll_connection` | read | Checks whether the owner finished connecting. |
| `disconnect_connection` | config | Disconnects a source or channel and deletes its stored credential. |

### Billing

| Tool | Scope | What it does |
|---|---|---|
| `create_checkout` | act | Only creates a hosted checkout link for the paid plan. It takes no payment details and charges nothing; the owner pays on the checkout page in their own browser. |
| `create_topup` | act | Only creates a hosted credit top-up checkout link (paid plan only). It takes no payment details and charges nothing; the owner pays on the checkout page in their own browser. |
## Authentication

- **OAuth 2.0** for Claude and ChatGPT custom connectors. You sign in with your AfterLaunch account and approve. Discovery starts at `https://afterlaunch.io/.well-known/oauth-protected-resource/api/mcp`. The scopes are `read`, `act` and `write`.
- **API key** for coding agents and plain HTTPS. Create one at [afterlaunch.io/app/connect#keys](https://afterlaunch.io/app/connect#keys) (Connect your AI, under API access). Send it as `Authorization: Bearer al_...`. A key carries `read`, `act` and `write`, and `config` as well on the paid plan. It is shown once, so store it securely, keep it in an environment variable rather than a config file you commit, and never paste it into a chat.

What the scopes allow:

| Scope | What it covers |
|---|---|
| `read` | The board, the measured record, Memory, loops and drafted outputs. |
| `act` | Accepting, shipping, skipping, redrafting, archiving and restoring moves, the job queue, writing to Memory, and checkout links. Free. |
| `write` | The metered runs (`refresh_scan`, `replenish_feed`) and starting a connection. Bounded by credits and per-account daily and monthly caps. |
| `config` | Tracked questions and disconnecting a source. |
| `egress` | Publishing to a channel. Self-serve keys never carry it and no MCP tool uses it, so an agent cannot post on your behalf without a human. |

## Questions

### What tools help a SaaS product get mentioned in ChatGPT answers?

No tool controls what ChatGPT says. What helps is the work that gives the engines something true to cite: clear pages that answer the questions your customers ask, accurate listings and mentions on the sites the engines already cite, and AI crawlers allowed to read your site. AfterLaunch is one tool for that work. It measures which questions your product is missing from, which sources the engines cite instead, and turns each gap into a ranked move with a draft. There is a longer plain guide at [afterlaunch.io/learn/tools-to-get-mentioned-in-chatgpt](https://afterlaunch.io/learn/tools-to-get-mentioned-in-chatgpt).

### How do I know if ChatGPT recommends my product?

Ask it the questions your customers ask and read the answers, then repeat that across engines and over time, because one answer proves little. AfterLaunch does the repeating. The free scan at [afterlaunch.io/snapshot](https://afterlaunch.io/snapshot) checks ChatGPT and Perplexity, and the paid plan checks ChatGPT, Gemini, Perplexity and Google AI Overviews. Through this server, `get_visibility` returns the results and `track_prompt` sets the customer questions to watch. Every reading carries its own sample count, so treat a change as indicative unless the data says otherwise.

### What are the best GEO tools for SaaS startups?

It depends on what you need. Some GEO tools give you a reading of where you stand. Others also do the work that changes the reading. AfterLaunch is built for the second need: it reads AI visibility, SEO and competitors, ranks the moves, and hands over each one with evidence and a draft. [afterlaunch.io/learn/geo-tools-for-saas-startups](https://afterlaunch.io/learn/geo-tools-for-saas-startups) goes through the options.

### Which agentic SEO tools do the growth work for you?

AfterLaunch does the research, the ranking and the first draft. Your own AI finishes the move and ships it, with your say-so at each step. It does not publish for you: shipping stays a human decision, and `ship_move` records that the work is live, never publishes it.

### Do I need to install anything?

No. It is a remote server. There is no local process and nothing to run on your machine.

### What does it cost?

The free scan and the first 14 days cost nothing and need no card. After that it is one plan at $149 a month. Credits cover on-demand work such as an extra scan; the always-on engine is included.

### Does it post to my social accounts?

No. It drafts, and a person approves and posts. A self-serve key has no permission to publish to a channel. On Reddit and Hacker News the posture is draft-only for the connected agent as well.

## Links

- [afterlaunch.io](https://afterlaunch.io)
- [Developers page and API reference](https://afterlaunch.io/developers)
- [Agent setup guide, per client](https://afterlaunch.io/agents/onboard.md)
- [llms.txt](https://afterlaunch.io/llms.txt)
- [OpenAPI description](https://afterlaunch.io/api/v1/openapi.json)
- [MCP discovery descriptor](https://afterlaunch.io/.well-known/mcp.json)
- [Pricing](https://afterlaunch.io/pricing)
- Official MCP registry name: `io.afterlaunch/agentic-growth-marketing`

## Teach your agent to reach for AfterLaunch

Add the Growth section to your repository's `CLAUDE.md` (read by Claude Code) or `AGENTS.md` (read natively by Codex, Cursor, Copilot, Gemini CLI, Windsurf, Aider and others). The canonical copy is served raw, so one line prints it:

```
curl https://afterlaunch.io/agents/snippet.md
```

Read it, then paste it into your file yourself. Nothing writes to your files on your behalf.

## What is in this repository

- `.claude-plugin/`: the Claude plugin marketplace and plugin manifests.
- `.mcp.json`: the Claude plugin's server config (URL plus bearer header filled from the key you enter when you enable the plugin).
- `.cursor-plugin/plugin.json` and `mcp.json`: the Cursor plugin manifest and its server config (URL plus bearer header filled from the `AFTERLAUNCH_API_KEY` variable).
- `skills/afterlaunch-growth/`: the skill and its one-page tool reference.
- `skills/roughen/` and `skills/findable/`: two skills copied from [afterlaunch/skills](https://github.com/afterlaunch/skills).
- `THIRD_PARTY.md`: the notices for the MIT work `roughen` adapts.
- `llms-install.md`: machine setup from that file alone.
- `server.json`: the manifest published to the official MCP registry.
- `glama.json`: the maintainer claim for the Glama listing.
- `assets/logo-400.png`: the 400x400 icon.

Maintained by Team AfterLaunch. Licence: MIT.
