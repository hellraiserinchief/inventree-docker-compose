# InvenTree (Local Lab) — Minimal Stack

This is a *lean* InvenTree setup for local use on your LAN, no reverse proxy.
It exposes port **8000** on the host so you can browse to **http://<host-ip>:8000**.

## Quick Start

1) Install Docker + Docker Compose.
2) Copy `.env` (already present) and edit passwords if desired.
3) Start:
```bash
docker compose up -d
```
4) Open **http://localhost:8000** (or `http://<host-ip>:8000`) and create the admin user in the UI.
5) Generate an API token (User → Settings → Tokens).

### Seed the Maker Categories & Locations
1) Copy `.env.seed.example` to `.env.seed` and set:
   - `INVENTREE_URL=http://localhost:8000`
   - `INVENTREE_TOKEN=<your token>`
2) Run the seeder:
```bash
docker compose run --rm init-seed
```

### Backups
Nightly at **03:00** into `./backups` with rotation (7 daily, 4 weekly, 3 monthly).

### Updating
```bash
docker compose pull && docker compose up -d
```

When you're ready to put it behind OPNsense later, stop this stack, switch to your proxy setup, and remove the `ports:` section / add a reverse proxy.
