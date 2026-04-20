import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_post_edit_event_validation_error():
    # First, create a valid event to edit
    create_url = f"{BASE_URL}/Event/Create"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    valid_event_data = {
        "Title": "Test Event",
        "Img": "https://example.com/img.jpg",
        "Description": "Valid description",
        "Location": "Test Location",
        "Status": "Active"
    }

    # Create new event to get valid event Id
    try:
        create_response = requests.post(create_url, data=valid_event_data, headers=headers, timeout=TIMEOUT)
        assert create_response.status_code == 302, f"Expected 302 redirect on create success, got {create_response.status_code}"

        # After successful creation, events are redirected to /Event/Index
        # We need to find the ID of the newly created event for editing.
        # Since no API returns the created ID, we get the event list and parse it.

        index_url = f"{BASE_URL}/Event/Index"
        index_response = requests.get(index_url, timeout=TIMEOUT)
        assert index_response.status_code == 200, f"Expected 200 from index, got {index_response.status_code}"

        # Parse the id from the HTML response - assume the event is listed and includes the ID in a predictable pattern
        # Since we have no API to get IDs, try to locate the event by its Title
        import re
        # Find all event edit links with /Event/Edit/{id}
        edit_links = re.findall(r'/Event/Edit/(\d+)', index_response.text)
        assert edit_links, "No event edit links found in index page"

        # To find the right event, search for event title near the edit link in the HTML, assume title is in text near the link
        # Simple approach: find first edit link with the title string nearby
        # This is fragile but no better option with the given info.

        # Find index of event title in the HTML to locate nearby ID
        event_id = None
        titles_indexes = [m.start() for m in re.finditer(re.escape(valid_event_data["Title"]), index_response.text)]
        for ti in titles_indexes:
            # find the closest edit link id before or after title
            # get position of all edit links in html
            positions = [(m.start(), m.group(1)) for m in re.finditer(r'(/Event/Edit/(\d+))', index_response.text)]
            # find edit link closest to title index
            closest = None
            closest_dist = None
            for pos, eid in positions:
                dist = abs(pos - ti)
                if closest_dist is None or dist < closest_dist:
                    closest_dist = dist
                    closest = eid
            if closest:
                event_id = closest
                break

        assert event_id is not None, "Could not find event ID for the created event"

        # Now test editing the event with missing required fields, expect validation errors with 200 status
        edit_url = f"{BASE_URL}/Event/Edit/{event_id}"

        # According to PRD, required fields: Title, Img, Description, Location, Status
        # Provide incomplete data missing Title, Description, Location, Status
        incomplete_edit_data = {
            "Id": int(event_id),
            "Img": "https://example.com/updated_img.jpg"
            # Missing Title, Description, Location, Status
        }

        post_edit_response = requests.post(edit_url, data=incomplete_edit_data, headers=headers, timeout=TIMEOUT)
        assert post_edit_response.status_code == 200, f"Expected 200 status for validation error, got {post_edit_response.status_code}"

        # Validate that the response contains validation error indications
        # For example, check the content includes "The Title field is required" or a form error marker
        content_lower = post_edit_response.text.lower()
        required_field_errors = [
            "title", "description", "location", "status"
        ]
        # Check that any of these required field names appear with error keywords like "required" or "field is required"
        validation_found = False
        for field in required_field_errors:
            if field in content_lower and ("required" in content_lower or "field is required" in content_lower):
                validation_found = True
                break
        assert validation_found, "Validation errors for missing required fields not found in response content"

    finally:
        # Cleanup: delete the created event if possible
        if 'event_id' in locals() and event_id is not None:
            delete_url = f"{BASE_URL}/Event/Delete/{event_id}"
            try:
                delete_response = requests.post(delete_url, timeout=TIMEOUT)
                # Accept either 302 redirect or 404 in case already deleted
                assert delete_response.status_code in (302, 404), f"Unexpected status code on delete cleanup: {delete_response.status_code}"
            except Exception:
                pass


test_post_edit_event_validation_error()