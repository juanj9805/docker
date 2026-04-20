import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_get_edit_event_form_not_found():
    non_existent_id = 9999
    url = f"{BASE_URL}/Event/Edit/{non_existent_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"
    assert response.status_code == 404, f"Expected 404 NotFound, got {response.status_code}"

test_get_edit_event_form_not_found()