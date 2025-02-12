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


def test_task_lifecycle(client) -> None:
    client.delete("/tasks/cleanup")
    score_initial = client.get("/scores/total").get_json()["total_score"]
    task_id = ajouter_tache_recuperer_id(client)
    assert (
        "0 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )
    added_score = client.post(f"/tasks/{task_id}/complete").get_json()['score_added']
    score_after_complete = client.get("/scores/total").get_json()["total_score"]
    assert (
        "1 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )
    assert (
        "0 tâches obsolètes ou complétées supprimées"
        == client.delete("/tasks/cleanup").get_json()["message"]
    )
    score_after_cleanup = client.get("/scores/total").get_json()["total_score"]
    assert score_after_cleanup == score_after_complete
    assert score_after_cleanup == score_initial + added_score


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


def test_completed_task_are_not_active_anymore(client) -> None:
    cleanup_all_active_tasks(client)
    res = client.get("/tasks/active")
    assert res.status_code == 404
    assert res.get_json()["message"] == "Aucune tâche active trouvée."
    id = ajouter_tache_recuperer_id(client)
    res = client.get("/tasks/active")
    first_task = res.get_json()[0]
    assert first_task["id"] == id
    client.post(f"/tasks/{id}/complete")
    assert client.get("/tasks/active").get_json() == {
        'message': 'Aucune tâche active trouvée.',
    }


def cleanup_all_active_tasks(client):
    res = client.get("/tasks/active")
    array = res.get_json()
    for task in array:
        id = task["id"]
        client.post(f"/tasks/{id}/complete")


def test_borrow_book_with_mock(mocker, client) -> None:
    mock_db = mocker.patch("src.tasks.get_existing_or_create_db")
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = {
        "priority": 20,
        "difficulty": 3,
        "completed": 0,
        "due_date": "",
    }

    mock_db.return_value.cursor.return_value = mock_cursor

    response = client.post("/tasks/200000000/complete")
    assert response.status_code == 200
    assert response.get_json()["score_added"] == 600
