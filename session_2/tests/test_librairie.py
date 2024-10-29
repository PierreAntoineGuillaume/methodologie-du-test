import pytest
from src.librairie import app, jsonify, get_existing_or_create_db


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

def test_bad_url(client):
    response = client.get('/unknown-url')
    assert response.status_code == 404
    assert response.get_json() is None
