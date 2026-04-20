
# TestSprite AI Testing Report (MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** docker (vps — ASP.NET Core MVC)
- **Date:** 2026-04-19
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

### Requirement: Event Listing
- **Description:** GET /Event/Index returns the full list of events from the database.

#### Test TC001 — Get Event Index List
- **Test Code:** [TC001_get_event_index_list.py](./TC001_get_event_index_list.py)
- **Test Error:** `AssertionError: Expected status code 200 but got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/4d67b9fc-19b2-4b21-a19c-98993421a8ec
- **Status:** ❌ Failed
- **Severity:** HIGH
- **Analysis / Findings:** The controller calls `_context.Events.ToListAsync()` which requires a live MySQL connection. The app is running without DB environment variables (`DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`), causing EF Core to throw an exception that surfaces as HTTP 500. Root cause: missing database at test runtime, not a code bug.

---

### Requirement: Event Creation
- **Description:** POST /Event/Create persists a new event. ModelState validation rejects incomplete submissions.

#### Test TC002 — POST Create Event (Success Path)
- **Test Code:** [TC002_post_create_event_success.py](./TC002_post_create_event_success.py)
- **Test Error:** `AssertionError: Expected 302 Redirect, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/ac05e884-3ee8-49a2-b33b-ab5c061ddfc0
- **Status:** ❌ Failed
- **Severity:** HIGH
- **Analysis / Findings:** DB connection failure before `_context.AddAsync()` is reached. Same root cause as TC001.

#### Test TC003 — POST Create Event (Validation Error)
- **Test Code:** [TC003_post_create_event_validation_error.py](./TC003_post_create_event_validation_error.py)
- **Test Error:** None
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/c08568b7-a698-40a6-9da0-c347a05b67c3
- **Status:** ✅ Passed
- **Severity:** LOW
- **Analysis / Findings:** ModelState validation fires before any DB call. `[Required]` annotations on `CreateEventDto` correctly reject empty submissions and return 200 with validation errors. This path does not require a database connection.

---

### Requirement: Event Editing
- **Description:** GET /Event/Edit/{id} renders the edit form; POST /Event/Edit/{id} saves changes. Both return 404 for non-existent IDs.

#### Test TC004 — GET Edit Event Form (Success)
- **Test Code:** [TC004_get_edit_event_form_success.py](./TC004_get_edit_event_form_success.py)
- **Test Error:** `AssertionError: Expected 302 redirect on create, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/581b0209-325d-4044-bb20-5956b23b78cf
- **Status:** ❌ Failed
- **Severity:** HIGH
- **Analysis / Findings:** Setup step (creating an event via POST) fails with 500 due to missing DB. Test cannot proceed to the GET Edit form.

#### Test TC005 — GET Edit Event Form (Not Found)
- **Test Code:** [TC005_get_edit_event_form_not_found.py](./TC005_get_edit_event_form_not_found.py)
- **Test Error:** `AssertionError: Expected 404 NotFound, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/1c9969ee-889c-4750-b761-24e6ef8cd9d2
- **Status:** ❌ Failed
- **Severity:** MEDIUM
- **Analysis / Findings:** `FirstOrDefaultAsync` cannot execute without a DB connection, throwing 500 before the `if (found == null) return NotFound()` guard is reached. The code logic is correct but untestable without a running database.

#### Test TC006 — POST Edit Event (Success)
- **Test Code:** [TC006_post_edit_event_success.py](./TC006_post_edit_event_success.py)
- **Test Error:** `AssertionError: Expected 302 redirect on create, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/b6c7d05c-d538-487f-ba28-6edd61be3559
- **Status:** ❌ Failed
- **Severity:** HIGH
- **Analysis / Findings:** Same DB root cause. Test setup (create) fails before edit can be attempted.

#### Test TC007 — POST Edit Event (Validation Error)
- **Test Code:** [TC007_post_edit_event_validation_error.py](./TC007_post_edit_event_validation_error.py)
- **Test Error:** `AssertionError: Expected 302 redirect on create success, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/cc156f2d-9570-4547-bc35-3ea2b983e539
- **Status:** ❌ Failed
- **Severity:** MEDIUM
- **Analysis / Findings:** Setup step fails. Note: unlike TC003, the Edit POST action calls `FirstOrDefaultAsync` even when ModelState is invalid — because validation is checked after the DB lookup. This is a minor code smell; the `if (!ModelState.IsValid)` guard should come before the DB query.

#### Test TC008 — POST Edit Event (Not Found)
- **Test Code:** [TC008_post_edit_event_not_found.py](./TC008_post_edit_event_not_found.py)
- **Test Error:** `AssertionError: Expected 404 NotFound but got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/2e5e7fdc-963e-4c2c-bc86-17ff1f78b986
- **Status:** ❌ Failed
- **Severity:** MEDIUM
- **Analysis / Findings:** Same root cause as TC005. DB unavailable → 500 before NotFound guard fires.

---

### Requirement: Event Deletion
- **Description:** POST /Event/Delete/{id} removes the event and redirects. Returns 404 for non-existent IDs.

#### Test TC009 — POST Delete Event (Success)
- **Test Code:** [TC009_post_delete_event_success.py](./TC009_post_delete_event_success.py)
- **Test Error:** `AssertionError: Expected 302 on create, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/476eb67a-e712-4092-b01f-41527b3103a2
- **Status:** ❌ Failed
- **Severity:** HIGH
- **Analysis / Findings:** Setup step (create) blocked by DB unavailability.

#### Test TC010 — POST Delete Event (Not Found)
- **Test Code:** [TC010_post_delete_event_not_found.py](./TC010_post_delete_event_not_found.py)
- **Test Error:** `AssertionError: Expected 404 NotFound, got 500`
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/b9c492d9-3746-4af7-9898-620eeba19870
- **Status:** ❌ Failed
- **Severity:** MEDIUM
- **Analysis / Findings:** Same root cause as TC005 and TC008.

---

## 3️⃣ Coverage & Matching Metrics

- **1 of 10 tests passed (10%)**

| Requirement      | Total Tests | ✅ Passed | ❌ Failed |
|------------------|-------------|-----------|----------|
| Event Listing    | 1           | 0         | 1        |
| Event Creation   | 2           | 1         | 1        |
| Event Editing    | 4           | 0         | 4        |
| Event Deletion   | 2           | 0         | 2        |
| **Total**        | **10**      | **1**     | **9**    |

---

## 4️⃣ Key Gaps / Risks

> **10% of tests passed.** The single failure mode responsible for 9/10 failures is a missing database connection at test runtime — not application logic bugs.

**Root Cause — No DB at Test Runtime**
The app reads MySQL credentials exclusively from environment variables (`DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). When run with bare `dotnet run` without those vars set, EF Core cannot connect and every DB-touching endpoint returns HTTP 500. To rerun tests successfully, start the app with valid env vars pointing to a running MySQL instance.

**Code-Level Risk — Edit action order of operations (TC007)**
In `EventController.Edit (POST)`, the `ModelState.IsValid` guard fires *after* `FirstOrDefaultAsync`. This means a bad request still causes a DB round-trip. Low severity but a clean practice violation.

**Structural Gaps (not tested, not covered)**
- No authentication/authorization on any endpoint — any request can mutate data.
- `DELETE` is implemented as a hard delete; the `Deleted` status enum value is never used.
- No pagination on `Index`; full table scan on every request.
- No `[ValidateAntiForgeryToken]` on any POST endpoint — CSRF vulnerability.
