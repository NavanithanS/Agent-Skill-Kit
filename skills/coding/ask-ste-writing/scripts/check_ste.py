#!/usr/bin/env python3
"""Check text against the core ASD-STE100 writing limits ("80% STE").

    python check_ste.py FILE [--procedural]
    some-command | python check_ste.py

Errors (exit 1):
  - sentence over 25 words (over 20 in list items, or everywhere with --procedural)
  - paragraph over 6 sentences
  - a word from the plain-word table (utilize -> use, ...)

Advisories (printed, never fail): possible passive voice, possible progressive tense.
These are regex heuristics, not grammar parsing, so they can be wrong.

Fenced code blocks, `inline code` and markdown table rows are ignored. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys

PROCEDURAL_LIMIT = 20
DESCRIPTIVE_LIMIT = 25
PARAGRAPH_LIMIT = 6

REPLACEMENTS = {
    r"utili[sz](e|es|ed|ing)": "use",
    r"prior to": "before",
    r"ensur(e|es|ed|ing)": "make sure",
    r"approximately": "about",
    r"commenc(e|es|ed|ing)": "start",
    r"in order to": "to",
    r"terminat(e|es|ed|ing)": "stop",
    r"subsequently": "then",
    r"replenish(es|ed|ing)?": "fill",
}

_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’/-]*")
_PASSIVE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+ed)\b", re.I)
_PROGRESSIVE = re.compile(r"\b(?:is|are|was|were)\s+(\w{3,}ing)\b", re.I)
_NOT_PROGRESSIVE = {"something", "nothing", "anything", "everything", "during", "string", "thing"}


def _strip_code(text: str) -> list[str]:
    """Return lines with fenced blocks blanked and inline code removed (line numbers kept)."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if line.strip().startswith(("```", "~~~")):
            in_fence = not in_fence
            lines.append("")
            continue
        if in_fence or line.lstrip().startswith("|"):  # code and table rows are not prose
            lines.append("")
        else:
            lines.append(re.sub(r"`[^`]*`", "code", line))
    return lines


def _blocks(lines: list[str]):
    """Yield (start_line, text, is_list_item). List items are their own blocks."""
    buf, start = [], 0
    for n, line in enumerate(lines, 1):
        is_heading = line.lstrip().startswith("#")  # headings end a paragraph and are not sentences
        if not line.strip() or is_heading or _LIST_ITEM.match(line):
            if buf:
                yield start, " ".join(buf), False
                buf = []
            if line.strip() and not is_heading:
                yield n, _LIST_ITEM.sub("", line), True
            continue
        if not buf:
            start = n
        buf.append(line.strip())
    if buf:
        yield start, " ".join(buf), False


def check(text: str, procedural: bool = False) -> tuple[list[str], list[str]]:
    errors, advisories = [], []
    for line_no, block, is_item in _blocks(_strip_code(text)):
        sentences = [s for s in _SENTENCE_END.split(block.strip()) if _WORD.search(s)]
        limit = PROCEDURAL_LIMIT if (procedural or is_item) else DESCRIPTIVE_LIMIT
        for s in sentences:
            words = len(_WORD.findall(s))
            if words > limit:
                errors.append(f"line {line_no}: sentence has {words} words (limit {limit}): {s[:60]}…")
        if not is_item and len(sentences) > PARAGRAPH_LIMIT:
            errors.append(f"line {line_no}: paragraph has {len(sentences)} sentences (limit {PARAGRAPH_LIMIT})")
        for pattern, plain in REPLACEMENTS.items():
            for m in re.finditer(rf"\b{pattern}\b", block, re.I):
                errors.append(f'line {line_no}: "{m.group(0)}" → use "{plain}"')
        for m in _PASSIVE.finditer(block):
            advisories.append(f'line {line_no}: possible passive voice: "{m.group(0)}"')
        for m in _PROGRESSIVE.finditer(block):
            if m.group(1).lower() not in _NOT_PROGRESSIVE:
                advisories.append(f'line {line_no}: possible progressive tense: "{m.group(0)}"')
    return errors, advisories


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", nargs="?", help="text or markdown file (default: stdin)")
    parser.add_argument("--procedural", action="store_true", help="apply the 20-word limit to every sentence")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    errors, advisories = check(text, procedural=args.procedural)
    for msg in errors:
        print(f"❌ {msg}")
    for msg in advisories:
        print(f"⚠️  {msg} (advisory)")
    if not errors:
        print("✅ STE check passed" + (f" with {len(advisories)} advisories" if advisories else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
