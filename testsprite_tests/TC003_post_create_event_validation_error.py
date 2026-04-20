import requests

BASE_URL = "http://localhost:5026"

def test_post_create_event_validation_error():
    url = f"{BASE_URL}/Event/Create"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # Missing required field "Title"
    payload = {
        "Img": "https://example.com/img.jpg",
        "Description": "Missing title",
        "Location": "Hall",
        "Status": "Active"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200
    # Validation errors should be shown in the returned HTML view.
    content = response.text
    assert "validation" in content.lower() or "error" in content.lower() or "<span" in content.lower(), "Expected validation error indicators in response content"

test_post_create_event_validation_error()