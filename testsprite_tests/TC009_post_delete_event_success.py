import requests
from urllib.parse import urljoin

BASE_URL = "http://localhost:5026"
TIMEOUT = 30

def test_post_delete_event_success():
    # Data to create a new event
    create_payload = {
        "Title": "Test Event for Delete",
        "Img": "https://example.com/image.jpg",
        "Description": "Event created for testing delete functionality.",
        "Location": "Test Location",
        "Status": "Active"
    }

    # Create event to get a valid ID for deletion
    create_url = urljoin(BASE_URL, "/Event/Create")
    session = requests.Session()

    event_id = None
    try:
        # POST to create event
        create_response = session.post(create_url, data=create_payload, timeout=TIMEOUT, allow_redirects=False)
        assert create_response.status_code == 302, f"Expected 302 on create, got {create_response.status_code}"
        location = create_response.headers.get("Location", "")
        assert location.endswith("/Event/Index"), f"Expected redirect to /Event/Index, got {location}"

        # GET /Event/Index to retrieve the event list page content
        index_url = urljoin(BASE_URL, "/Event/Index")
        index_response = session.get(index_url, timeout=TIMEOUT)
        assert index_response.status_code == 200, f"Expected 200 on index after create, got {index_response.status_code}"
        assert create_payload["Title"] in index_response.text, "Created event title not found in Event Index page"

        # Extract event ID for delete
        # Since API does not provide JSON or API-based ID retrieval, 
        # we must parse the ID from the index page HTML.
        # Assuming event IDs are present in HTML as /Event/Delete/{id} or /Event/Edit/{id} links
        import re
        matches = re.findall(r'/Event/Delete/(\d+)', index_response.text)
        assert matches, "No Delete links found on Event Index page to extract event ID"
        # Choose the newest event by finding the max ID in the matches
        event_id = max(int(id_) for id_ in matches)

        # POST to delete the event
        delete_url = urljoin(BASE_URL, f"/Event/Delete/{event_id}")
        delete_response = session.post(delete_url, timeout=TIMEOUT, allow_redirects=False)
        assert delete_response.status_code == 302, f"Expected 302 on delete, got {delete_response.status_code}"
        delete_location = delete_response.headers.get("Location", "")
        assert delete_location.endswith("/Event/Index"), f"Expected redirect to /Event/Index after delete, got {delete_location}"

        # GET /Event/Index to verify the event no longer appears
        post_delete_index_response = session.get(index_url, timeout=TIMEOUT)
        assert post_delete_index_response.status_code == 200, f"Expected 200 on index after delete, got {post_delete_index_response.status_code}"
        assert create_payload["Title"] not in post_delete_index_response.text, "Deleted event title still found in Event Index page"

    finally:
        # Cleanup: If for some reason delete didn't succeed in the test, attempt delete to keep clean
        if event_id is not None:
            try:
                session.post(urljoin(BASE_URL, f"/Event/Delete/{event_id}"), timeout=TIMEOUT, allow_redirects=False)
            except Exception:
                pass

test_post_delete_event_success()