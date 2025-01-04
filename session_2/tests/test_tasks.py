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
    # assert response.status_code == 404
    # assert response.get_json() == {"message": "Tout fonctionne"}
