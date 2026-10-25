#!/usr/bin/env python3
"""roughen evals: lints over the skill's own files, and behaviour tests of the
script. Offline, standard library only.

    python3 evals/run.py        # exit 0 = every check passes
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parent.parent
SCRIPT = SKILL / 'scripts' / 'roughen.py'
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = '') -> None:
    print(('PASS' if ok else 'FAIL'), name, '' if ok else detail)
    if not ok:
        FAILURES.append(name)


def run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin,
                          capture_output=True, text=True)


def lint_files() -> None:
    skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    for f in ('name', 'description', 'when_to_use', 'allowed-tools'):
        check(f'frontmatter has {f}', re.search(rf'^{f}:', skill, re.M) is not None)
    for h in ('Whose words are these', 'How to run it', 'The writing rules',
              'Hard gates', 'Three rules for the findings', 'What this cannot do alone',
              '# The register', 'Vocabulary, zero tolerance', 'Staging instead of stating',
              'Not tells, when the writer', 'Machine-checked', '# The dice', 'Sources'):
        check(f'section present: {h}', h in skill)
    check('audit runs after the writing, never as a brief', 'brief' in skill and 'after' in skill)
    check('a person\'s words are flagged, never rewritten', 'never rewrite' in skill.lower())

    shipped = [p for p in REPO.rglob('*') if p.is_file() and p.suffix in {'.md', '.py', '.json'}
               and '.git' not in p.parts]
    for p in shipped:
        text = p.read_text(encoding='utf-8')
        rel = p.relative_to(REPO)
        check(f'no em-dash in {rel}', chr(0x2014) not in text)
        if p.suffix == '.md':
            check(f'no exclamation mark in {rel}', '!' not in text.replace('exclamation', '').replace('![', ''))
            allowed = {'utilize', 'revolutionize', 'humanize'}  # the last is an upstream file name
            hits = [w for w in re.findall(r'\b\w+iz(?:e|ed|es|ing|ation)\b', text, re.I)
                    if w.lower() not in allowed]
            check(f'british spelling in {rel}', not hits, str(hits))
            for frag in ('co' + 'st', 'pri' + 'ce', 'sp' + 'end', 'cred' + 'it'):
                check(f'no "{frag}"-shaped language in {rel}', re.search(frag, text, re.I) is None)
    inside = (SKILL / 'SKILL.md').read_text() + (SKILL / 'tolerances.json').read_text() + SCRIPT.read_text()
    check('the skill folder names no product or company', 'after' + 'launch' not in inside.lower())
    check('no personal handle anywhere',
          re.search('|'.join(['shr' + 'eyas', 'caffeine' + 'mojo']),
                    '\n'.join(p.read_text() for p in shipped), re.I) is None)

    blocks = [json.loads(b) for b in re.findall(r'```json\n(.*?)\n```', skill, re.S)]
    reg = next((b for b in blocks if b.get('register') == 'prose'), None)
    check('register json block parses', reg is not None)
    if reg:
        check('register has at least 30 banned words', len(reg['banned_words']) >= 30, str(len(reg['banned_words'])))
        check('register has at least 30 banned phrases', len(reg['banned_phrases']) >= 30, str(len(reg['banned_phrases'])))
        vocab = re.search(r'## Vocabulary, zero tolerance\n\n(.+?)\n\n', skill, re.S).group(1)
        missing = [w for w in reg['banned_words'] if w.lower() not in vocab.lower()]
        check('every machine-checked word is also in the prose list', not missing, str(missing))
    tol = json.loads((SKILL / 'tolerances.json').read_text())
    check('tolerances carry the four knobs',
          set(tol) == {'apostrophe_drop', 'lowercase', 'typo_chance', 'max_sentences_per_paragraph'}, str(sorted(tol)))
    check('third-party notices present', (REPO / 'THIRD_PARTY.md').exists()
          and 'Siqi Chen' in (REPO / 'THIRD_PARTY.md').read_text()
          and 'Schincariol' in (REPO / 'THIRD_PARTY.md').read_text())


def test_script() -> None:
    tells = ('Our launch is a game-changer ' + chr(0x2014) + ' here' + chr(0x2019) + 's the thing, it' + chr(0x2019) + 's seamless.\n\n'
             'We leverage everything.' + chr(0x200B) + ' Second paragraph.\n')
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / 'a.md'
        src.write_text(tells, encoding='utf-8')
        r = run(str(src), '--report', '--json')
        check('report exits 1 on hard tells', r.returncode == 1, r.stderr[-300:])
        found = {f['check'] for f in json.loads(r.stdout)['findings']} if r.stdout else set()
        for c in ('dash', 'banned_word', 'banned_phrase', 'invisible'):
            check(f'report finds {c}', c in found, str(found))

        r = run(str(src), '--no-roughen', '--quiet')
        check('clean exits 0', r.returncode == 0, r.stderr[-300:])
        check('clean removes the em-dash', chr(0x2014) not in r.stdout)
        check('clean removes the invisible character', chr(0x200B) not in r.stdout)
        check('clean straightens curly quotes', chr(0x2019) not in r.stdout and "here's" in r.stdout)
        check('clean keeps the words', 'game-changer' in r.stdout and 'Second paragraph.' in r.stdout)

        bullets = 'Intro line.\n' + chr(0x2014) + ' first point\n' + chr(0x2014) + ' second point\n'
        src.write_text(bullets, encoding='utf-8')
        r = run(str(src), '--no-roughen', '--quiet')
        check('a dash at line start becomes a bullet, lines are not merged',
              r.stdout == 'Intro line.\n- first point\n- second point\n', repr(r.stdout))

        piece = ("First line it's protected and I stay.\n\n"
                 "We don't think you'll see it. I checked 3 engines yesterday and Google named us. "
                 '"Don\'t touch this" he said. Email me@example.com or @handle or #tag. '
                 "The measurement happened quietly.\n")
        src.write_text(piece, encoding='utf-8')
        off = Path(d) / 'off.json'
        off.write_text(json.dumps({'apostrophe_drop': 0, 'lowercase': 0, 'typo_chance': 0, 'max_sentences_per_paragraph': 4}))
        r = run(str(src), '--tolerances', str(off), '--quiet')
        check('all knobs at zero leaves the text unchanged', r.stdout == piece, repr(r.stdout))

        full = Path(d) / 'full.json'
        full.write_text(json.dumps({'apostrophe_drop': 1, 'lowercase': 1, 'typo_chance': 0, 'max_sentences_per_paragraph': 4}))
        r = run(str(src), '--tolerances', str(full), '--seed', '1', '--quiet')
        out = r.stdout
        check('first line is never touched', out.startswith("First line it's protected and I stay.\n"))
        check('contraction apostrophes are dropped', "we dont think youll see it." in out, out)
        check('the pronoun I is lowercased', ' i checked 3 engines' in out, out)
        check('a number and its neighbours are kept', 'checked 3 engines' in out)
        check('a name is never lowercased', 'Google' in out)
        check('quoted words are never touched', '"Don\'t touch this"' in out)
        check('address, handle and hashtag survive', 'me@example.com' in out and '@handle' in out and '#tag' in out)
        check('an ordinary sentence start is lowercased', 'the measurement happened quietly.' in out, out)
        baseline = out

        typo = Path(d) / 'typo.json'
        typo.write_text(json.dumps({'apostrophe_drop': 1, 'lowercase': 1, 'typo_chance': 1, 'max_sentences_per_paragraph': 4}))
        r = run(str(src), '--tolerances', str(typo), '--seed', '1', '--quiet')
        a, b = baseline.split(), r.stdout.split()
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        check('typo pass changes exactly one word', len(a) == len(b) and len(diff) == 1, str(diff))
        if len(diff) == 1:
            x, y = diff[0]
            check('the typo is a swap of two adjacent letters in an ordinary word',
                  sorted(x) == sorted(y) and x.islower() and len(x) >= 6 and x.isalpha(), str(diff))
        r2 = run(str(src), '--tolerances', str(typo), '--seed', '1', '--quiet')
        check('same seed, same result', r.stdout == r2.stdout)
        r3 = run(str(src), '--tolerances', str(typo), '--seed', '1')
        check('every change is logged', r3.stderr.count('dice:') >= 4, r3.stderr)

        r = run('-', '--report', stdin='plain text, nothing wrong here.\n')
        check('a clean piece reports nothing and exits 0', r.returncode == 0 and '0 findings' in r.stdout, r.stdout)


def main() -> int:
    lint_files()
    test_script()
    print(('OK' if not FAILURES else 'FAILED'), f'({len(FAILURES)} failures)')
    return 1 if FAILURES else 0


if __name__ == '__main__':
    sys.exit(main())
