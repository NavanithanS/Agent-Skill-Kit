🚨 Agent Skill Kit v0.10.0 is out! 🚀

This one has no new commands. I audited why nobody could find ASK and got an uncomfortable answer: **zero pages indexed by Google.** Not ranking badly — not indexed at all.

Turns out the repo had no `_config.yml`, so GitHub Pages was publishing ~400 files with no sitemap and *one shared meta description* across every skill page. The docs page built its whole skill list in JS, so crawlers saw 162 words. And the MIT license was declared in `pyproject.toml` but the LICENSE file didn't exist, so GitHub called it unlicensed.

Fixed in v0.10.0:
🗺️ Real sitemap.xml + 275 junk pages excluded
🏷️ Unique title/description per skill, enforced in CI
🔗 Docs page: 162 → 880 crawlable words, 42 real links
📄 LICENSE added, PyPI now links back to the docs

Also fixed a fun one: `ask --version` read a hardcoded string inside a `try/except` that could never fire. It reads real package metadata now.

If you maintain an open-source project, go run `site:yourdomain` on Google. You may not like the answer.

👉 https://navanithans.github.io/Agent-Skill-Kit/

#AI #LLMs #AgentSkillKit #DeveloperTools #SEO
