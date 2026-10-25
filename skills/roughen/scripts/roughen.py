#!/usr/bin/env python3
"""roughen.py: the mechanical half of the roughen skill.

Two jobs, and it is always clear which one is running:

  --report     Find the tells a regex can find and change nothing: dashes,
               banned words and phrases, invisible characters, hashtag walls,
               paragraphs that run too long. Exit 1 if any hard tell is found.

  (default)    Clean the typography (invisible characters out, dashes and
               curly quotes straightened, blank lines normalised), then roll
               the dice: drop some contraction apostrophes, lowercase some
               sentence starts, maybe one typo, all at the tolerances in
               tolerances.json and all logged so a writer can veto any one.

The register it checks against is the JSON block in SKILL.md, read live, so
there is one list and it cannot drift from the prose above it.

Usage
  python3 roughen.py draft.md --report
  python3 roughen.py draft.md --seed 7 -o out.md
  python3 roughen.py draft.md --no-roughen
  pbpaste | python3 roughen.py - --seed 7
  python3 roughen.py draft.md --tolerances mine.json --json

Standard library only. No network.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
SKILL_MD = SKILL_DIR / 'SKILL.md'
TOLERANCES = SKILL_DIR / 'tolerances.json'

# Characters a keyboard never produces. Deleted outright, or turned into a
# plain space where they are a space in disguise. The pass follows the one
# in Jakeschincariol/linkedin-agent-skill (MIT); see THIRD_PARTY.md.
DELETE = {
    0x200B: 'ZERO WIDTH SPACE', 0x200C: 'ZERO WIDTH NON-JOINER',
    0x200D: 'ZERO WIDTH JOINER', 0x2060: 'WORD JOINER',
    0xFEFF: 'ZERO WIDTH NO-BREAK SPACE', 0x00AD: 'SOFT HYPHEN',
    0x180E: 'MONGOLIAN VOWEL SEPARATOR', 0x200E: 'LEFT-TO-RIGHT MARK',
    0x200F: 'RIGHT-TO-LEFT MARK',
}
SPACE = {0x00A0, 0x202F, 0x2007, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006,
         0x2008, 0x2009, 0x200A, 0x205F, 0x3000}
TAG_RANGE = (0xE0000, 0xE007F)

CURLY = {'‘': "'", '’': "'", '‚': "'", '‛': "'",
         '“': '"', '”': '"', '„': '"', '‟': '"',
         '…': '...', '•': '-'}

# Words that may safely lose a sentence-initial capital: they are never
# names. Anything not in this list must also appear in lowercase elsewhere
# in the same text before the dice may touch it.
COMMON = set('''a an the this that these those it its i im ive ill id we our
us you your they their them he she his her there here then than so and but or
nor if when while where what which who how why not no yes just only also even
still again maybe most some every any each all both few many much more less
one two first last next now today yesterday tomorrow never always often
sometimes once because since until after before as at by for from in into of
on to with without about over under up down out off through across my me mine
is are was were be been being have has had do does did can could will would
should may might must get got make made take took go went come came see saw
know knew think thought say said tell told want need keep let try turn start
stop run work use find give put look seem feel like love hate read write post
ship build send ask show mean call'''.split())

CONTRACTIONS = re.compile(
    r"\b(?:"
    r"[A-Za-z]+n't"                                  # don't, can't, isn't
    r"|(?:it|that|what|there|here|he|she|who|let|where|how|this)'s"
    r"|I'm|(?:you|we|they)'re"
    r"|(?:I|you|we|they|could|should|would|might|must)'ve"
    r"|(?:I|you|we|they|he|she|it|that|there|who)'ll"
    r"|(?:I|you|we|they|he|she|who)'d"
    r")\b", re.I)

SENTENCE_START = re.compile(r"(?:(?<=^)|(?<=\n)|(?<=[.?!]\s)|(?<=[.?!]\s\s))([A-Z][a-z']*)", re.M)
PRONOUN_I = re.compile(r"\bI\b(?=[\s'.,;:?]|$)")
TYPO_WORD = re.compile(r"\b[a-z]{6,}\b")
DASH_NAME = {0x2012: 'figure dash', 0x2013: 'en dash', 0x2014: 'em dash',
             0x2015: 'horizontal bar', 0x2E3A: 'two-em dash',
             0x2E3B: 'three-em dash', 0xFE58: 'small em dash'}


# ---------------------------------------------------------------- register

def load_register() -> dict:
    text = SKILL_MD.read_text(encoding='utf-8')
    for body in re.findall(r'```json\n(.*?)\n```', text, re.S):
        parsed = json.loads(body)
        if isinstance(parsed, dict) and parsed.get('register') == 'prose':
            return parsed
    raise SystemExit('no prose register block found in SKILL.md')


def load_tolerances(path: Path) -> dict:
    tol = json.loads(path.read_text(encoding='utf-8'))
    for k in ('apostrophe_drop', 'lowercase', 'typo_chance'):
        v = float(tol.get(k, 0))
        if not 0 <= v <= 1:
            raise SystemExit(f'{k} must be between 0 and 1, got {v}')
        tol[k] = v
    tol['max_sentences_per_paragraph'] = int(tol.get('max_sentences_per_paragraph', 4))
    return tol


# ---------------------------------------------------------------- masking

def _span_mask(text: str, patterns: list[re.Pattern]) -> list[bool]:
    mask = [False] * len(text)
    for pat in patterns:
        for m in pat.finditer(text):
            for i in range(m.start(), m.end()):
                mask[i] = True
    return mask


def hard_mask(text: str) -> list[bool]:
    """Everything the dice must never touch: code, links, addresses,
    handles, hashtags, quoted words, anything near a number, and the
    first line of the piece."""
    mask = _span_mask(text, [
        re.compile(r'```.*?```', re.S),
        re.compile(r'`[^`\n]+`'),
        re.compile(r'https?://\S+|www\.\S+'),
        re.compile(r'\S+@\S+\.\S+'),
        re.compile(r'(?<!\w)@\w+'),
        re.compile(r'(?<!\w)#\w+'),
        re.compile(r'"[^"\n]*"'),
    ])
    tokens = list(re.finditer(r'\S+', text))
    for i, t in enumerate(tokens):
        if any(ch.isdigit() for ch in t.group(0)):
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(tokens):
                    for k in range(tokens[j].start(), tokens[j].end()):
                        mask[k] = True
    first = re.search(r'\S.*', text)
    if first:
        for k in range(first.start(), first.end()):
            mask[k] = True
    return mask


def name_mask(text: str) -> list[bool]:
    """Capitals that might be names: any capitalised word not at a sentence
    start, and anything in all capitals."""
    mask = [False] * len(text)
    starts = {m.start(1) for m in SENTENCE_START.finditer(text)}
    for m in re.finditer(r"\b[A-Z][A-Za-z'\-]*", text):
        if m.start() in starts and m.group(0) != 'I':
            continue
        for k in range(m.start(), m.end()):
            mask[k] = True
    for m in re.finditer(r'\b[A-Z]{2,}\b', text):
        for k in range(m.start(), m.end()):
            mask[k] = True
    return mask


def clear(mask: list[bool], a: int, b: int) -> bool:
    return not any(mask[a:b])


def line_of(text: str, pos: int) -> int:
    return text.count('\n', 0, pos) + 1


# ---------------------------------------------------------------- cleaning

def pass_invisible(text: str, log: list[str]) -> str:
    out = []
    for ch in text:
        cp = ord(ch)
        if cp in DELETE:
            log.append(f'invisible: removed {DELETE[cp]} (U+{cp:04X})')
            continue
        if TAG_RANGE[0] <= cp <= TAG_RANGE[1]:
            log.append(f'invisible: removed tag character (U+{cp:04X})')
            continue
        if cp in SPACE:
            log.append(f'invisible: {unicodedata.name(ch, "space")} (U+{cp:04X}) made a plain space')
            out.append(' ')
            continue
        out.append(ch)
    return ''.join(out)


def pass_typography(text: str, register: dict, log: list[str]) -> str:
    dashes = {int(cp[2:], 16) for cp in register.get('dash_code_points', [])}
    for ch, rep in CURLY.items():
        n = text.count(ch)
        if n:
            log.append(f'typography: {n} x {unicodedata.name(ch).lower()} -> {rep!r}')
            text = text.replace(ch, rep)

    def fix_dash(m: re.Match) -> str:
        before, dash, after = m.group(1), m.group(2), m.group(3)
        name = DASH_NAME.get(ord(dash), 'dash')
        if before == '' or before.endswith('\n'):
            log.append(f'typography: line {line_of(text, m.start())}: {name} at line start -> "- "')
            return before + '- ' + after
        if before.strip()[-1:].isdigit() and after.strip()[:1].isdigit():
            log.append(f'typography: line {line_of(text, m.start())}: {name} in a range -> "-"')
            return before.rstrip() + '-' + after.lstrip()
        log.append(f'typography: line {line_of(text, m.start())}: {name} -> comma')
        return before.rstrip() + ', ' + after.lstrip()

    dash_class = '[' + ''.join(re.escape(chr(cp)) for cp in dashes) + ']'
    text = re.sub(rf'(^|[^\n]?)[ \t]*({dash_class})[ \t]*([^\n]?)', fix_dash, text, flags=re.M) if dashes else text
    return text


def pass_blank_lines(text: str, log: list[str]) -> str:
    before = text
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    if text != before:
        log.append('layout: trailing spaces trimmed and blank-line runs collapsed to one')
    return text.strip('\n') + '\n'


# ---------------------------------------------------------------- dice

def roll_apostrophes(text: str, p: float, rng: random.Random, log: list[str]) -> str:
    if p <= 0:
        return text
    hard = hard_mask(text)
    out, last = [], 0
    for m in CONTRACTIONS.finditer(text):
        if not clear(hard, m.start(), m.end()):
            continue
        if rng.random() < p:
            word = m.group(0)
            out.append(text[last:m.start()] + word.replace("'", ''))
            last = m.end()
            log.append(f"dice: line {line_of(text, m.start())}: '{word}' -> '{word.replace(chr(39), '')}' (apostrophe)")
    out.append(text[last:])
    return ''.join(out)


def roll_lowercase(text: str, p: float, rng: random.Random, log: list[str]) -> str:
    if p <= 0:
        return text
    hard = hard_mask(text)
    names = name_mask(text)
    lower_words = set(re.findall(r'\b[a-z]+\b', text))
    edits: list[tuple[int, int, str]] = []
    for m in SENTENCE_START.finditer(text):
        word = m.group(1)
        if not clear(hard, m.start(1), m.end(1)) or not clear(names, m.start(1), m.end(1)):
            continue
        base = word.lower().replace("'", '')
        if base in COMMON or word.lower() in lower_words:
            if rng.random() < p:
                edits.append((m.start(1), m.end(1), word[0].lower() + word[1:]))
    for m in PRONOUN_I.finditer(text):
        if not clear(hard, m.start(), m.end()):
            continue
        if any(a <= m.start() < b for a, b, _ in edits):
            continue
        if rng.random() < p:
            edits.append((m.start(), m.end(), 'i'))
    for a, b, rep in sorted(edits, reverse=True):
        log.append(f"dice: line {line_of(text, a)}: '{text[a:b]}' -> '{rep}' (lowercase)")
        text = text[:a] + rep + text[b:]
    return text


def roll_typo(text: str, p: float, rng: random.Random, log: list[str]) -> str:
    if p <= 0 or rng.random() >= p:
        return text
    hard = hard_mask(text)
    names = name_mask(text)
    candidates = [m for m in TYPO_WORD.finditer(text)
                  if clear(hard, m.start(), m.end()) and clear(names, m.start(), m.end())]
    rng.shuffle(candidates)
    for m in candidates:
        w = m.group(0)
        spots = [k for k in range(1, len(w) - 2) if w[k] != w[k + 1]]
        if not spots:
            continue
        k = rng.choice(spots)
        typo = w[:k] + w[k + 1] + w[k] + w[k + 2:]
        log.append(f"dice: line {line_of(text, m.start())}: '{w}' -> '{typo}' (typo)")
        return text[:m.start()] + typo + text[m.end():]
    return text


# ---------------------------------------------------------------- report

def report(text: str, register: dict, tol: dict) -> tuple[list[dict], int]:
    findings: list[dict] = []
    norm = text
    for ch, rep in CURLY.items():
        norm = norm.replace(ch, rep)

    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in DELETE or cp in SPACE or TAG_RANGE[0] <= cp <= TAG_RANGE[1]:
            findings.append({'check': 'invisible', 'line': line_of(text, i),
                             'evidence': f'U+{cp:04X} {unicodedata.name(ch, "?")}', 'hard': True})
    dashes = {int(cp[2:], 16) for cp in register.get('dash_code_points', [])}
    for i, ch in enumerate(text):
        if ord(ch) in dashes:
            ln = line_of(text, i)
            findings.append({'check': 'dash', 'line': ln, 'evidence': text.split('\n')[ln - 1].strip()[:120], 'hard': True})
    for word in register.get('banned_words', []):
        for m in re.finditer(r'(?<![\w-])' + re.escape(word) + r'(?![\w-])', norm, re.I):
            findings.append({'check': 'banned_word', 'line': line_of(norm, m.start()), 'evidence': m.group(0), 'hard': True})
    for phrase in register.get('banned_phrases', []):
        for m in re.finditer(re.escape(phrase), norm, re.I):
            findings.append({'check': 'banned_phrase', 'line': line_of(norm, m.start()), 'evidence': m.group(0), 'hard': True})
    tags = re.findall(r'(?<!\w)#\w+', text)
    if len(tags) > 2:
        findings.append({'check': 'hashtag', 'line': 0, 'evidence': f'{len(tags)} hashtags: ' + ' '.join(tags[:6]), 'hard': False})
    limit = tol['max_sentences_per_paragraph']
    pos = 0
    for para in re.split(r'\n\s*\n', text):
        ln = line_of(text, pos)
        pos += len(para) + 2
        body = para.strip()
        if not body or body.startswith(('```', '- ', '* ', '|', '#')) or re.match(r'\d+\. ', body):
            continue  # code, lists, tables and headings are not paragraphs
        sentences = [s for s in re.split(r'(?<=[.?!])\s+', body) if s.strip()]
        if len(sentences) > limit:
            findings.append({'check': 'long_paragraph', 'line': ln, 'evidence': f'{len(sentences)} sentences, limit {limit}: "{body[:60]}..."', 'hard': False})
    findings.sort(key=lambda f: (not f['hard'], f['line']))
    hard = sum(1 for f in findings if f['hard'])
    return findings, hard


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description='The mechanical half of the roughen skill.')
    ap.add_argument('source', help='a file, or - for stdin')
    ap.add_argument('--report', action='store_true', help='find the mechanical tells and change nothing')
    ap.add_argument('--no-roughen', action='store_true', help='clean the typography only, no dice')
    ap.add_argument('--seed', type=int, default=None, help='repeatable dice')
    ap.add_argument('--tolerances', default=str(TOLERANCES), help='path to a tolerances json')
    ap.add_argument('-o', '--out', default=None, help='write the result here instead of stdout')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('--quiet', action='store_true', help='no change log on stderr')
    args = ap.parse_args()

    text = sys.stdin.read() if args.source == '-' else Path(args.source).read_text(encoding='utf-8')
    register = load_register()
    tol = load_tolerances(Path(args.tolerances))

    if args.report:
        findings, hard = report(text, register, tol)
        if args.json:
            print(json.dumps({'findings': findings, 'hard': hard}, indent=2))
        else:
            for f in findings:
                where = f'line {f["line"]}' if f['line'] else 'whole piece'
                print(f'{"HARD" if f["hard"] else "soft"}  {f["check"]:<15} {where}: {f["evidence"]}')
            print(f'{len(findings)} findings, {hard} hard')
        return 1 if hard else 0

    log: list[str] = []
    text = pass_invisible(text, log)
    text = pass_typography(text, register, log)
    text = pass_blank_lines(text, log)
    if not args.no_roughen:
        rng = random.Random(args.seed)
        text = roll_apostrophes(text, tol['apostrophe_drop'], rng, log)
        text = roll_lowercase(text, tol['lowercase'], rng, log)
        text = roll_typo(text, tol['typo_chance'], rng, log)
        if args.seed is not None:
            log.append(f'dice: seed {args.seed}')

    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
    if args.json:
        print(json.dumps({'text': text, 'changes': log}, indent=2))
    elif not args.out:
        sys.stdout.write(text)
    if not args.quiet and not args.json:
        for line in log:
            print(line, file=sys.stderr)
        if not log:
            print('no changes', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
