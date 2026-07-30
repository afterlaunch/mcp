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
  moves, and the boundary between free actions and the ones that spend money.
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
and mint a key from Settings.

---

## Step 2: confirm the key with whoami

Call `whoami` first, every session. It returns the product run this key is
bound to, the tier (free, founder, growth or scale), the trial end date, the key
scopes, and, once credit metering is live, the credit balance. It is read-only
and free. If `whoami` fails, the key is wrong or missing and nothing else will
work; fix that before going further.

---

## Step 3: read the Feed before improvising

`list_feed` is the ranked backlog of prepared growth moves across SEO, AI
visibility (GEO), competitors and distribution channels. Each move carries its
title, why it matters, its area, status, rank and the full draft body. Read it
before proposing any growth work of your own.

- By default `list_feed` returns only live (pending) moves. Pass
  `include_resolved` to also see shipped, skipped, archived and expired ones.
- If a live move already covers what the founder asked, ship or refine that
  move rather than writing something new.

Related read-only tools, all free:

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

- `ship_move`: marks a move shipped.
- `skip_move`: dismisses a move with a reason. Use the closed feedback
  vocabulary in the tool schema; the reason improves future drafts.
- `update_draft`: replaces a draft body before shipping.
- `archive_move`: hides a move without recording a verdict.

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
  a human approves and posts.
- **Never** present a checkout link as a purchase you completed.
- Read the Feed before writing growth content of your own.
- Confirm before any money-spending tool call.

A one-page tool reference, grouped by cost and scope, is in
`reference/tools.md`. Machine setup from this repository alone is in
`llms-install.md` at the repository root.
