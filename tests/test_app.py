from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "student@example.edu"

    first_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_participant_can_be_removed_from_activity():
    activity_name = "Chess Club"
    email = "remove-me@example.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{quote(email)}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"].startswith("Removed")

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]
