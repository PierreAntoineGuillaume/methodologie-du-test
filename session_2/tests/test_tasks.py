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


def ajouter_tache(client):
    return client.post(
        "/tasks",
        json={
            "title": "Preparer le rapport",
            "description": "Finaliser le rapport pour la reunion",
            "due_date": "2050-12-15",
            "priority": 3,
            "difficulty": 2,
        },
    )


def ajouter_tache_recuperer_id(client):
    return ajouter_tache(client).get_json()["id"]


def test_add_task(client) -> None:
    response = ajouter_tache(client)
    assert response.status_code == 201
    keys = response.get_json()
    assert keys["description"] == "Finaliser le rapport pour la reunion"
    assert keys["difficulty"] == 2
    assert keys["due_date"] == "2050-12-15"
    assert keys["priority"] == 3
    assert keys["title"] == "Preparer le rapport"
    assert keys["worth"] == 60


def test_add_without_data(client) -> None:
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_complete_missing_task(client) -> None:
    response = client.post("/tasks/200000000/complete", json={})
    assert response.status_code == 404


def test_complete_already_completed_task(client) -> None:
    id = ajouter_tache_recuperer_id(client)
    assert client.post(f"/tasks/{id}/complete", json={}).status_code == 200
    assert client.post(f"/tasks/{id}/complete", json={}).status_code == 400


def test_complete_task(client) -> None:
    task_id = ajouter_tache_recuperer_id(client)
    score_initial = client.get("/scores/total").get_json()["total_score"]
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Tâche marquée comme terminée",
        "score_added": 60,
    }
    assert client.get("/scores/total").get_json()["total_score"] == score_initial + 60


def test_clean_task(client) -> None:
    client.delete("/tasks/cleanup")
    task_id = ajouter_tache_recuperer_id(client)
    assert (
        "0 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )
    client.post(f"/tasks/{task_id}/complete")
    assert (
        "1 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )
    assert (
        "0 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )


def test_due_date_none(client) -> None:
    res = client.post(
        "/tasks",
        json={
            "title": "Preparer le rapport",
            "description": "Finaliser le rapport pour la reunion",
            "priority": 5,
            "difficulty": 4,
        },
    )

    assert res.get_json()["worth"] == 200


def test_due_date_in_past(client) -> None:
    res = client.post(
        "/tasks",
        json={
            "title": "Preparer le rapport",
            "description": "Finaliser le rapport pour la reunion",
            "due_date": "2000-01-01",
            "priority": 5,
            "difficulty": 4,
        },
    )

    assert res.get_json()["worth"] == 100


def test_due_date_bad_format(client) -> None:
    res = client.post(
        "/tasks",
        json={
            "title": "Preparer le rapport",
            "description": "Finaliser le rapport pour la reunion",
            "due_date": "azeaze",
            "priority": 5,
            "difficulty": 4,
        },
    )

    assert res.get_json()["worth"] == 200


def test_active(client) -> None:
    res = client.get("/tasks/active")
    array = res.get_json()
    for task in array:
        id = task["id"]
        client.post(f"/tasks/{id}/complete")
    res = client.get("/tasks/active")
    assert res.status_code == 404
    assert res.get_json()["message"] == "Aucune tâche active trouvée."
    id = ajouter_tache_recuperer_id(client)
    res = client.get("/tasks/active")
    first_task = res.get_json()[0]
    assert first_task["id"] == id
