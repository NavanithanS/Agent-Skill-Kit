---
name: ask-readme-gardener
description: Keep README.md in sync with code changes (APIs, features).
triggers: ["update readme", "document api", "sync docs", "add to docs"]
---

<critical_constraints>
✅ MUST maintain existing README style and headers
✅ MUST identify correct section (API Reference, Usage, Features)
✅ MUST document: method, URL, parameters, response for endpoints
</critical_constraints>

<workflow>
1. **Analyze**: Understand new feature, API, or change
2. **Locate**: Find relevant section in README.md
3. **Draft**: Write update matching existing style
4. **Update**: Edit README.md directly
</workflow>

<api_template>
```markdown
### GET /status
Returns the current system status.

**Response**
```json
{ "status": "ok", "uptime": 1234 }
```
```
</api_template>

<patterns>
- New endpoint → add to API Reference with method, URL, params, response
- Modified feature → update existing description
- New feature → add bullet or section describing usage
</patterns>
