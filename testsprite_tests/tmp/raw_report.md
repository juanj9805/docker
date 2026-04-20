
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** docker
- **Date:** 2026-04-19
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 get event index list
- **Test Code:** [TC001_get_event_index_list.py](./TC001_get_event_index_list.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 27, in <module>
  File "<string>", line 16, in test_get_event_index_list
AssertionError: Expected status code 200 but got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/4d67b9fc-19b2-4b21-a19c-98993421a8ec
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 post create event success
- **Test Code:** [TC002_post_create_event_success.py](./TC002_post_create_event_success.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 58, in <module>
  File "<string>", line 22, in test_post_create_event_success
AssertionError: Expected 302 Redirect, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/ac05e884-3ee8-49a2-b33b-ab5c061ddfc0
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 post create event validation error
- **Test Code:** [TC003_post_create_event_validation_error.py](./TC003_post_create_event_validation_error.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/c08568b7-a698-40a6-9da0-c347a05b67c3
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 get edit event form success
- **Test Code:** [TC004_get_edit_event_form_success.py](./TC004_get_edit_event_form_success.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 68, in <module>
  File "<string>", line 23, in test_get_edit_event_form_success
AssertionError: Expected 302 redirect on create, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/581b0209-325d-4044-bb20-5956b23b78cf
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 get edit event form not found
- **Test Code:** [TC005_get_edit_event_form_not_found.py](./TC005_get_edit_event_form_not_found.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 15, in <module>
  File "<string>", line 13, in test_get_edit_event_form_not_found
AssertionError: Expected 404 NotFound, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/1c9969ee-889c-4750-b761-24e6ef8cd9d2
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 post edit event success
- **Test Code:** [TC006_post_edit_event_success.py](./TC006_post_edit_event_success.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 90, in <module>
  File "<string>", line 29, in test_post_edit_event_success
AssertionError: Expected 302 redirect on create, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/b6c7d05c-d538-487f-ba28-6edd61be3559
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 post edit event validation error
- **Test Code:** [TC007_post_edit_event_validation_error.py](./TC007_post_edit_event_validation_error.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 103, in <module>
  File "<string>", line 21, in test_post_edit_event_validation_error
AssertionError: Expected 302 redirect on create success, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/cc156f2d-9570-4547-bc35-3ea2b983e539
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 post edit event not found
- **Test Code:** [TC008_post_edit_event_not_found.py](./TC008_post_edit_event_not_found.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 24, in <module>
  File "<string>", line 20, in test_post_edit_event_not_found
AssertionError: Expected 404 NotFound but got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/2e5e7fdc-963e-4c2c-bc86-17ff1f78b986
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 post delete event success
- **Test Code:** [TC009_post_delete_event_success.py](./TC009_post_delete_event_success.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 65, in <module>
  File "<string>", line 25, in test_post_delete_event_success
AssertionError: Expected 302 on create, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/476eb67a-e712-4092-b01f-41527b3103a2
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 post delete event not found
- **Test Code:** [TC010_post_delete_event_not_found.py](./TC010_post_delete_event_not_found.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 15, in <module>
  File "<string>", line 13, in test_post_delete_event_not_found
AssertionError: Expected 404 NotFound, got 500

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/1e862ab3-e401-498f-82be-035df9bef597/b9c492d9-3746-4af7-9898-620eeba19870
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **10.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---