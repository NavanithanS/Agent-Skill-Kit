#!/usr/bin/env python3
"""Inject SEO front matter into each skill's README.md.

Without front matter, jekyll-seo-tag falls back to the site-wide description,
so every skill page on GitHub Pages shipped the identical meta description.
This gives each page a unique title and description sourced from skill.yaml.

Some READMEs already carry ASK front matter (`name:` + `description:`) but no
`title:`, and some descriptions exceed what Google will render. Those are
merged in place rather than skipped: `title:` is added, an over-long
`description` is trimmed, and every other key is preserved untouched.

Idempotent: re-running changes nothing once each README has a `title:` and a
`description` within the length limit.

    python3 scripts/add_skill_frontmatter.py [--check]

--check exits 1 if any README still needs work (for CI).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
SKILLS = ROOT / "skills"

# Google truncates meta descriptions around 155-160 characters.
MAX_DESCRIPTION = 155

AGENT_LABELS = {
    "claude": "Claude Code",
    "codex": "Codex",
    "gemini": "Gemini CLI",
    "cursor": "Cursor",
    "antigravity": "Antigravity",
}


# str.title() lowercases acronyms ("ast" -> "Ast"), which reads as a typo in a
# page title. Restore the ones that appear in skill names.
ACRONYMS = {
    "Ast": "AST", "Api": "API", "Pdf": "PDF", "Sql": "SQL", "Ui": "UI",
    "Ux": "UX", "Cli": "CLI", "Llm": "LLM", "Mcp": "MCP", "Adr": "ADR",
    "Db": "DB", "Owasp": "OWASP", "Http": "HTTP", "Json": "JSON",
    "Yaml": "YAML", "Ai": "AI", "Orm": "ORM", "Tdd": "TDD",
}


def humanize(name: str) -> str:
    """ask-ast-mapper -> AST Mapper"""
    words = re.sub(r"^ask[-_]", "", name).replace("_", "-").split("-")
    return " ".join(ACRONYMS.get(w.title(), w.title()) for w in words if w)


def first_h1(text: str) -> str | None:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


# An H1 that is really the slug ("ask-context-janitor") makes a poor page
# title, which is the exact problem this script exists to fix.
SLUG_H1_RE = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)+$")


def page_title(readme_text: str, name: str) -> str:
    """Human-readable heading for the page <title>, never a raw slug."""
    heading = first_h1(readme_text)
    if not heading or SLUG_H1_RE.match(heading):
        heading = humanize(name)
    else:
        # "Ask Commit Assistance" -> "Commit Assistance"; the product name is
        # already appended, so the prefix is pure duplication.
        heading = re.sub(r"^Ask\s+(?=\S)", "", heading)
    return heading


def truncate(text: str, limit: int = MAX_DESCRIPTION) -> str:
    """Trim to `limit` chars on a word boundary, without a dangling comma."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return f"{cut}…"


def strip_final_period(text: str) -> str:
    """Drop one sentence-final period, even behind a closing quote or bracket.

    A plain rstrip('.') is a no-op on a description ending `…"dead code."`,
    which then renders as `…"dead code.". For Codex…`.
    """
    return re.sub(r"\.(?=[\"'’”)\]]*$)", "", text.rstrip(), count=1)


def build_frontmatter(skill_yaml: Path, readme_text: str) -> dict:
    meta = yaml.safe_load(skill_yaml.read_text(encoding="utf-8")) or {}
    name = meta.get("name", skill_yaml.parent.name)

    title = f"{page_title(readme_text, name)} — Agent Skill Kit"

    # Collapse whitespace: a folded YAML description can carry newlines, which
    # would break the generated markdown table downstream.
    description = " ".join((meta.get("description") or "").split())
    agents = [AGENT_LABELS.get(a, a.title()) for a in meta.get("agents", [])]

    if not agents:
        return {"title": title, "description": truncate(description)}

    joined = ", ".join(agents[:-1]) + f" and {agents[-1]}" if len(agents) > 1 else agents[0]
    suffix = f"For {joined}."

    # Guard the empty case: without this an absent description yields the
    # malformed ". For Claude Code." with a leading full stop.
    if not description:
        return {"title": title, "description": truncate(suffix)}

    # The agent list is near-identical across skills, so it adds little to a
    # search snippet; the skill's own description is the part that makes the
    # page distinct. Append the list only when it fits whole — never truncate
    # the description to make room for it, and never clip the list itself into
    # a dangling fragment ("... For Antigravity, Gemini CLI, Claude…").
    combined = f"{strip_final_period(description)}. {suffix}"
    if len(combined) <= MAX_DESCRIPTION:
        return {"title": title, "description": combined}

    return {"title": title, "description": truncate(description)}


SUFFIX = " — Agent Skill Kit"


def is_weak_title(title: str) -> bool:
    """True for a title this script previously generated badly.

    Two shapes are worth rewriting: a raw slug ("ask-context-janitor"), and a
    redundant "Ask " prefix that duplicates the appended product name. A title
    a human wrote deliberately matches neither, so it is left alone.
    """
    heading = title[: -len(SUFFIX)] if title.endswith(SUFFIX) else title
    return bool(SLUG_H1_RE.match(heading.strip())) or heading.startswith("Ask ")


FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    """Return (parsed front matter or None, remaining body)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    try:
        parsed = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None, text
    if not isinstance(parsed, dict):
        return None, text
    return parsed, text[match.end():]


def render(front: dict) -> str:
    body = yaml.safe_dump(front, sort_keys=False, allow_unicode=True, width=10_000)
    return f"---\n{body}---\n\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report only; change nothing")
    args = parser.parse_args()

    changed, already_ok, missing_yaml, is_instruction_file = [], [], [], []

    for readme in sorted(SKILLS.glob("*/*/README.md")):
        # ask/utils/skill_registry.py falls back to README.md as a skill's
        # _instruction_file when SKILL.md is absent, and adapters deploy that
        # file to the agent. Adding SEO front matter to it would ship title/
        # description metadata into agent instructions, so leave those alone.
        # No skill hits this branch today; the guard keeps it that way.
        if not (readme.parent / "SKILL.md").exists():
            is_instruction_file.append(readme)
            continue

        text = readme.read_text(encoding="utf-8")
        existing, body = split_frontmatter(text)

        skill_yaml = readme.parent / "skill.yaml"
        if not skill_yaml.exists():
            missing_yaml.append(readme)
            continue

        generated = build_frontmatter(skill_yaml, body if existing else text)

        if existing is None:
            front, needs_write = generated, True
        else:
            # Preserve every existing key; only fill a missing title and trim
            # a description that is too long to render in a search result.
            front = dict(existing)
            needs_write = False
            if not front.get("title") or is_weak_title(str(front["title"])):
                if front.get("title") != generated["title"]:
                    front["title"] = generated["title"]
                    needs_write = True
            # Only fill an absent description. An existing one is repo source
            # of truth, and MAX_DESCRIPTION is a search-result *display* limit
            # — Google clips long descriptions harmlessly at render time.
            # Rewriting the file to fit that limit destroys real content.
            current = str(front.get("description") or "").strip()
            if not current:
                front["description"] = generated["description"]
                needs_write = True
            # Put title first so the file reads naturally.
            front = {k: front[k] for k in (["title"] + [x for x in front if x != "title"])}

        if not needs_write:
            already_ok.append(readme)
            continue

        changed.append(readme)
        if not args.check:
            readme.write_text(render(front) + body.lstrip("\n"), encoding="utf-8")

    if args.check:
        for readme in changed:
            print(f"needs front matter: {readme.relative_to(ROOT)}")
        for readme in missing_yaml:
            print(f"no skill.yaml:      {readme.relative_to(ROOT)}")
        for readme in is_instruction_file:
            print(f"skipped (is the deployed instruction file): {readme.relative_to(ROOT)}")
        if changed or missing_yaml:
            return 1
        print(f"✅ all {len(already_ok)} skill READMEs have a title and a valid description")
        return 0

    print(f"✅ updated {len(changed)} README(s); {len(already_ok)} already correct")
    for readme in is_instruction_file:
        print(f"   ↷ skipped (serves as the deployed instruction file): {readme.relative_to(ROOT)}")
    for readme in missing_yaml:
        print(f"   ⚠️  skipped (no skill.yaml): {readme.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
