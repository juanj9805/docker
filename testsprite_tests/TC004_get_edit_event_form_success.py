import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_get_edit_event_form_success():
    # First create an event to get a valid existing event id
    create_url = f"{BASE_URL}/Event/Create"
    create_payload = {
        "Title": "Test Event for Edit Form",
        "Img": "https://example.com/test_img.jpg",
        "Description": "Description of test event",
        "Location": "Test Location",
        "Status": "Active"
    }
    # Use form data as MVC expects form encoded data for POST
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        # Create event (POST /Event/Create)
        create_response = requests.post(create_url, data=create_payload, headers=headers, timeout=TIMEOUT, allow_redirects=False)
        assert create_response.status_code == 302, f"Expected 302 redirect on create, got {create_response.status_code}"
        # Extract event id from redirect location or by listing events
        # The app redirects to /Event/Index, so we need to get the event list to find the new event id

        # Get list of events to find the new event id
        index_url = f"{BASE_URL}/Event/Index"
        index_response = requests.get(index_url, timeout=TIMEOUT)
        assert index_response.status_code == 200, f"Expected 200 on index, got {index_response.status_code}"
        content = index_response.text

        # Look for the created event title in the HTML to find event id (assumes the id is somewhere visible in the content)
        # Simple approach: find event id with the title
        # Since no API returns JSON, parse from html the edit link: /Event/Edit/{id}
        import re
        pattern = re.compile(r"/Event/Edit/(\d+).*?>\s*Test Event for Edit Form\s*<", re.I)
        match = pattern.search(content)
        if match:
            event_id = int(match.group(1))
        else:
            # If not found by title match, fallback: try to find any edit link and pick one (best effort)
            fallback_pattern = re.compile(r"/Event/Edit/(\d+)", re.I)
            fallback_match = fallback_pattern.search(content)
            assert fallback_match, "Could not find any event id in event index view."
            event_id = int(fallback_match.group(1))

        # Now perform GET /Event/Edit/{id}
        edit_url = f"{BASE_URL}/Event/Edit/{event_id}"
        edit_response = requests.get(edit_url, timeout=TIMEOUT)
        assert edit_response.status_code == 200, f"Expected 200 on edit GET, got {edit_response.status_code}"
        edit_content = edit_response.text

        # Validate that the edit form contains the event data we created
        assert "Test Event for Edit Form" in edit_content
        assert "https://example.com/test_img.jpg" in edit_content
        assert "Description of test event" in edit_content
        assert "Test Location" in edit_content
        assert "Active" in edit_content

    finally:
        # Cleanup: delete the created event if event_id is set
        if 'event_id' in locals():
            delete_url = f"{BASE_URL}/Event/Delete/{event_id}"
            delete_response = requests.post(delete_url, timeout=TIMEOUT, allow_redirects=False)
            assert delete_response.status_code == 302, f"Expected 302 redirect on delete, got {delete_response.status_code}"

test_get_edit_event_form_success()