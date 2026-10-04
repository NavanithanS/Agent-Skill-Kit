## Release post

🚨 Agent Skill Kit v0.10.1 is out! 🚀

Agents write more of our code now. So our job shifts to reading what they made. @karpathy had a great post on this, and this release turns two of its ideas into skills.

✍️ New: ask-ste-writing
Agent prose in ~80% ASD-STE100, the controlled English of aircraft maintenance manuals. Max 20 words per instruction, active voice, one meaning per word. Comes with a checker script.

🗺️ ask-explaining-code 1.1.0
Picks the format: prose → diagram → a throwaway HTML explainer of your diff. No more ASCII art for a one-liner.

Also fixed: skill pages that 404'd after v0.10.0, and a Homebrew checksum that could never match.

pip install --upgrade agent-skill-kit

👉 https://navanithans.github.io/Agent-Skill-Kit/

#AI #LLMs #AgentSkillKit #DeveloperTools

---

## Quote post

Quote: https://x.com/karpathy/status/2105819303471976479

Turned this into two open agent skills (Claude Code, Codex, Gemini CLI, Cursor):

✍️ ask-ste-writing: agent prose in ~80% ASD-STE100
🗺️ ask-explaining-code: prose → diagram → throwaway HTML explainer

pip install agent-skill-kit
ask copy claude --skill ask-explaining-code
