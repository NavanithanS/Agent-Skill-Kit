---
name: ask-docker-expert
description: Docker and Docker Compose optimization. Multi-stage builds, security, debugging.
triggers: ["optimize dockerfile", "debug container", "multi-stage build", "secure docker"]
---

<critical_constraints>
❌ NO running as root → use `USER node` or create user
❌ NO unpinned base images → `node:18-alpine3.18`
❌ NO hardcoded secrets → use .env files
✅ MUST use multi-stage builds for compiled/Node.js apps
✅ MUST use .dockerignore (exclude node_modules, .git)
</critical_constraints>

<multi_stage_template>
```dockerfile
# Build Stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production Stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./
RUN npm install --production
USER node
CMD ["npm", "start"]
```
</multi_stage_template>

<layer_caching>
Order: least → most frequently changed
1. Copy package.json, install deps
2. THEN copy source code
</layer_caching>

<compose>
- Use healthcheck for dependencies
- Use .env for secrets
- Version 3.8 if required
</compose>

<debugging>
- Connectivity: `docker compose exec app curl db:5432`
- Logs: `docker logs -f <container_id>`
- Shell: `docker exec -it <container_id> /bin/sh`
</debugging>
