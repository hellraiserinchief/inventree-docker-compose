# InvenTree (Local Lab) — Minimal Stack

This is a *lean* production ready InvenTree setup.

It exposes port **8080** on the host so you can browse to **http://<host-ip>:8080**.

TLS etc is the responsibility of the gateway/proxy server that connects to **http://<host-ip>:8080**

## Quick Start

1) Install Docker + Docker Compose.
2) Copy `.env` (already present) and edit usernames/passwords/urls.
3) Start:
```bash
docker compose up -d
```
4) Open `http://<host-ip>:8080` and create the admin user in the UI.
5) Generate an API token (User → Settings → Tokens).

### Seed the Maker Categories & Locations
1) Copy `.env.seed.example` to `.env.seed` and update url/token
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
