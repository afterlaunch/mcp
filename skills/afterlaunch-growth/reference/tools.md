# AfterLaunch MCP tools, grouped by cost and scope

This reference mirrors the shipped action registry
(`apps/web/lib/public-api/registry.ts`) as of the time this artefact was
staged. The server is the source of truth: on connection, `tools/list` returns
the live catalogue with the exact input schemas. Treat this table as a map, not
as the contract.

## Read (free, `read` scope)

| Tool | What it returns |
|---|---|
| `whoami` | The product run this key is bound to, tier, trial end date, key scopes, credit balance when metering is live. Call first. |
| `list_feed` | The ranked backlog of prepared growth moves, each with its full draft body. Pass `include_resolved` for shipped / skipped / archived / expired. |
| `get_loop_status` | The automated loops provisioned for this product and the loop types `run_loop` accepts. |
| `get_enrollment` | The product-run summary and delivery settings. |
| `list_outputs` | The drafted channel and distribution content (newest first). |
| `get_output` | One drafted output by id, with its full body. |
| `get_setup_snippet` | The AfterLaunch growth section for a repo's CLAUDE.md or AGENTS.md. |

## Act on a move (free, `act` scope)

| Tool | Effect |
|---|---|
| `ship_move` | Marks a move shipped. |
| `skip_move` | Dismisses a move with a reason from the closed feedback vocabulary. |
| `update_draft` | Replaces a draft body before shipping. |
| `archive_move` | Hides a move without recording a verdict. |
| `create_checkout` | Returns a checkout link bound to this product run. The founder pays; never present it as your purchase. |

## Spend money (`write` scope, AfterLaunch-issued; confirm with the founder)

Each needs an `idempotency_key` you mint. Reuse the same key on a retry.

| Tool | Cost and cadence |
|---|---|
| `refresh_scan` | On-demand AI visibility scan. One per scan type per product per local day; a same-day repeat replays the original result. |
| `replenish_feed` | Fresh batch of growth moves. Once a day per product. |
| `run_loop` | Runs one loop's generation. One run per loop per cycle; a same-cycle repeat replays at no cost. |

Real channel publishing (approving a drafted output for dispatch) sits on the
separate `egress` scope, which AfterLaunch issues and self-serve keys never
carry, and it is not currently exposed as an MCP tool. Social and distribution
content stays review-and-post by a human.

## Configure (`config` scope AND Founder tier)

| Tool | Effect |
|---|---|
| `set_loop_autonomy` | Changes a loop's autonomy. Social and distribution channels never accept `autonomous`. |
| `set_loop_cadence` | Changes a loop's cadence. You can slow or pause a loop, never speed it up past default. |

## Boundaries

- Social and distribution content is always review-and-post by a human.
- Read the Feed before improvising growth work.
- Confirm before any `write`-scope tool call.
