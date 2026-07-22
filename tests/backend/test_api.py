from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"]


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@example.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
