import json
import sqlite3

import pytest

from app import create_app, export_tasks


@pytest.fixture
def resources(tmp_path):
    db_path = tmp_path / "tasks.db"
    export_path = tmp_path / "tasks.json"
    app = create_app(db_path, export_path)
    return app.test_client(), db_path, export_path


def test_create_task(resources):
    client, db_path, export_path = resources

    response = client.post("/tasks", json={"title": "Вивчити pytest"})

    assert response.status_code == 201
    assert response.get_json()["title"] == "Вивчити pytest"
    with sqlite3.connect(db_path) as connection:
        row = connection.execute("SELECT title FROM tasks").fetchone()
    assert row == ("Вивчити pytest",)
    assert json.loads(export_path.read_text(encoding="utf-8"))[0]["title"] == "Вивчити pytest"


def test_get_tasks(resources):
    client, _, _ = resources
    client.post("/tasks", json={"title": "Перше завдання"})
    client.post("/tasks", json={"title": "Друге завдання"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["title"] for task in response.get_json()] == [
        "Перше завдання",
        "Друге завдання",
    ]


def test_create_task_requires_title(resources):
    client, _, export_path = resources

    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Поле title є обов'язковим"}
    assert not export_path.exists()


def test_export_empty_tasks(resources):
    client, db_path, export_path = resources

    export_tasks(db_path, export_path)

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []
    assert json.loads(export_path.read_text(encoding="utf-8")) == []


def test_export_replaces_corrupted_json(resources):
    client, _, export_path = resources
    export_path.write_text("{broken", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        json.loads(export_path.read_text(encoding="utf-8"))

    response = client.post("/tasks", json={"title": "Відновити експорт"})

    assert response.status_code == 201
    assert json.loads(export_path.read_text(encoding="utf-8")) == [response.get_json()]


def test_tasks_are_stored_in_creation_order(resources):
    client, db_path, export_path = resources
    first = client.post("/tasks", json={"title": "Яблуко"})
    second = client.post("/tasks", json={"title": "Абрикос"})

    assert first.status_code == second.status_code == 201
    expected = [first.get_json(), second.get_json()]
    assert expected[0]["id"] < expected[1]["id"]
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    assert rows == [(task["id"], task["title"]) for task in expected]
    assert json.loads(export_path.read_text(encoding="utf-8")) == expected


def test_delete_task(resources):
    client, db_path, export_path = resources
    first = client.post("/tasks", json={"title": "Видалити"}).get_json()
    second = client.post("/tasks", json={"title": "Залишити"}).get_json()

    response = client.delete(f"/tasks/{first['id']}")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/tasks").get_json() == [second]
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT id, title FROM tasks").fetchall()
    assert rows == [(second["id"], second["title"])]
    assert json.loads(export_path.read_text(encoding="utf-8")) == [second]


def test_delete_missing_task(resources):
    client, _, export_path = resources
    task = client.post("/tasks", json={"title": "Зберегти"}).get_json()

    response = client.delete(f"/tasks/{task['id'] + 1}")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Завдання не знайдено"}
    assert client.get("/tasks").get_json() == [task]
    assert json.loads(export_path.read_text(encoding="utf-8")) == [task]
