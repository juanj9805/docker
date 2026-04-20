import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_post_delete_event_not_found():
    non_existent_id = 99999999
    url = f"{BASE_URL}/Event/Delete/{non_existent_id}"
    try:
        response = requests.post(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"
    assert response.status_code == 404, f"Expected 404 NotFound, got {response.status_code}"

test_post_delete_event_not_found()