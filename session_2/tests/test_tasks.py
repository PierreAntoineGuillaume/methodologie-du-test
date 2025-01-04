import pytest
from src.tasks import app


@pytest.fixture
def test_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_url(client):
    response = client.post("/URL", json={"key": "payload"})
    assert response.status_code == 404


def test_add_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Preparer le rapport",
            "description": "Finaliser le rapport pour la reunion",
            "due_date": "2050-12-15",
            "priority": 3,
            "difficulty": 2,
        },
    )
    assert response.status_code == 201
    keys = response.get_json()
    assert keys["description"] == "Finaliser le rapport pour la reunion"
    assert keys["difficulty"] == 2
    assert keys["due_date"] == "2050-12-15"
    assert keys["priority"] == 3
    assert keys["title"] == "Preparer le rapport"
    assert keys["worth"] == 60
