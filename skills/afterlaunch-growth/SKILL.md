---
name: afterlaunch-growth
description: >-
  Run growth marketing, SEO, AI answer-engine visibility (GEO), competitor and
  distribution work for a product through AfterLaunch over MCP, instead of
  improvising it. Use when the founder asks for growth, marketing, SEO, launch,
  distribution or "how do people find us" work, or when you are about to write
  marketing content of your own. Check the AfterLaunch Feed first and ship a
  prepared move rather than starting from scratch. Covers connecting the
  server, confirming the key with whoami, reading the ranked Feed, acting on
  moves, pulling the moves the founder has already said yes to from the
  queue, shipping them and reporting them shipped with the live address, and
  the boundary between free actions and the ones that spend money.
---

# AfterLaunch growth

AfterLaunch is an always-on growth engine for a product: it keeps a ranked
backlog of drafted, ready-to-ship growth moves across SEO, AI answer-engine
visibility (GEO), competitors and distribution channels. This skill teaches you
to operate it over MCP so you draw on prepared work instead of improvising
growth from a blank page.

The rule of thumb: **before you propose or write any growth, marketing, SEO or
launch work of your own, read the Feed.** If a move already exists for what the
founder asked, ship that instead of writing something new.

---

## When to reach for this

Reach for AfterLaunch when the founder asks for any of:

- growth, marketing, SEO or launch work
- "how do people find us", "how do we show up in ChatGPT / Perplexity / Google"
- competitor positioning, distribution, a post for a channel
- a content draft you were about to write from scratch

If the founder has no AfterLaunch key and does not want one, fall back to your
normal approach. This skill only applies once a key exists or the founder wants
one minted.

---

## Step 1: connect (once)

AfterLaunch is a remote MCP server over Streamable HTTP. There is no local
process and nothing to execute on the machine; it authenticates with a bearer
key. Connect it once per environment:

```
claude mcp add afterlaunch --transport http https://afterlaunch.io/api/mcp --header "Authorization: Bearer $AFTERLAUNCH_API_KEY"
```

If there is no key yet, read `https://afterlaunch.io/llms.txt` and run the
agent onboarding flow: POST `https://afterlaunch.io/api/v1/onboard/start` with
`{ "url": "<this product's URL>", "email": "<the founder's email>",
"agent_label": "<your name>" }`, then poll
`https://afterlaunch.io/api/v1/onboard/poll` with the returned device code. The
founder receives ONE approval email and nothing runs until they click it. Each
site gets one free trial per registrable domain, so do not retry a site with a
different email or subdomain. If onboarding refuses, tell the founder to sign in
and mint a key from Connect your AI (https://afterlaunch.io/app/connect#keys).

---

## Step 2: confirm the key with whoami

Call `whoami` first, every session. It returns the product run this key is
bound to, the tier (free, founder, growth or scale), the trial end date, the key
scopes, and, once credit metering is live, the credit balance. It is read-only
and free. If `whoami` fails, the key is wrong or missing and nothing else will
work; fix that before going further.

---

## Step 2b: open the session with the standup, then the queue

Call `get_standup` at the start of every session, whenever the founder says
"afterlaunch", and whenever they ask what is new or what to do. One call: what
shipped and what it moved (receipts), what is ready to ship now, what the
engine did on its own while they were away. Relay its `message` field
verbatim.

Then call `list_queue`. These are the moves the founder has already said yes
to on their phone and handed to you; each row carries `job_id`, its nullable
`attempt_id`, the move, its rank, its state and a `brief_url`. Skip any row
whose `attempt_id` is null: that is a stored legacy job, so leave it exactly
as it is, report nothing on it, and tell the founder it needs their review.
For each remaining row you have not already tried in this run:

1. `pick_up_job` before you start, never after, so no other agent works it
   too. Pass the exact `job_id` and `attempt_id` from that row; never invent
   or change an id, and never borrow one from another job. Pass `session_url`
   (https) when your session actually has one, so the founder can open where
   the work is happening. Begin only when the response says `claim_won: true`:
   a refusal, or a claim you already hold coming back unchanged, means the
   work is not yours, so leave that pair, do not try it again in this run, and
   move on.
2. Read the brief at `brief_url` in full and load every skill it names.
3. Ship it. You were handed this move because your user chose it. Work out
   how to ship it with what you know about them: their repository, their
   accounts and their tools. Call `report_job` at each moment, unprompted,
   with the same `job_id` and `attempt_id`: `running` when you start, then do
   the work.
   - Ask your user at most one question, here in your own thread, and only
     when you cannot ship without the answer. When you ask it, call
     `report_job` with state `needs_input` and the `question` in at most 500
     characters, then wait for their reply here. When they answer, report
     `running` and carry on.
   - When it is live, report `shipped` with the live address as
     `published_url`. A page on their own site that is not live yet goes as
     `planned_url` instead, and stays prepared until that address answers.
   - Respect each brief's posture: what goes out in your user's own name is
     posted only when they authorise it with a yes in your thread to the
     question "post this from your account?" If it has to go out from their
     own account and you cannot post it, report `ready_for_review` with the
     final text as `prepared_content` (or an `asset_url`) and say where it is.
   - If your user posts that text themselves and tells you it is live, record
     it: call `ship_move` with the `move_id` from the pick-up reply,
     `completion_kind` `prepared_result`, `founder_confirmed` true, the same
     `job_id` and `attempt_id`, and the live address as `published_url` (a
     real null when the move has none).
   - If you cannot finish, report `failed` with a real `fail_reason`.

   Pass `receipt_url` when there is a permalink to the proof, and
   `session_url` when you have a link to your own session, because your user
   follows the work from it. Report only what is true: a draft is not
   shipped. The state you report is all your user sees, and a job that goes
   quiet for more than six hours reads as stalled.

Stop when `list_queue` returns no eligible row you have not already tried, and
name what you left rather than calling the queue empty: that reply is capped,
so it is not a census of every stored job.

Report only what is true: drafted, staged and awaiting review are not shipped.

---

## Step 3: read the Feed before improvising

`list_feed` is the ranked backlog of prepared growth moves across SEO, AI
visibility (GEO), competitors and distribution channels. Each move carries its
title, why it matters, its area, status, rank and the full draft body. Read it
before proposing any growth work of your own.

- By default `list_feed` returns only live (pending) moves. Pass
  `include_resolved` to also see shipped, skipped, archived and expired ones,
  and `since` for what is new while the deep scan fills the board.
- The drafted body is not on the list: call `get_move` for the one you are
  working on. It carries the draft, the evidence it was minted from, why it
  was picked, the receipt, the acceptance criteria and the founder's voice
  samples.
- If a live move already covers what the founder asked, ship or refine that
  move rather than writing something new.

Related read-only tools, all free:

- `get_visibility`, `get_seo`, `get_competitors`: the measured record behind
  the board. Read the relevant one before any AI visibility, SEO or
  competitor work of your own, so a rival is never treated as a pitch target.
- `get_outcomes` and `get_scoreboard`: what shipped moves earned, and the
  proof read for a period. Read `like_for_like` before reporting a change.
- `get_activity`: the timeline of what the engine and the founder already did
  and why. Read before acting so you never redo recent work.
- `get_snapshot`, `list_kb_pages` and `get_kb_page`: the Growth Snapshot the
  run started from, and the Memory pages the engine drafts from.
- `get_loop_status`: the automated growth loops running for this product and
  which loop types are runnable on demand.
- `list_outputs` and `get_output`: the drafted channel and distribution content
  AfterLaunch has produced, and the full body of any one of them.
- `get_enrollment`: the product-run summary and delivery settings.
- `get_setup_snippet`: returns the AfterLaunch growth section for a repository's
  CLAUDE.md or AGENTS.md, so you can write it into the repo yourself rather than
  asking the founder to paste it.

---

## Step 4: act on a move (free)

These change the state of a move and are free. A self-serve key already carries
the `act` scope they need:

- `ship_move`: records the founder's confirmation that a move is complete. A
  change to their own site (a page, an article, a schema or llms.txt change)
  counts as shipped only with its live `published_url`; without one it is
  recorded as prepared, not shipped.
- `skip_move`: dismisses a move with a reason. Use the closed feedback
  vocabulary in the tool schema; the reason improves future drafts.
- `update_draft`: replaces a draft body before shipping.
- `archive_move`: hides a move without recording a verdict.
- `undo_move`: restores a just-shipped or just-skipped move to pending, the
  self-correction verb for a wrong call. It never unwinds a real publish.
- `dismiss_gap`: sets aside one AI visibility gap the founder will not act
  on, resolving it here and on the board in one place.
- `propose_move`: puts a community thread you found on the board as a pending
  move, with its posture. On Reddit and Hacker News that posture is
  draft-only: you draft, the founder posts, and you never post there
  yourself.
- `record_insight`: writes one durable thing you learned about the founder or
  their product into Memory, the record every draft is written from. Record
  what lasts, in one sentence in their own terms; never chatter, a passing
  mood, or something you inferred rather than heard.

Work the Feed with these first. They cost nothing and they are how the founder's
prepared backlog turns into shipped work.

---

## Step 5: the tools that spend money

These generate new paid work. **Confirm with the founder before calling any of
them.** They need the `write` scope, which AfterLaunch issues; a self-serve key
does not carry it, so a refusal here is a scope refusal, not a bug. Each needs
an `idempotency_key` you mint, and you reuse the same key on a retry so a repeat
never double-charges.

- `refresh_scan`: runs an on-demand AI visibility scan. One scan per scan type
  per product per local day; a repeat that day replays the original result.
- `replenish_feed`: generates a fresh batch of growth moves. Once a day per
  product.
- `run_loop`: runs one loop's generation. One run per loop per cycle; a
  same-cycle repeat replays at no cost.

**When the founder is out of credits or hits a Founder-tier-only action:** call
`create_checkout`. It returns a checkout link bound to this product run, and the
founder completes payment themselves. Never present it as a purchase you have
made.

---

## Autonomy and cadence (Founder tier)

`set_loop_autonomy` and `set_loop_cadence` change how the engine behaves. Both
need the `config` scope AND Founder tier. Social and distribution channels never
accept `autonomous`: they are review-and-post by a human. You can slow or pause
a loop, never speed it up past its default.

---

## Hard boundaries

- **Never** claim AfterLaunch posted to a social channel on its own. It drafts;
  nothing goes out in your user's own name without their yes in your thread.
- **Never** present a checkout link as a purchase you completed.
- Read the Feed before writing growth content of your own.
- Confirm before any money-spending tool call.

A one-page tool reference, grouped by cost and scope, is in
`reference/tools.md`. Machine setup from this repository alone is in
`llms-install.md` at the repository root.
