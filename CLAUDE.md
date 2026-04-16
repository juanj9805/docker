# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal **ASP.NET Core MVC** web application (targeting **.NET 10**) named `vps`. Its primary purpose is to serve as a learning project for containerizing a .NET app with Docker and deploying it to a VPS with a custom domain and SSL.

## Commands

```bash
# Run locally (Development)
dotnet run

# Build for release
dotnet publish -c Release -o ./out

# Build Docker image
docker build -t <image-name> .

# Run Docker container locally
docker run -d -p 8080:8080 --name <container-name> <image-name>

# List Docker images / running containers
docker images
docker ps
```

Local dev runs at `http://localhost:5026` (HTTP) or `https://localhost:7291` (HTTPS), as defined in [Properties/launchSettings.json](Properties/launchSettings.json).

## Architecture

Standard ASP.NET Core MVC layout — no custom layering yet:

- **[Program.cs](Program.cs)** — app entry point, middleware pipeline, and route registration. Uses the default `{controller=Home}/{action=Index}/{id?}` convention.
- **[Controllers/](Controllers/)** — MVC controllers. Currently only `HomeController`.
- **[Models/](Models/)** — view models. Currently only `ErrorViewModel`.
- **[Views/](Views/)** — Razor views (`.cshtml`). Layout is in `Views/Shared/_Layout.cshtml`.
- **[wwwroot/](wwwroot/)** — static assets (Bootstrap, jQuery, CSS, JS).

## Docker Setup

The [Dockerfile](Dockerfile) uses a **two-stage build**:
1. **Build stage** (`mcr.microsoft.com/dotnet/sdk:10.0`) — restores, compiles, and publishes.
2. **Runtime stage** (`mcr.microsoft.com/dotnet/aspnet:10.0`) — runs the published output.

The app listens on **port 8080** inside the container. Map it to the host with `-p 8080:8080`.

## Deployment Workflow

See [docs/pasos.md](docs/pasos.md) for the full deployment checklist:
1. Build and test locally
2. Push to GitHub
3. Clone on VPS and build the Docker image there
4. Configure DNS (dondominio) pointing to the VPS IP
5. Install SSL certificate
