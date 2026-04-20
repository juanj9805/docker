# Product Requirements Document — VPS Events App

## 1. Overview

| Field | Value |
|---|---|
| Project Name | `vps` |
| Stack | .NET 10 · ASP.NET Core MVC · EF Core · MySQL (Pomelo) |
| Deployment Target | VPS with Docker, custom domain, SSL |
| Purpose | Learning project: Docker containerization + VPS deployment lifecycle |

---

## 2. Goals

1. Ship a functional CRUD web app for managing events.
2. Containerize the app with Docker and deploy it to a VPS.
3. Apply professional patterns: DTOs, async DB calls, EF Core migrations, conventional commits.
4. Configure a custom domain (dondominio) pointing to the VPS IP with SSL.

**Non-goal:** This is not a production SaaS. Auth, multi-tenancy, and advanced UI are out of scope for this phase.

---

## 3. Domain Model

### `Event`

| Field | Type | Constraints |
|---|---|---|
| `Id` | `int` | PK, auto-increment |
| `Title` | `string` | Required |
| `Img` | `string` | Required — URL or path to image |
| `Description` | `string` | Required |
| `Location` | `string` | Required |
| `Status` | `enum Status` | `Active` / `Inactive` / `Deleted` — default `Active` |
| `CreateAt` | `DateTime` | DB default: `CURRENT_TIMESTAMP` |

### `Status` Enum
```
Active | Inactive | Deleted
```

---

## 4. Functional Requirements

### FR-01 — List Events
- **Route:** `GET /Event/Index`
- Returns all events from the DB (no filtering/pagination yet).
- Renders `Views/Event/Index.cshtml`.

### FR-02 — Create Event
- **Route:** `GET /Event/Create` → render form
- **Route:** `POST /Event/Create` → validate `CreateEventDto`, persist, redirect to Index
- Validates all required fields via `ModelState`.
- On failure: returns the same view with validation errors.

### FR-03 — Edit Event
- **Route:** `GET /Event/Edit/{id}` → load event by ID, map to `EditEventDto`, render form
- **Route:** `POST /Event/Edit/{id}` → validate, update fields, save, redirect to Index
- Returns `404 NotFound` if event does not exist.

### FR-04 — Delete Event
- **Route:** `POST /Event/Delete/{id}`
- Hard-deletes the record from DB.
- Returns `404 NotFound` if event does not exist.
- Redirects to Index on success.

---

## 5. DTOs

| DTO | Used In | Fields |
|---|---|---|
| `CreateEventDto` | POST Create | Title, Img, Description, Location, Status |
| `EditEventDto` | GET/POST Edit | Id, Title, Img, Description, Location, Status |

All fields carry `[Required]` validation attributes.

---

## 6. Architecture

```
Request → Controller → EF Core DbContext → MySQL
              ↓
           Razor View (DTO / Model)
```

- **No service/repository layer** — direct `DbContext` injection into controllers (intentional for this learning phase).
- All DB operations are `async` with `CancellationToken` propagation.
- Connection string assembled from env vars: `DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

---

## 7. Infrastructure Requirements

### Docker
- Two-stage Dockerfile: SDK stage builds/publishes, ASP.NET runtime stage runs.
- App listens on **port 8080** inside the container.
- DB config injected via environment variables at runtime.

### VPS Deployment
1. Build and test locally (`dotnet run`).
2. Push to GitHub.
3. Clone on VPS, build Docker image on the server.
4. Configure DNS (dondominio) → VPS IP.
5. Install SSL certificate (HTTPS).

---

## 8. Current Gaps / Known Missing Requirements

These are gaps relative to a production-grade app. Addressing them is part of the learning roadmap:

| Gap | Priority | Notes |
|---|---|---|
| No authentication/authorization | High | `UseAuthorization()` is registered but no policies exist |
| Hard delete instead of soft delete | Medium | `Status.Deleted` exists but `Delete` action does `Remove()` — inconsistent |
| No service/repository layer | Medium | Business logic lives directly in controllers |
| No pagination or filtering on Index | Low | All events loaded at once |
| `Img` field accepts arbitrary string | Medium | No URL validation or file upload — potential bad data |
| No global error handling for DB failures | High | Only handles `NotFound`; no try/catch for DB exceptions |
| No input sanitization on Description | Medium | XSS risk if rendered as raw HTML |
| View names deviate from ASP.NET convention | Low | `Show`/`Destroy` instead of `Details`/`Delete` |

---

## 9. Out of Scope (v1)

- User authentication and roles
- Event registration / attendees
- Image upload (file storage)
- Pagination, search, or filtering
- Email notifications
- API endpoints (REST/JSON)

---

## 10. Acceptance Criteria

| ID | Criteria |
|---|---|
| AC-01 | App runs locally via `dotnet run` without errors |
| AC-02 | Docker image builds and container starts with correct env vars |
| AC-03 | All four CRUD operations work end-to-end against MySQL |
| AC-04 | EF Core migration `InitialMigration` applies cleanly on a fresh DB |
| AC-05 | App is reachable on VPS via custom domain over HTTPS |
| AC-06 | Invalid form submissions return validation errors without crashing |
