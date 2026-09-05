# Log

Append-only chronological record. Format: `## [YYYY-MM-DD] <action> | <subject>`

---

## [2026-04-06] ingest | Initial wiki creation

Bootstrap from codebase scan. Created: SCHEMA.md, overview.md, concepts/adapter-pattern.md, entities/skill.md, skills-catalog.md, index.md, log.md.

Sources: agents/base.py, ask/utils/skill_registry.py, CLAUDE.md, skills/** yaml inventory, agents/** adapter listing.

## [2026-04-11] ingest | Documented Release Protocol

Added `concepts/release-protocol.md` to ensure future agents update all hidden version references (Homebrew, init.py, etc.) during version bumps. Updated index.

## [2026-05-24] update | Added remote registries & diff viewer

Implemented `ask install <url>` to support remote Git-backed skill registries. Improved conflict resolution across CLI commands (`ask copy`, `ask update`, `ask install`) with an interactive `[v]iew diff` option. Hardened `skill_registry.py` to support scanning single-level directories for remote skills. Reduced token footprint of `ask-commit-assistance`, `ask-impact-sentinel`, and `ask-shadcn-mechanic` to satisfy linter constraints.

## [2026-05-30] update | Added `ask test` Layer 1 (trigger/collision audit)

Built the offline half of the skill eval harness. New `ask/utils/eval/` package with a pure-stdlib TF-IDF cosine ranker (`trigger_scorer.py`) and `ask/commands/test.py` exposing `ask test`. It audits each skill's `tests/evals.yaml` (`should_fire` prompts) against the whole library and flags **collisions** — similar skills competing for the same prompt — rather than claiming absolute routing accuracy, which is honestly framed as a lexical pre-screen (real accuracy is Layer 2's `--behavior`, still stubbed). Supports `--strict` (CI gate), `--json`, `--margin`, and per-skill scoping. Demo evals added to the laravel/vue architect+mechanic pairs; the audit correctly surfaces architect↔mechanic collisions. 7 new tests; suite 30→37. See `concepts/eval-harness.md`.

## [2026-05-30] update | Added `ask mcp serve` (MCP server, provider model)

Exposed the skill library to MCP-capable agents so they can discover/pull skills at runtime. Read-only *provider, not installer* design — no filesystem mutation. New `ask/utils/provider.py` (pure, testable: `list_skills_payload`/`search_skills_payload`/`get_skill_payload`), `ask/mcp_server.py` (thin FastMCP wrapper, `mcp` as optional `[mcp]` extra), and `ask/commands/mcp_cmd.py` (`ask mcp serve` / `tools` / `probe`). `search_skills` reuses the `ask test` TF-IDF index so search and trigger audit agree on skill topics. 8 new tests; suite 37→45. See `concepts/mcp-server.md`.

## [2026-07-15] update | Added `ask-wiki-init` and `ask-hold-code` skills

Created `ask-wiki-init` (tooling) to scaffold the LLM Wiki pattern and `ask-hold-code` (planning) to enforce a planning-mode lock. Refactored both to strictly follow the Gold Standard architecture from `ask-skill-creator` (extracted config, added identity/persona). Updated `README.md` to reflect 42 total skills.

## [2026-08-02] update | v0.9.1 Release: Database Indexing & Safe Copy Fix

Bumped version to 0.9.1. Enhanced `ask-impact-sentinel` with a mandatory Database Indexing Review protocol to systematically audit query paths and suggest migration scripts. Fixed a hardcoded `force=True` parameter in `ask copy` that violated the Safe Copy protocol when installing sidecar resources (`config/`, `scripts/`, etc.). Introduced a legacy path migration script for `AntigravityAdapter` to move old `.agent` installations to `.agents`.

## [2026-08-02] lint | Full wiki sync audit

Comprehensive lint pass auditing all wiki pages against codebase state at v0.9.1. Corrections:

- **skills-catalog.md**: Fixed coding count 25→26 (missing `ask-flutter-architect`). Removed duplicate `ask-parallel-auditor` row. Fixed tooling count 11→10. Added missing `workflows/` category with `skill-creator`. Updated date.
- **overview.md**: Rewrote to reflect v0.9.1 — added all 15 CLI commands, USoT mention, `workflows/` category, Antigravity local/global paths, accurate skill counts (42 total).
- **concepts/adapter-pattern.md**: Documented v0.9.1 sidecar resource expansion (10 resource types), legacy path migration (`.agent`→`.agents`, `~/.gemini/antigravity`→`~/.gemini/config`), `remove_skill()` and `install()` methods, dynamic loader `inspect.signature` detail, fixed broken link to non-existent `entities/skill-add-agent.md`.
- **entities/skill.md**: Added `workflows/` to category table, `evals.yaml` to Gold Standard structure, `config/` and `resources/` directories, `ask install` to lifecycle, updated date.
- **concepts/release-protocol.md**: Added `manifest.json` and `README.md` to version bump checklist.
- **[NEW] concepts/usot-pattern.md**: Created concept page for USoT + symlink architecture — the core pattern since v0.5.0 that was entirely undocumented.
- **index.md**: Added `usot-pattern.md` entry, updated skill count references, added missing `llm-wiki.md` link, and significantly expanded the context descriptions for all listed files.
- **llm-wiki.md**: Added missing YAML frontmatter and contextualized introduction per schema.
- **SCHEMA.md**: Removed reference to non-existent `decisions/` directory in directory layout.

Sources: agents/base.py, agents/antigravity/adapter.py, ask/commands/copy.py, ask/utils/filesystem.py, ask/cli.py, skills/** directory listing, CHANGELOG.md, pyproject.toml.


## [2026-09-05] update | Search discoverability: Pages config, SEO metadata, generated docs

Implemented Phases 1–3 of the search-visibility plan after an audit found **zero pages indexed by Google** on both `github.com/NavanithanS/Agent-Skill-Kit` and `navanithans.github.io` (verified with live `site:` queries in a browser; search APIs silently ignore the `site:` operator). The repo also had `repositoryTopics: null`, `licenseInfo: null`, and no `_config.yml`, so Jekyll was publishing all ~400 markdown files with one shared meta description.

Changes:

- **[NEW] `_config.yml`** — enables `jekyll-sitemap` (site had no `sitemap.xml`), sets explicit `url`/`baseurl` (required: Pages previously auto-derived `baseurl`, and omitting it would strip `/Agent-Skill-Kit` from every canonical), carries `google_site_verification`, and excludes 27 paths. Exclusions cover agent instruction files, `wiki/`, source dirs, per-skill `tests|scripts|assets|resources|reference|references`, and `SKILL.md` (which duplicated each skill's `README.md` page at `/SKILL`).
- **[NEW] `scripts/add_skill_frontmatter.py`** — gives all 42 skill READMEs a unique `title:` and ≤155-char `description:` from `skill.yaml`. Guards: skips any README that serves as a skill's `_instruction_file` (no `SKILL.md`), since adapters deploy that file to agents; humanizes slug-like H1s; strips redundant `Ask ` prefixes; restores acronyms.
- **`scripts/generate_site.py`** — added canonical/OG/Twitter/verification tags to the generated `<head>`, plus a server-rendered static skill index (docs page went from **162 → 880** crawlable words with 42 real internal links). New `generate_skill_index()` writes `skills/README.md` as a crawlable hub; new `sync_readme_table()` maintains the README table between `SKILLS:START/END` markers.
- **[NEW] `LICENSE`** (MIT — was declared in `pyproject.toml` but absent, so GitHub reported no license, blocking directory submissions), **`CITATION.cff`**, **`robots.txt`**.
- **`pyproject.toml`** — added `[project.urls]` (PyPI is the only page-1 result for the brand phrase and linked nowhere: `home_page: None`, `project_urls: None`), author email, expanded keywords.
- **`README.md`** — restructured opening (changelog moved below the fold; content verified preserved in `CHANGELOG.md`), added the generated 42-row skill table.
- **`.github/workflows/docs.yml`** — now commits `skills/README.md` and `README.md`. The existing `[skip ci]` prevents the `skills/**` trigger from looping.
- **4 new skill READMEs** — `ask-owasp-security-review`, `ask-hold-code`, `ask-smart-booking-test`, `ask-wiki-init` had none.
- **[NEW] `concepts/site-and-seo.md`**, indexed in `index.md`.

Corrections to existing wiki content:

- **skills-catalog.md**: `workflows/` was recorded as holding 1 skill (`skill-creator`). It holds **none** — that directory has no `skill.yaml` and no `SKILL.md`, is not registered by `SkillRegistry`, and is absent from `manifest.json` (42, not 43). Marked superseded; the directory remains unresolved (delete or promote).

Bugs found and fixed during review (two reviewer passes plus an independent code review):

- **`generate_site.py` had a backslash inside an f-string expression** — a hard `SyntaxError` on Python 3.9–3.11, which `ci.yml` tests and `requires-python` declares. Both scripts now verified compiling *and running* on 3.9/3.10/3.11/3.12.
- **Front matter destroyed repo content.** An earlier revision truncated any `description` over 155 chars *in the file*, silently dropping a sentence from `ask-effective-llm-coder`, `ask-shadcn-mechanic`, `ask-brainstorm` and `ask-solution-architect`. Restored from HEAD; the script now only fills an *absent* description, since 155 is a display limit, not a storage limit.
- **The agent-list suffix was appended before truncation**, so it was clipped first — 19 generated descriptions ended in a dangling `… For Antigravity, Gemini CLI, Claude…`. The suffix is now appended only when the whole string fits.
- **`sync_readme_table`'s failure was silent** — its boolean return was discarded while `docs.yml` committed `README.md` unconditionally, so a removed marker would ship a stale table behind a green build. Now exits non-zero (verified).
- **`--check` was documented "for CI" but no workflow ran it.** Wired into `ci.yml`; `docs.yml` now also runs the script itself so a newly added skill gets metadata automatically.
- Smaller: empty-description produced a malformed `". For Claude Code."`; `rstrip('.')` was a no-op on descriptions ending `…"dead code."`, yielding `.".`; folded YAML newlines could break the markdown table; README marker ordering was unguarded; `str.title()` lowercased acronyms (`Ast Mapper`).

Method note: the first content-preservation check excluded the `description` field as "intentionally changed", which is exactly why the data loss above went unnoticed for two passes. The check now covers every field.

Verification: `ask validate` 42/42 · `pytest` 47/47 · `python -m build` OK · generators idempotent · all 42 READMEs carry a unique title and valid description · non-description front-matter keys and README bodies byte-identical to HEAD.

Not done (requires owner action): Search Console verification, GitHub topics/description, social preview image, PyPI release.

Sources: _config.yml, scripts/generate_site.py, scripts/add_skill_frontmatter.py, ask/utils/skill_registry.py, agents/*/adapter.py, .github/workflows/{docs,ci,release}.yml, pyproject.toml, live Google SERPs.

## [2026-09-05] update | v0.10.0 Release: Making the Library Findable

Version bumped 0.9.1 → 0.10.0. Chosen over a patch bump because the release adds a subsystem (Jekyll/SEO site generation, front-matter tooling, a CI gate) rather than fixing behaviour; PyPI versions cannot be reused, so under-numbering is the harder error to undo. No CLI commands, flags or skill formats changed — upgrading needs no migration.

Files bumped: `pyproject.toml`, `CITATION.cff`, `agent-skill-kit.rb` (url + version + test assertion), `Formula/agent-skill-kit.rb`, `wiki/overview.md`, `wiki/index.md`. Written: `CHANGELOG.md` [0.10.0], `RELEASE_NOTES.md` v0.10.0, `TWEET.md`.

Two pre-existing defects fixed as part of the release:

- **`ask/__init__.py` version drift.** The file assigned a hardcoded `__version__` *inside* a `try:` / `except PackageNotFoundError:` block — the literal can never raise, so the branch was dead and the imported `version()` was unused. `ask --version` was therefore a hand-synced string, exactly the drift the release protocol was written to police. Now reads `importlib.metadata.version("agent-skill-kit")`; verified reporting `0.10.0` after `pip install -e .`. `__author__` also corrected from `"Nava"` to `"Navanithan S"` for consistency with `CITATION.cff` and `pyproject.toml`.
- **`RELEASE_NOTES.md` was off by one release.** Its `## v0.9.1` section carried v0.9.0's content and date (May 24, 2026 — Remote Registries & Diff Viewer), while `CHANGELOG.md` correctly dated 0.9.1 to 2026-08-02. Renamed that section to v0.9.0 and wrote a correct v0.9.1 entry from the changelog, with a `> **Corrected:**` note. Heading sequence now matches CHANGELOG with no duplicates or gaps.

`concepts/release-protocol.md` updated from what following it actually revealed: `ask/__init__.py` no longer needs a manual bump (with a warning not to reintroduce the hardcode), `CITATION.cff`, `TWEET.md` and the two wiki version references added to the checklist, the README skill table marked generated, a note that hits in CHANGELOG/RELEASE_NOTES/log are history and must not be rewritten, and a Publishing section recording that `release.yml` automates PyPI + the Homebrew tap on `release: published` — so a release is tagged, never `twine`d by hand.

Sources: pyproject.toml, ask/__init__.py, ask/cli.py, agent-skill-kit.rb, Formula/agent-skill-kit.rb, CHANGELOG.md, RELEASE_NOTES.md, .github/workflows/release.yml, skills/manifest.json.

## [2026-09-05] update | Fix: `plugins:` in _config.yml dropped GitHub Pages defaults

The v0.10.0 `_config.yml` listed only `jekyll-sitemap` and `jekyll-seo-tag` under `plugins:`. On GitHub Pages that key **replaces** the default plugin set rather than extending it, so `jekyll-readme-index` was silently dropped and `README.md` stopped rendering as each directory's `index.html`.

Live effect: `/skills/<category>/<skill>/` returned 404 while `/skills/<category>/<skill>/README.html` returned 200 — breaking roughly 127 internal links across the README skill table, the generated `skills/README.md` hub, and the docs static index. `jekyll-titles-from-headings` and `jekyll-relative-links` were dropped the same way.

The failure was not obvious because the parts that were checked all passed: `sitemap.xml` returned 200, canonicals carried the correct `/Agent-Skill-Kit` prefix, and the excluded junk pages 404'd as intended. The tell was the sitemap listing `.../README.html` rather than the clean directory URL.

Fix: `_config.yml` now lists all nine GitHub Pages defaults alongside the two opt-ins, with a warning comment. `concepts/site-and-seo.md` gained a section documenting the replace-not-extend semantics.

Root cause of the miss: the config could not be validated locally (no Jekyll toolchain), and the post-deploy verification checked sitemap/canonical/exclusions but never asserted that a generated internal link actually resolved. Link resolution is now part of the documented verification step.

Sources: _config.yml, live navanithans.github.io/Agent-Skill-Kit responses, sitemap.xml.

## [2026-09-05] update | Fix (part 2): readme_index must allow front matter

Restoring the GitHub Pages default plugin list did **not** fix the 404s on `/skills/<category>/<skill>/`. Pages rebuilt cleanly (build `1cbfd6a5`, status `built`, no error) and the URLs still 404'd with 43 `README.html` entries in the sitemap.

Actual root cause: `jekyll-readme-index` skips any `README.md` carrying YAML front matter — its documented default. Every skill README gained front matter in v0.10.0 for per-page titles and descriptions, so the plugin ignored all 42.

Two independent conditions had been making the clean URLs work, and the v0.10.0 SEO work broke both simultaneously:

1. No `_config.yml` existed, so the Pages default plugins (including `jekyll-readme-index`) were active — broken by adding a `plugins:` list.
2. Skill READMEs had no front matter, so the plugin processed them — broken by adding `title:`/`description:`.

Fixing only the first left the second violated, which is why the earlier fix appeared to fail. `_config.yml` now sets `readme_index: {with_frontmatter: true}` alongside the restored plugin list; both keys are required and neither is sufficient alone.

Diagnostic note: the first fix was pushed and verified as *deployed* (Pages API build status + `Last-Modified` matching the build) before concluding it was ineffective, rather than assuming a propagation delay. That distinction is what isolated the second cause.

Sources: _config.yml, jekyll-readme-index documented defaults, GitHub Pages builds API, live sitemap.xml.

## [2026-09-05] update | Search Console verified, sitemap accepted — Day-0 baseline recorded

The technical SEO track from the discoverability audit is complete and verified against the live site.

Verified live:
- `/skills/<category>/<skill>/` returns 200 (clean directory URLs, `jekyll-readme-index` working with front matter)
- `sitemap.xml` returns 200 `application/xml`, well-formed `urlset`, 50 entries, 0 duplicates, all correctly prefixed, 0 `README.html` entries
- Per-page `<title>` and `<meta description>` unique per skill; titles no longer duplicate the product name
- `CLAUDE.md`, `AGENTS.md`, `TWEET.md` and duplicate `SKILL` pages all 404 as intended
- Search Console ownership verified via HTML file at the property root; sitemap submitted and accepted

Two false alarms worth recording, both caused by a **leading slash** against a path-scoped property (`https://navanithans.github.io/Agent-Skill-Kit/`), which resolves to the host root — a path this project does not control and which 404s:

- HTML verification file reported "not found in the required location" when it was live and byte-correct. Actual cause was a race: the file went live at 01:46:55 GMT and Verify was clicked at 01:47:54, inside GitHub's `max-age=600` CDN window, so Google's fetcher saw a cached 404. Retrying after propagation succeeded.
- Sitemap reported "Couldn't fetch" when submitted as `/sitemap.xml`. Resubmitting as `sitemap.xml` (no leading slash) succeeded.

**Rule for this property: never use a leading slash in Search Console inputs.** The field is already prefixed with the property URL.

Day-0 baseline (2026-09-05, for measuring the 30/60/90 targets):

| Metric | Value |
|---|---|
| Google pages indexed | 0 |
| Sitemap URLs submitted | 50 |
| GitHub stars / forks | 1 / 1 |
| GitHub topics | 11 (added same day) |
| GitHub traffic, 14d | 8 views / 7 uniques |
| License detected | MIT (was: none) |

**Phase 1 of the audit is complete as of this date.** Repository description rewritten (was the keyword-free tagline "Create once. Share across agents"), `homepageUrl` repointed from `/docs/` to the root landing page, MIT `LICENSE` detected, and 11 topics added: `agent-skills`, `ai-agents`, `claude-code`, `cli`, `codex`, `cursor`, `developer-tools`, `gemini-cli`, `mcp`, `python`, `skill-management`.

Topics matter disproportionately here because Search Console cannot cover `github.com` — the repository can only be reached by crawlers through inbound links, and GitHub topic hubs are the most heavily crawled source available. `topic:agent-skills` alone indexes over 21,000 repositories.

Gotcha for future runs: `gh api -f 'names[]=...'` must be **single-quoted** in zsh, which otherwise treats `[]` as a glob and fails with `no matches found` before `gh` is invoked. The `--input -` heredoc form avoids the problem entirely and is preferred.

Remaining from the audit: Phase 6 (directory and awesome-list submissions, now unblocked by the license), the differentiator content of Phase 5, and the Day-30 gate that decides the naming question (T-2.4).

Sources: live navanithans.github.io responses, Google Search Console, GitHub repo + traffic APIs.
