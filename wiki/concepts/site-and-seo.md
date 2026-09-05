---
title: Pages Site & Search Discoverability
type: concept
tags: [jekyll, github-pages, seo, generate-site, frontmatter, sitemap]
updated: 2026-09-05
sources: 6
---

# Concept: Pages Site & Search Discoverability

How `navanithans.github.io/Agent-Skill-Kit/` is built, which files become public
pages, and the constraints that keep it discoverable. Read this before touching
`_config.yml`, `scripts/generate_site.py`, or any skill `README.md`.

## The two build systems

The site is produced by **two independent pipelines** that must not be confused:

| Pipeline | Builds | Trigger |
|---|---|---|
| **Jekyll** (GitHub Pages, `build_type: legacy`) | Every non-excluded markdown file in the repo, from `master` root | Any push |
| **`scripts/generate_site.py`** | `docs/index.html`, `skills/README.md`, and the README skill table | `.github/workflows/docs.yml` |

Because Pages serves from the **repo root** (`source: {branch: master, path: "/"}`),
every markdown file is a candidate public page. That is why `_config.yml` has a
large `exclude:` list rather than a small one.

## Generated files — never hand-edit

`scripts/generate_site.py` overwrites these on every run, and `docs.yml`
regenerates and auto-commits them:

- `docs/index.html` — edit the template in `generate_site.py` (`generate_index_page`), not the output
- `skills/README.md` — edit `generate_skill_index()`
- The `README.md` block between `<!-- SKILLS:START -->` and `<!-- SKILLS:END -->` — edit `sync_readme_table()`

Everything in `README.md` outside those markers is hand-written and preserved.

## Why the exclusions matter

Three classes of file would otherwise publish as low-quality pages:

1. **Agent instruction files** — `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `TWEET.md`
2. **Per-skill support files** — `tests/`, `scripts/`, `assets/`, `resources/`, `reference/`, `references/`
3. **`SKILL.md`** — renders at `/skills/<cat>/<skill>/SKILL`, duplicating the
   `README.md`-derived page at `/skills/<cat>/<skill>/`

`README.md` is deliberately the canonical page for a skill: cleaner URL, human
prose, and it is the one that gets indexed. `SKILL.md` is instruction-shaped and
reads badly as a landing page.

> **When adding a new per-skill directory type, add it to `exclude:` in
> `_config.yml`** or it will publish as an orphan page.

## Two settings that are load-bearing

- **`url` + `baseurl`** — before `_config.yml` existed, Pages auto-derived
  `baseurl` and `jekyll-seo-tag` emitted correct canonicals as a side effect.
  Removing either key strips the `/Agent-Skill-Kit` prefix from every canonical
  URL and sitemap entry.
- **`google_site_verification`** — `jekyll-seo-tag` renders this into every page
  head. Removing it revokes Search Console ownership.

`jekyll-seo-tag` (already active) also emits JSON-LD, Open Graph and Twitter
tags, so structured data needs no separate work. The gap it cannot fill is
**per-page titles and descriptions** — hence the front-matter script below.

## Skill README front matter

`scripts/add_skill_frontmatter.py` gives every skill page a unique `title:` and
a ≤155-character `description:`, sourced from `skill.yaml`. Without it every
page inherits the site description and Google sees ~400 identical snippets.

Four constraints the script encodes, all easy to reintroduce by accident:

- **It skips a `README.md` when the directory has no `SKILL.md`.**
  `ask/utils/skill_registry.py` falls back to `README.md` as a skill's
  `_instruction_file`, and adapters deploy that file to the agent — so SEO
  front matter would leak into agent instructions.
- **It never rewrites an existing `description`.** `MAX_DESCRIPTION` (155) is a
  search-result *display* limit; Google clips longer text harmlessly at render
  time. Truncating the file to fit destroys repo content — an earlier revision
  did exactly that and silently dropped a sentence from four skill READMEs.
  The script only fills an *absent* description.
- **The agent list is appended only when it fits whole.** The suffix
  (`For Claude Code, Codex, … and Antigravity.`) runs ~55 characters and is
  near-identical across skills, so it adds little to a snippet while the
  skill's own description is what makes the page distinct. Appending first and
  truncating afterwards clips the *suffix*, leaving a dangling
  `… For Antigravity, Gemini CLI, Claude…` in the rendered result.
- **Titles are never raw slugs.** An H1 that is just `ask-context-janitor`
  is humanized (`Context Janitor`), a redundant `Ask ` prefix is dropped, and
  acronyms are restored (`Ast` → `AST`).

Run `python3 scripts/add_skill_frontmatter.py --check` as a CI gate; it exits 1
when a README needs work.

## Verifying a deploy

A failed Jekyll build **silently keeps serving the last good version** — there
is no error page. After pushing a change to `_config.yml`, check
Settings → Pages for a build-failure banner, then:

```bash
B=https://navanithans.github.io/Agent-Skill-Kit
curl -s -o /dev/null -w "%{http_code}\n" $B/sitemap.xml    # 200
curl -s $B/sitemap.xml | grep -c "<loc>"                   # ~45, not ~400
curl -s $B/skills/coding/ask-unit-test-generation/ | grep canonical
curl -s -o /dev/null -w "%{http_code}\n" $B/skills/coding/ask-unit-test-generation/SKILL  # 404
```

If `sitemap.xml` 404s, remove the `plugins:` key first — legacy Pages loads
both allowlisted plugins from its default set regardless.

## Known limitation: robots.txt

`robots.txt` lives at the repo root and therefore serves at
`/Agent-Skill-Kit/robots.txt`. **Crawlers only read `robots.txt` at the host
root** (`navanithans.github.io/robots.txt`), which belongs to a user-pages repo
that does not exist. The file is effectively inert; the sitemap reaches Google
through **Search Console submission**, not through that file. It becomes live
if a custom domain is ever added.

## Related

- [adapter-pattern.md](adapter-pattern.md) — what adapters deploy, and why `README.md` is not among the copied resources
- [entities/skill.md](../entities/skill.md) — the skill directory contract
- [release-protocol.md](release-protocol.md) — version-bump checklist
