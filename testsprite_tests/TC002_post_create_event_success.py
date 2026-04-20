import requests

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_post_create_event_success():
    create_url = f"{BASE_URL}/Event/Create"
    index_url = f"{BASE_URL}/Event/Index"

    event_data = {
        "Title": "Summer Gala",
        "Img": "https://example.com/img.jpg",
        "Description": "Annual event",
        "Location": "Town Hall",
        "Status": "Active"
    }

    session = requests.Session()
    try:
        # Step 1: POST to create event
        response = session.post(create_url, data=event_data, allow_redirects=False, timeout=TIMEOUT)
        assert response.status_code == 302, f"Expected 302 Redirect, got {response.status_code}"
        assert "/Event/Index" in response.headers.get("Location", ""), "Redirect Location header does not contain /Event/Index"

        # Step 2: Follow redirect to Event/Index
        response_index = session.get(index_url, timeout=TIMEOUT)
        assert response_index.status_code == 200, f"Expected 200 on /Event/Index, got {response_index.status_code}"
        content = response_index.text
        # Check that the event title appears on the page (simple string check)
        assert event_data["Title"] in content, f"Event title '{event_data['Title']}' not found in Event/Index page content"
    finally:
        # Cleanup: Find the event by title and delete it to avoid test pollution

        import re

        try:
            response_index = session.get(index_url, timeout=TIMEOUT)
            if response_index.status_code == 200:
                # Look for event ID in edit/delete link near the title text
                pattern = rf'<a[^>]*href="/Event/Edit/(\d+)"[^>]*>[^<]*{re.escape(event_data["Title"])}[^<]*</a>'
                match = re.search(pattern, response_index.text)
                if not match:
                    # Try searching delete link with id if edit link not found
                    pattern_delete = rf'<a[^>]*href="/Event/Delete/(\d+)"[^>]*>[^<]*</a>.*{re.escape(event_data["Title"])}'
                    match = re.search(pattern_delete, response_index.text)

                if match:
                    event_id = match.group(1)
                    delete_url = f"{BASE_URL}/Event/Delete/{event_id}"
                    # Perform POST to delete
                    del_response = session.post(delete_url, allow_redirects=False, timeout=TIMEOUT)
                    # Accept 302 redirect or 404 if event missing already
                    assert del_response.status_code in (302, 404)
        except Exception:
            # Suppress cleanup failure exceptions
            pass

test_post_create_event_success()
