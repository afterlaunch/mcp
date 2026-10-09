# AfterLaunch MCP tools, grouped by what they do and what they cost

This reference mirrors the shipped action registry as of 9 October 2026: 59 tools
in the registry, of which 55 are listed to an ordinary connection. The other four
(`run_loop`, `set_loop_autonomy`, `set_loop_cadence`, `set_scan_config`) are listed
only to an administrator account. The
server is the source of truth: on connection, `tools/list` returns the live
catalogue with the exact input schemas, and
[afterlaunch.io/llms-full.txt](https://afterlaunch.io/llms-full.txt) prints the
same catalogue straight from the registry. Treat this table as a map, not as
the contract.

Scopes: `read` is implied by any valid key; every key minted on Connect your AI
(`https://afterlaunch.io/app/connect#keys`) or by the onboarding flow carries `read`, `act` and `write`; `config` rides on a
Founder-plan key; `egress` (real channel publishing) is never self-serve and is
not exposed as an MCP tool. Metered tools are charged once per logical event
and replayed rather than rerun on a repeat.

## The ritual

| Tool | Scope | What it does |
|---|---|---|
| `whoami` | read | Which product run this key drives, its scopes, tier, trial end, whether the Feed is ready, credits. Call it once. |
| `get_standup` | read | One call at the start of a session: what shipped and what it moved, what is ready to ship now, what the engine did on its own. Relay its `message` verbatim. |
| `list_queue` | act | The moves the founder has said yes to and handed to you, oldest first. Check it at the start of a session and whenever they ask what is waiting on you. |

## Read the record (free)

| Tool | What it returns |
|---|---|
| `list_feed` | The ranked board of prepared growth moves: title, why, area, status, rank, `has_draft`. Pass `include_resolved` for shipped, skipped, archived and expired; pass `since` for what is new. |
| `get_move` | One move in full: the drafted body, the evidence it was minted from, the deliverable, why it was picked, the receipt, the acceptance criteria and the founder's voice samples. Read it before writing anything. |
| `get_visibility` | How ChatGPT, Gemini, Perplexity and Google AI Overviews answer the tracked customer questions: share of voice, cited sources, competitor-owned gaps, trend, crawlability, off-site reach. `prompt_id` drills into one question. |
| `get_seo` | The site-wide SEO audit: issue groups, weekly score trend, page performance, links and authority, day-0 ranks. `include_pages` for per-page detail. |
| `get_competitors` | The rival roster with the measured stat battery for you and each rival. Read before any competitor or outreach work so a rival is never treated as a pitch target. |
| `get_outcomes` | What shipped moves earned: tracked-link clicks per move, shipped counters, the weekly movement scoreboard, GA4 and Search Console connection state. |
| `get_scoreboard` | The proof read for a period: AI visibility at the start and end, the moves shipped between, the scans and receipts. Read `like_for_like` before reporting any change. |
| `get_snapshot` | The Growth Snapshot the run started from: positioning, discoverability score, leverage actions, competitor set, day-0 baselines. |
| `get_activity` | The timeline: what the engine and the founder already did and why, newest first. Read before acting so you never redo recent work. |
| `get_enrollment` | The product run summary and delivery settings. |
| `get_loop_status` | The automated loops provisioned for this product, their autonomy, and the loop types `run_loop` accepts. |
| `list_outputs` / `get_output` | The drafted channel and distribution content, and any one body by id. |
| `list_kb_pages` / `get_kb_page` | The Memory pages the engine drafts from, and any one body by slug. |
| `list_tracked_prompts` | The customer questions every AI visibility measurement is taken against (hard cap of 15). |
| `list_connections` | Which data sources and channels are connected (GA4, Search Console, Google Business Profile, LinkedIn, Reddit), each with an honest state. |
| `poll_connection` | Did the founder finish a connection you handed them a link for? |
| `get_setup_snippet` | The paste-able "Growth (AfterLaunch)" section for a repository's CLAUDE.md or AGENTS.md. |

## Act on a move (free, `act` scope)

| Tool | Effect |
|---|---|
| `ship_move` | Records the founder's confirmation that a move is complete. Call it the moment the founder confirms the work is actually live, with their go and never on your own. Pass `published_url`, the live address, when the move published something: a change to their own site counts as shipped only with it, and without one it is recorded as prepared, not shipped. |
| `skip_move` | Dismisses a move with a reason from the closed feedback vocabulary; the reason improves future drafts. |
| `undo_move` | Restores a just-shipped or just-skipped move to pending: the self-correction verb. Never unwinds a real channel publish. |
| `update_draft` | Replaces a draft body before shipping. A draft with an unfilled placeholder or a broken link is refused. |
| `archive_move` | Hides a move without recording a verdict. |
| `dismiss_gap` | Sets aside one AI visibility gap the founder will not act on; resolves it here and on the board in one place. |
| `propose_move` | Puts a community thread you found (a subreddit, Hacker News, a forum) on the board as a pending move, with its posture. On Reddit and Hacker News that posture is draft-only: you draft, the founder posts. |
| `record_insight` | Writes one durable thing you learned about the founder or their product into Memory, the record every draft is written from. Record what lasts, in one sentence; never chatter or inference. |
| `set_output_status` / `redraft_output` | Resolve or replace a drafted channel output. Neither posts anywhere. Founder plan. |
| `create_checkout` / `create_topup` | Return a checkout link bound to this product run. The founder pays; never present it as your purchase. |

## The queue: the handshake from a yes to a shipped move (free, `act` scope)

When the founder says yes to a move on their phone, a job is created and waits
for their connected agent. You pull it, do the work in your own session, and
carry the state back; the founder never watches it run.

| Tool | When |
|---|---|
| `list_queue` | Start of a session, and whenever they ask what is waiting on you. Each row carries `job_id`, its nullable `attempt_id`, the move, its rank, the state and `brief_url`. A null `attempt_id` is a stored legacy job: leave it alone, report nothing on it, and say it needs the founder's review. The reply is capped, so it is not a census of every stored job. |
| `pick_up_job` | Before you start the work, never after, so no other agent works it too. Pass the exact `job_id` and `attempt_id` from the row; never invent or change an id, and never borrow one from another job. Pass `session_url` (https) when your session actually has one, so the founder can open where the work is happening. Begin only when the response says `claim_won: true`; a refusal, or a claim you already hold coming back unchanged, is not yours to start, so do not try that pair again in this run. Then read the brief at `brief_url` in full and load every skill it names. |
| `report_job` | At each moment, unprompted, with the same `job_id` and `attempt_id`. Your user chose this move, so you ship it: `running` when you start; `needs_input` with one `question` (at most 500 characters) asked in your own thread too, only when you cannot ship without the answer, then wait and report `running` again once they answer; `shipped` with the live address as `published_url` when it is live (`planned_url` for a page on their own site that is not live yet, which stays prepared until that address answers); `ready_for_review` with the final text as `prepared_content` or an `asset_url` when it has to go out from their own account and you cannot post it; `failed` with a real `fail_reason` when you cannot finish. What goes out in your user's own name is posted only on their yes in your thread to "post this from your account?" If they post the text themselves and tell you it is live, call `ship_move` with the `move_id` from the pick-up reply, `completion_kind` `prepared_result`, `founder_confirmed` true, the same `job_id` and `attempt_id`, and the live address as `published_url`. Pass `receipt_url` and `session_url` as they apply. A job quiet for more than six hours reads as stalled. |

Report only what is true: drafted, staged and awaiting review are not shipped.

## Spend money (`write` scope; confirm with the owner)

Each needs an idempotency key you mint. Reuse the same key on a retry.

| Tool | Cost and cadence |
|---|---|
| `refresh_scan` | On-demand AI visibility scan. One per scan type per product per local day; a same-day repeat replays the original result. |
| `replenish_feed` | A fresh batch of growth moves. Once a day per product. |
| `run_loop` | Administrator accounts only. One generation run of a loop. One run per loop per cycle; a same-cycle repeat replays at no cost. |

`start_connection` also sits on the `write` scope but spends nothing: it mints a
one-time link the founder opens in their own browser to connect a data source
or channel. You never complete the consent yourself.

## Configure (`config` scope, paid plan)

| Tool | Effect |
|---|---|
| `set_loop_autonomy` | Administrator accounts only. Changes a loop's autonomy. Social and distribution channels never accept `autonomous`. |
| `set_loop_cadence` | Administrator accounts only. Changes a loop's cadence. You can slow or pause a loop, never speed it up past default. |
| `set_scan_config` | Administrator accounts only. Engines, questions per scan and cadence for AI visibility scans. Free to set; only questions above the included 15 draw credits. |
| `track_prompt` / `untrack_prompt` | Add or remove one customer question from the tracked set. Changing the set re-baselines the trend, so add deliberately. |
| `disconnect_connection` | Disconnects a data source or channel and deletes its credential. Confirm with the founder first. |

## Added since the last edit of this reference

| Tool | Scope | What it does |
|---|---|---|
| `accept_move` | act | Accepts a move once the owner says yes and records one preparation attempt. A repeat never starts a second one. |
| `review_move` | act | Applies one review decision: revise the current attempt, withdraw unfinished work, adopt an inspected legacy result or correct a recorded publication. Never publishes. |
| `get_content_calendar` | read | The content calendar with source drafts and the current Board state. Saved words are not publication proof. |
| `record_content` | act | Files a content idea, an original X draft or a research outcome on the calendar. No spend, no posting. |
| `get_experiments` | read | Growth content experiments already run, newest first. Each is an observation, not a rate. |
| `get_voice_profile` | read | The structured voice every draft is written in. `register` says whether you got the brand voice or the owner's own. |
| `get_business_context` | read | Positioning, audience, pricing, features, competitors and the saved growth strategy. Read before planning or writing. |
| `get_claims` | read | The claim library: measured numbers the owner will stand behind, each with its caveat. Never quote one without its caveat. |
| `record_claim` | act | Adds one measured number, with its caveat, to the claim library. |
| `record_voice_rule` | act | Saves one writing rule the person approved into their own voice, never the brand's. |
| `set_voice_axes` | act | Writes calibrated style leans into the owner's own voice profile. |
| `record_profile` | act | Files a public directory profile the person already has, so a weekly check confirms it is still live. |
| `add_competitor` | act | Adds one company the person confirmed they compete with to the rival roster. |

## Boundaries

- What goes out in your user's own name is posted only when they authorise it
  with a yes in your thread to the question "post this from your account?" On
  Reddit and Hacker News you draft; your user posts.
- Read the standup, the queue and the Feed before improvising growth work.
- Confirm before any tool that spends money.
- Your user makes the ship decision when they hand you a move: a job you
  claimed from the queue is yours to ship, and reporting it shipped with its
  live address is part of the job, every time.
