---
name: ask-docker-expert
description: Expert guidance on Docker, Docker Compose, and container optimization. Focuses on multi-stage builds and security.
---

## 1. Dockerfile Best Practices
When writing a `Dockerfile`:

*   **Multi-Stage Builds:** ALWAYS use multi-stage builds for compiled languages or Node.js apps to keep the final image small.
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
    CMD ["npm", "start"]
    ```
*   **Layer Caching:** Order instructions from least to most frequently likely to change. (Copy package.json and install deps BEFORE copying source code).
*   **Security:**
    *   Never run as root (use `USER node` or create a user).
    *   Pin base image versions (e.g., `node:18-alpine3.18`).

## 2. Docker Compose
*   **Versions:** Use valid Compose file syntax (no `version:` top-level key needed in newer specs, but `3.8` is safe if required).
*   **Services:**
    *   Use `healthcheck` for dependencies (e.g., waiting for DB).
    *   Use `.env` files for secrets (never hardcode passwords).

## 3. Debugging Containers
*   **Connectivity:** Suggest `docker network inspect` or `docker compose exec app curl db:5432` to test internal networking.
*   **Logs:** `docker logs -f <container_id>` is the first step.
*   **Shell Access:** `docker exec -it <container_id> /bin/sh` (or `/bin/bash`).

## 4. Optimization
*   **This skill is aggressive about image size.**
*   Suggest `.dockerignore` to exclude `node_modules`, `.git`, `Dockerfile`, etc.

## Trigger Phrases

Activate this skill when the user says things like:
- "Optimize this Dockerfile"
- "Debug container connectivity"
- "Create a multi-stage build"
- "Secure my Docker image"

