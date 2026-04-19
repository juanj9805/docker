# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ASP.NET Core MVC web application (**.NET 10**) named `vps`. Learning project for Docker containerization and VPS deployment with custom domain and SSL.

## Commands

```bash
# Run locally
dotnet run

# Build for release
dotnet publish -c Release -o ./out

# EF Core migrations
dotnet ef migrations add <MigrationName>
dotnet ef database update

# Build Docker image
docker build -t <image-name> .

# Run container locally (requires DB env vars)
docker run -d -p 8080:8080 \
  -e DB_SERVER=... -e DB_NAME=... -e DB_USER=... -e DB_PASSWORD=... \
  --name <container-name> <image-name>
```

Local dev runs at `http://localhost:5026` / `https://localhost:7291` (see `Properties/launchSettings.json`).

## Architecture

Standard MVC — no service/repository layer yet. Direct `DbContext` injection into controllers.

- **`Program.cs`** — middleware pipeline, registers `MysqlDbContext` via `AddDbContext<MysqlDbContext>()`. Default route: `{controller=Home}/{action=Privacy}/{id?}`.
- **`Data/MysqlDbContext.cs`** — EF Core context using Pomelo MySQL driver. Connection string built from env vars (`DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). Config lives in `OnConfiguring`, not `appsettings.json`.
- **`Models/Event/Event.cs`** — domain model with `Status` enum (`Active`, `Inactive`, `Deleted`). `CreateAt` has a DB-level default of `CURRENT_TIMESTAMP`.
- **`Controllers/EventController.cs`** — CRUD controller for `Event`. All DB calls must be `async` (`ToListAsync`, `SaveChangesAsync`, etc.).
- **`Views/Event/`** — Razor views: `Index`, `Create`, `Edit`, `Show`, `Destroy`. Note: view names `Show`/`Destroy` deviate from ASP.NET convention (`Details`/`Delete`) — keep consistent with existing names when adding views.

## Database

MySQL via **Pomelo.EntityFrameworkCore.MySql**. Migration already applied: `InitialMigration` creates the `Events` table. Run `dotnet ef database update` after pulling new migrations.

## Docker Setup

Two-stage Dockerfile: SDK image builds/publishes, ASP.NET runtime image runs the output. App listens on **port 8080** inside the container.

## Deployment Workflow

See [docs/pasos.md](docs/pasos.md):
1. Build and test locally
2. Push to GitHub
3. Clone on VPS, build Docker image there
4. Configure DNS (dondominio) → VPS IP
5. Install SSL certificate
