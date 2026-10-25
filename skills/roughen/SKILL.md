---
name: roughen
description: Make machine-written prose read as if a person typed it. Audits a finished piece against one register of the patterns that give AI writing away, fixes what fails, then puts back, by dice and at tolerances you set, the small roughness a person leaves behind. Prose only.
when_to_use: Use on any finished piece of writing before it goes out, a post, an email, a page, a reply, when you ask does this sound like AI, or after any drafting step. Run it on hand-written work too; it only flags there.
allowed-tools: Read Grep Glob Bash Edit
---

# Roughen

Two moves, in this order. Take out what a model reaches for. Then put back,
at random, what a person leaves in.

The first move is an audit, and it runs after the writing exists. Never hand
this file to whatever is doing the writing as a brief. A model given a
checklist while it writes satisfies the checklist and loses the point; the
same register run afterwards catches the same problems without causing that
one. Assemble what you need before you start, check what you produced after
you finish, and put nothing in between.

The second move is the dangerous one, so it does not run as an instruction
at all. "Start one sentence in three without a capital" is a pattern, and a
pattern is a new tell. So the roughness is rolled, not written: a script
draws from tolerances you set, with a seed you can repeat, and shows you
every change so you can veto any one of them. The model never decides where
the rough edges go. Dice do.

## Whose words are these

Decide this before anything else, because it changes what you are allowed
to do.

- **A model wrote it.** Apply the fixes. There is no voice to protect.
- **A person wrote it.** Flag and suggest, never rewrite. Quote the line,
  say which tell it is, offer one fix, and let them choose. Their own
  casing, punctuation habits, sentence length and roughness are their
  voice, not tells, and an audit that sands them off has made the piece
  more machine-like, not less. The register still wins on invention and on
  the banned vocabulary.

## How to run it

**1. Mechanical pass first.** Cheap, and it front-loads the certain
findings.

```
python3 scripts/roughen.py draft.md --report
```

It reports dashes, banned words and phrases, invisible characters, hashtag
walls, and paragraphs that run too long. It changes nothing in this mode.

**2. Read the whole thing once**, then go through the register below and
mark every tell you find, strongest first. Look at paragraph shape as well
as sentences: a contrast split across two sentences, three parallel
examples, or the same closer after every section is the same tell at a
larger scale.

**3. Report per finding**, most severe first: the tell, named from the
register; the sentence, quoted; the suggested fix; and whether it is a
defect, a judgement call, or a collision with something already decided
on purpose.

**4. Fix** (if a model wrote it) or hand over the suggestions (if a person
did). When you rewrite, state each point plainly rather than patching
flagged phrases one at a time. If a sentence stays awkward, rewrite the
paragraph around its main point. Keep every supported claim. Add no fact,
name, number, date, quote or citation that was not in the source.

**5. Roll the dice.**

```
python3 scripts/roughen.py draft.md --seed 7 -o out.md
```

This cleans the typography (dashes, curly quotes, invisible characters),
normalises blank lines between paragraphs, then applies the roughness
pass from `tolerances.json`. It prints every change it made. Show that
list to the writer. Any single change can be refused.

**6. Read it aloud.** Machine text is evenly weighted and nothing surprises
you. If no sentence makes you stop, neither will it for a reader. Every
sentence the same length is the failure to listen for.

## The writing rules, while you fix

**Fewer and simpler words, not shorter pieces.** A long post is fine. The
question is whether the same thing could be said with plainer words and
fewer of them. If it could, do that. Cut intensifiers doing no work,
throat-clearing before the point, a close that restates the opening, and
any adjective not carrying a fact.

**Say it clearly.** One idea per sentence. If a sentence needs a detail you
do not have, write a simpler sentence rather than inventing the detail.

**Contract your words.** "Wouldn't", not "would not". "It's", "doesn't",
"won't", "here's", "that's". Formal full forms in casual writing are a
tell, because the register does not match the room. All full forms is a
tell; all contractions is a different tell; uniform anything is the tell.

**Casual over correct.** Aim for how you would say it out loud, not for a
clean sentence. Slightly loose beats slightly stiff.

**Blank lines between ideas.** One idea, one paragraph, a blank line, the
next. A wall of text reads as generated even when every sentence passes.
A paragraph that changes subject halfway is two paragraphs.

**Never a mistake in the facts.** The dice may scuff the typing. Nothing
may ever touch a number, a name, a date, a link, a quoted line or the
first line of the piece. Careless in the typing, never careless in the
facts.

## Hard gates for anything going out

Any one fails the piece.

1. **Em-dashes.** Zero. Use a full stop and a new sentence, a colon, or a
   comma.
2. **Banned vocabulary.** Zero instances from the register. One is enough.
3. **Invented numbers or experience.** Every figure traces to something
   measured or a named public source. No invented personal experience,
   expectation, feeling or reaction put in the writer's mouth ("my guess
   going in", "I went in expecting"). If it cannot be traced, cut it.
4. **Claims about a named person or company.** An observation with a
   date, never a verdict.
5. **Engagement bait.** No "like if you agree", no question that exists
   only to farm replies.
6. **The four shapes.** No aphorisms, no "it's not X, it's Y", no pithy
   fragments for emphasis, no stacked fragments.
7. **Uncontracted casual prose.** Full forms where a person would contract.

Soft checks, report and suggest:

8. **Length.** Note the character count against where the piece is going.
   A LinkedIn post reads best somewhere around 900 to 1,300 characters;
   X is 280 unless the account has the longer limit.
9. **Rhythm.** Uniform sentence length, rule-of-three lists, and the
   intro, balanced body, summary, optimistic close shape.
10. **Specificity.** Count the adjectives doing no work.
11. **The opening.** Does the first line stand alone and earn the second?
12. **Case and formatting.** Casing follows the writer's own samples where
    there are any. Hashtags sparingly if the platform uses them at all.

## Three rules for the findings

**A decision already made beats this register.** Where the writer has
deliberately settled something, that wins and the finding closes as
"collision, no action". Write it down once in `EXCEPTIONS.md` next to this
file rather than re-litigating it every run. One line per accepted
exception. The file is optional; a run without one has nothing to skip yet.

**Separate defect from preference.** "This restates the opening" is a
defect. "I would have used a shorter word" is not a finding at all. If you
cannot say what breaks, you have an opinion.

**Do not manufacture findings.** If nothing fails, say so and stop. A
register with a quota becomes a machine for inventing work, which is its
own kind of machine-made output. The same goes for roughness: never add a
rough edge by hand to seem human. That is what the dice are for, and they
only run with the tolerances the writer set.

## Output

A short table: tell, verdict, evidence, suggested fix. Then the rewritten
text if a model wrote the original. Then the dice log. Then one line on
anything you could see was wrong but could not fix without the writer's
decision.

## What this cannot do alone

It cannot tell whether the result reads better to a real reader; that
needs a reader. It cannot learn the writer's voice from one piece; their
own posted samples do that, and samples beat this file on style every
time. And it cannot know what the writer has already decided unless they
wrote it in `EXCEPTIONS.md`.

This file is written in British English. The text you run it on keeps
whatever spelling it already has.

---

# The register

One list of the patterns that give machine-made prose away. An entry earns
its place one of two ways: it appears on two or more independent public
lists, or it is mechanically checkable and has been caught on a real,
published piece. Neither "one person dislikes it" nor "it feels a bit AI"
is enough. A register that accepts taste becomes one person's aesthetics
wearing the authority of a rule, and then it starts overruling choices
that were made on purpose.

## Vocabulary, zero tolerance

leverage, unlock, delve, harness, robust, seamless, utilise, utilize,
empower, navigate (figurative), foster, streamline, fundamentally,
elevate, revolutionise, revolutionize, game-changer, cutting-edge,
best-in-class, industry-leading, transformative, holistic, synergy,
paradigm, ecosystem (figurative), supercharge, turbocharge, double-down,
deep dive, unpack (figurative), tapestry, testament, realm, landscape
(figurative), embark, journey (figurative), AI-powered, disruptive,
growth hacking

"navigate" and "ecosystem" are judgement tells for their figurative use
only. Used literally ("the npm ecosystem", "navigate the settings") they
are ordinary prose and the script does not flag them.

## Phrases

"in today's landscape", "in an increasingly", "it's not just X, it's Y",
"let that sink in", "the truth is", "here's the thing", "at the end of the
day", "moving the needle", "circle back", "low-hanging fruit", "the
reality is", "make no mistake", "that said" as a paragraph opener, and
the openings that bait or promise instead of giving: "Confession:", "let
me tell you about", "here's a thread", "what do you think?", "like if you
agree"

## Punctuation and typography

- **Em-dash.** Zero, always.
- Semicolons in social copy read as drafted rather than spoken.
- Curly quotes mixed with straight ones.
- Bold used for emphasis more than once or twice.
- Invisible characters: zero-width spaces and joiners, soft hyphens,
  byte-order marks, non-breaking and narrow spaces. A keyboard never
  produces them, they survive copy and paste, and they are the most
  mechanical tell there is.

## Constructions, zero tolerance

The four shapes that give a piece away fastest.

- **Aphorisms.** Any sentence built to be quotable rather than to say
  something. If it would fit on a quote card, it fails.
- **This, but that.** "It's not X, it's Y", "Not a tool. A system.", and
  every variant of the reversal. The most overused construction in AI
  copy.
- **The pithy fragment.** A clipped ending for emphasis. "Simple, right?",
  "Every time.", "That's it.", "Not close."
- **Stacked fragments.** "Fast. Simple. Done." Three beats where a
  sentence would do.

## Staging instead of stating

Five patterns that rate as the strongest current tells: one sighting
justifies a flag. Each names something the sentence does instead of
adding a fact. (From blader/humanizer, MIT, sections 1 to 5.)

- **Not X but Y, in every form.** "Not just X, but Y", "it's not X,
  it's Y", "X rather than Y" used for weight, the contrast split across
  two sentences ("This does not mean X. It means Y."), and the clipped
  tail (", no guessing"). The negative half names something nobody
  claimed. Keep a contrast only when the reader actually holds the
  belief being corrected, or both halves carry information.
- **One-line closers and dramatic fragments.** A one-sentence paragraph
  that restates the one before it, "That is the real win.", "Read that
  again.", the same closer after several sections, a row of fragments,
  one word in capitals or "every. single. day." A short line is fine
  when it carries a new fact.
- **Sayings that sound deep.** "The real question is", "at its core",
  "what really matters", "the heart of the matter", "X is the Y of Z",
  "X becomes a trap", "the language of", "the currency of". An ordinary
  point dressed as a hidden truth. Say the specific claim.
- **Staged run-ups before the point.** "Let's dive in", "let's break
  this down", "here's what you need to know", "without further ado", a
  standalone "Honestly?" or "Look," or "Real talk" before a routine
  claim. Announcing the point instead of making it. **Not this entry:**
  a first-person "I learned this", "here's what I learned", "I studied
  these results and here is what I found" followed by the thing found.
  That is the writer's point of view and it is the voice, so never flag
  it.
- **Arguing with no one.** "I'm not saying", "To be clear", "Don't get
  me wrong", "This isn't about", "You might think... but", "A tempting
  approach would be". An answer to an objection nobody raised. Keep an
  objection the text attributes to someone or answers in full.

## The essay machinery

One instance of any of these is a judgement call; recurrence fails the
piece.

- **Enumeration scaffolds.** "Three measurements change what that means.
  The first is... The second is... The third..." Announcing a list, then
  walking it with ordinals. Say the things and let the reader count.
- **Meta-connectives.** "Two things are true at once.", "Two details
  stand out.", "Here is where it gets interesting." Sentences that
  announce structure instead of carrying content. Delete them; if the
  paragraph stops making sense without them, the structure was
  load-bearing and the fix is the paragraph, not the connective.
- **The X-not-Y pivot.** "Measured, not projected." The reversal's
  smaller sibling: a clipped contrast doing rhetoric instead of work.
  Recast with "rather than", or give each half its own plain sentence.
- **Uniform tidy landings.** Every paragraph clicking shut on a polished
  final beat. Human paragraphs sometimes just stop; let a few.
- **Uncontracted prose.** Any prose meant to read as written by a person
  wants natural contractions mixed with formal forms.

## Register, structure, tone

- Any adjective not carrying a fact.
- Throat-clearing before the point.
- A closing line that restates the opening in different words.
- Uniform sentence length across a whole piece.
- Rule-of-three lists everywhere, especially three adjectives.
- Intro, balanced body, summary, optimistic close.
- Every paragraph the same shape; symmetrical thread posts, each the
  same length.
- Hedging on every claim.
- Balance for its own sake, presenting two sides where one is right.
- Enthusiasm with no specific object.
- Advice with no failure mode attached.
- Authority claimed rather than shown.

## Not tells, when the writer's own samples show them

- Lowercase sentence starts and loose casing
- Extra full stops, a trailing ".." or "..."
- A typo or small grammar slip the writer left in
- An exclamation mark
- Emoji doing a job, such as marking sections on LinkedIn
- Long sentences that run on the way someone talks

Never add any of these by hand to look human. Never remove them from a
person's own words either. The dice below are the only thing allowed to
add them, and only at the writer's tolerances.

## Machine-checked

The subset the script reads, in the form it reads it: straight
apostrophes, matched without regard to case, words on word boundaries,
phrases as substrings. Edit it and the script follows.

```json
{
  "register": "prose",
  "banned_words": [
    "leverage", "unlock", "delve", "harness", "robust", "seamless",
    "utilise", "utilize", "empower", "foster", "streamline",
    "fundamentally", "elevate", "revolutionise", "revolutionize",
    "game-changer", "cutting-edge", "best-in-class", "industry-leading",
    "transformative", "holistic", "synergy", "paradigm", "supercharge",
    "turbocharge", "double-down", "deep dive", "unpack", "tapestry",
    "testament", "realm", "landscape", "embark", "journey", "AI-powered",
    "disruptive", "growth hacking"
  ],
  "banned_phrases": [
    "in today's landscape", "in an increasingly", "it's not just",
    "it is not just", "let that sink in", "the truth is",
    "here's the thing", "here is the thing", "at the end of the day",
    "moving the needle", "circle back", "low-hanging fruit",
    "the reality is", "make no mistake", "what do you think?",
    "like if you agree", "confession:", "let me tell you about",
    "here's a thread", "here is a thread", "two things are true",
    "two details stand out", "here is where it gets interesting",
    "here's where it gets interesting", "that is the real win",
    "read that again", "every. single. day.", "the real question is",
    "at its core", "what really matters", "the heart of the matter",
    "becomes a trap", "the currency of", "let's dive in",
    "let's break this down", "here's what you need to know",
    "without further ado", "honestly?", "real talk", "I'm not saying",
    "to be clear", "don't get me wrong", "this isn't about",
    "you might think", "a tempting approach would be"
  ],
  "dash_code_points": ["U+2012", "U+2013", "U+2014", "U+2015", "U+2E3A", "U+2E3B", "U+FE58"],
  "checks": ["dash", "banned_word", "banned_phrase", "invisible", "hashtag", "long_paragraph"]
}
```

---

# The dice

Everything in this section is a tolerance in `tolerances.json`, next to
this file. The defaults are one writer's; change them to yours. Set any
knob to 0 and that pass is off. Run with `--seed` and the same draft gives
the same result every time, so a change can be reviewed and repeated.

| Knob | Default | What it means |
| --- | --- | --- |
| `apostrophe_drop` | 0.33 | Each contraction apostrophe ("don't", "it's", "I'm", "we've") has this chance of being dropped. Possessives are left alone. |
| `lowercase` | 0.16 | Each eligible capital has this chance of becoming lowercase. Eligible means the first word of a sentence when it is an ordinary word, and the pronoun "I". A capital that might be a name is never touched. |
| `typo_chance` | 0.2 | The chance that this piece gets one typo at all. At most one per piece: two adjacent interior letters swapped in an ordinary lowercase word of six letters or more. Never in the first line. |
| `max_sentences_per_paragraph` | 4 | Report only. A paragraph longer than this is flagged for the writer to split; the script never splits ideas. |

**What the dice never touch.** Numbers, anything next to a number, names
and anything else capitalised mid-sentence, links, email addresses,
handles, hashtags, code, anything inside quotation marks, and the first
line of the piece. The script protects all of these before it rolls.

**Why dice and not a rule.** A fixed share of lowercase openings is a
pattern, and readers find patterns. A seeded draw at a low rate is not
one: some pieces come out untouched, some get one rough edge, and nothing
repeats at a fixed interval. That is what a person typing looks like from
the outside, and it is the only honest way to add roughness.

---

## Sources

The vocabulary and phrase lists were compiled from the banned-word lists
of ten public posting skills, keeping what two or more agree on. The five
"Staging instead of stating" entries are from blader/humanizer (MIT,
copyright Siqi Chen). The invisible-character pass in the script follows
the one in Jakeschincariol/linkedin-agent-skill (MIT). Both are attributed
in full in `THIRD_PARTY.md` at the root of this repository.
