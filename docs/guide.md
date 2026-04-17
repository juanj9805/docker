# Docker Guide — Conceptos fundamentales

## 1. Image vs Container

Una **imagen** es una receta. Un **container** es el plato que cocinaste con esa receta.

| Concepto | Qué es | Analogía |
|---|---|---|
| **Image** | Snapshot congelado y read-only de tu app + runtime + OS libs | Receta de cocina |
| **Container** | Proceso vivo creado a partir de una imagen | El plato cocinado |

Una imagen puede generar múltiples containers simultáneamente. Cada container es independiente.

```
Dockerfile  ──→  docker build  ──→  Image  ──→  docker run  ──→  Container
 (receta)                          (congelado)                    (corriendo)
```

---

## 2. Dockerfile — el two-stage build

Este proyecto usa un build de dos etapas para mantener la imagen final pequeña:

```dockerfile
# Etapa 1: compilar (usa el SDK completo ~700MB)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /app
COPY *.csproj ./
RUN dotnet restore vps.csproj
COPY . ./
RUN dotnet publish vps.csproj -c Release -o /out

# Etapa 2: runtime (solo lo necesario para correr ~200MB)
FROM mcr.microsoft.com/dotnet/aspnet:10.0
WORKDIR /app
COPY --from=build /out .
EXPOSE 8080
ENTRYPOINT ["dotnet", "vps.dll"]
```

**Por qué dos etapas:** el SDK solo se necesita para compilar. La imagen final solo carga el runtime + el output compilado. Resultado: imagen más pequeña y sin código fuente expuesto.

---

## 3. Comandos esenciales

```bash
# Construir una imagen
docker build -t <nombre-imagen> .

# Ver imágenes disponibles
docker images

# Crear y correr un container
docker run -d -p 8080:8080 --name <nombre-container> <nombre-imagen>

# Ver containers corriendo
docker ps

# Detener un container
docker stop <nombre-container>

# Eliminar un container
docker rm <nombre-container>
```

---

## 4. Por qué necesitas stop → rm → run para cada deploy

Los containers son **inmutables** — una vez corriendo, no se actualizan solos.

Cuando cambias el código y haces `docker build`, obtienes una **nueva imagen**. El container viejo sigue corriendo desde la **imagen vieja** y no sabe que existe la nueva.

Por eso el ciclo de deploy es siempre:

```bash
docker build -t vps .        # nueva imagen con el nuevo código
docker stop vps-container    # detener el container viejo
docker rm vps-container      # eliminar el container viejo (liberar el nombre)
docker run -d -p 8080:8080 --name vps-container vps  # container nuevo desde imagen nueva
```

**Beneficios de la inmutabilidad:**
- Lo que corres en el VPS es idéntico a lo que probaste local
- Puedes hacer rollback corriendo la imagen anterior
- No hay servidores con cambios acumulados que nadie recuerda haber hecho

---

## 5. Workflow de deploy completo

```
Local machine                          VPS
─────────────                         ──────────────────────────
1. Editar código
2. git add + commit + push  ───────→  3. git pull
                                      4. docker build -t vps .
                                      5. docker stop vps-container
                                      6. docker rm vps-container
                                      7. docker run -d -p 8080:8080 \
                                           --name vps-container vps
                                      ✓ cambios en producción
```

**Regla importante:** nunca edites archivos directamente en el VPS. Todo cambio entra por git. El VPS solo hace `git pull` + rebuild.

---

## 6. Errores comunes

### "more than one project or solution file"
```
MSBUILD : error MSB1011: Specify which project or solution file to use
```
**Causa:** el VPS tiene tanto `vps.csproj` como `docker.sln` y dotnet no sabe cuál usar.  
**Fix:** especificar el archivo explícitamente:
```dockerfile
RUN dotnet restore vps.csproj
RUN dotnet publish vps.csproj -c Release -o /out
```

---

## 7. El siguiente nivel — CI/CD

Una vez que el deploy manual se vuelve repetitivo, se automatiza con GitHub Actions. El pipeline hace exactamente los mismos pasos, pero se dispara solo con cada `git push`:

```
git push → GitHub Actions → SSH al VPS → git pull → docker build → swap container
```

Primero domina el flujo manual. El CI/CD es solo scripting de lo que ya haces a mano.
