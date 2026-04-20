import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_get_event_index_list():
    url = f"{BASE_URL}/Event/Index"
    headers = {
        "Accept": "text/html"
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "text/html" in content_type, f"Expected 'text/html' in Content-Type but got {content_type}"

    content = response.text
    # Check if the response body contains event list HTML elements at least in some form,
    # since it's rendered in a view. We'll do a simple sanity check for typical event keywords.
    # This is a basic heuristic because we do not have a strict JSON schema for this endpoint.
    assert "event" in content.lower() or "events" in content.lower() or "<div" in content.lower(), "Response body does not contain expected event list view content"

test_get_event_index_list()
