import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_post_edit_event_success():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Step 1: Create a new event to edit
    create_data = {
        "Title": "Original Event",
        "Img": "https://example.com/original.jpg",
        "Description": "Original Description",
        "Location": "Original Location",
        "Status": "Active"
    }

    new_event_id = None
    try:
        create_resp = requests.post(
            f"{BASE_URL}/Event/Create",
            data=create_data,
            headers=headers,
            allow_redirects=False,
            timeout=TIMEOUT
        )
        assert create_resp.status_code == 302, f"Expected 302 redirect on create, got {create_resp.status_code}"
        location_header = create_resp.headers.get("Location", "")
        assert location_header.endswith("/Event/Index"), f"Expected redirect location /Event/Index, got {location_header}"

        # Step 2: Retrieve the list of events to find the new event's ID
        index_resp = requests.get(f"{BASE_URL}/Event/Index", timeout=TIMEOUT)
        assert index_resp.status_code == 200, f"Expected 200 on Event/Index get, got {index_resp.status_code}"
        # Since response is rendered HTML, we try to find the event by title
        # This is a heuristic since no API returns JSON; we parse HTML text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(index_resp.text, "html.parser")
        event_link = None
        # Look for link or element that leads to edit page and contains the event title
        for a in soup.find_all("a", href=True):
            if "/Event/Edit/" in a['href'] and create_data["Title"] in a.text:
                event_link = a['href']
                break
        assert event_link is not None, "Created event link not found in Event/Index page"
        try:
            new_event_id = int(event_link.rstrip("/").split("/")[-1])
        except Exception:
            raise AssertionError("Failed to parse new event ID from Event/Index page")

        # Step 3: Prepare updated data for edit post
        edit_data = {
            "Id": str(new_event_id),
            "Title": "Updated Event",
            "Img": "https://example.com/updated.jpg",
            "Description": "Updated Description",
            "Location": "Updated Location",
            "Status": "Active"
        }

        # Step 4: POST edited event
        edit_resp = requests.post(
            f"{BASE_URL}/Event/Edit/{new_event_id}",
            data=edit_data,
            headers=headers,
            allow_redirects=False,
            timeout=TIMEOUT
        )
        assert edit_resp.status_code == 302, f"Expected 302 redirect on edit, got {edit_resp.status_code}"
        edit_location = edit_resp.headers.get("Location", "")
        assert edit_location.endswith("/Event/Index"), f"Expected redirect to /Event/Index, got {edit_location}"

        # Step 5: Verify the event on index page includes updated information
        index_resp_after_edit = requests.get(f"{BASE_URL}/Event/Index", timeout=TIMEOUT)
        assert index_resp_after_edit.status_code == 200, f"Expected 200 on Event/Index after edit, got {index_resp_after_edit.status_code}"
        soup_after_edit = BeautifulSoup(index_resp_after_edit.text, "html.parser")
        assert "Updated Event" in soup_after_edit.text, "Updated event title not found in index page after edit"
        assert "Updated Description" in soup_after_edit.text, "Updated event description not found in index page after edit"
        assert "Updated Location" in soup_after_edit.text, "Updated event location not found in index page after edit"

    finally:
        # Cleanup: Delete the created event if it was created
        if new_event_id is not None:
            requests.post(
                f"{BASE_URL}/Event/Delete/{new_event_id}",
                timeout=TIMEOUT
            )

test_post_edit_event_success()
