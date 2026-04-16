# What Docker is doing in this project

The core problem Docker solves here: **your machine has .NET 10 installed, the VPS might not — and even if it did, versions could differ and things would break.**

Docker packages the app *with everything it needs to run*, so the VPS just needs Docker installed, nothing else.

---

## The Dockerfile, line by line

```dockerfile
# ── STAGE 1: Build ──────────────────────────────────────
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
```
Pulls a Microsoft image that has the full **.NET SDK** (compiler, CLI, build tools). This stage is only used to produce the compiled output — it never runs in production.

```dockerfile
WORKDIR /app
COPY *.csproj ./
RUN dotnet restore
```
Copies only the project file first and restores NuGet packages. This is a deliberate optimization: Docker caches each instruction as a layer. If you only change source code (not the `.csproj`), Docker reuses the cached restore layer and skips re-downloading packages.

```dockerfile
COPY . ./
RUN dotnet publish -c Release -o /out
```
Copies all source files and compiles in Release mode. Output goes to `/out`.

```dockerfile
# ── STAGE 2: Runtime ────────────────────────────────────
FROM mcr.microsoft.com/dotnet/aspnet:10.0
```
Pulls a much **smaller** Microsoft image — only the ASP.NET runtime, no SDK. The final image that runs in production doesn't carry compilers or build tools. This is called a **multi-stage build**, and its main benefit is image size and attack surface.

```dockerfile
WORKDIR /app
COPY --from=build /out .
```
Copies only the compiled output from Stage 1 into the runtime image. Nothing from your source code or the SDK bleeds into the final image.

```dockerfile
EXPOSE 8080
ENTRYPOINT ["dotnet", "vps.dll"]
```
Documents that the container listens on port 8080, and sets the startup command.

---

## The full mental model

```
Your machine                     VPS
─────────────────                ─────────────────────────────────
Source code (.cs, .cshtml)  →   docker build  →  Image (compiled app + runtime)
                                docker run    →  Container (running process, port 8080)
                                               ↑
                                         DNS + SSL sit in front of this
```

When you run `docker run -d -p 8080:8080 --name myapp vps-image`, Docker maps **port 8080 on the VPS** to **port 8080 inside the container**. That's what makes the app reachable from the outside world.
