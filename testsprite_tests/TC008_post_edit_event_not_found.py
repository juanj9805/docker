import requests

def test_post_edit_event_not_found():
    base_url = "http://localhost:5026"
    non_existent_id = 9999
    url = f"{base_url}/Event/Edit/{non_existent_id}"
    payload = {
        "Id": non_existent_id,
        "Title": "NonExistent Event",
        "Img": "https://example.com/image.jpg",
        "Description": "This event does not exist",
        "Location": "Nowhere",
        "Status": "Active"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        assert response.status_code == 404, f"Expected 404 NotFound but got {response.status_code}"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_post_edit_event_not_found()