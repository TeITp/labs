import json
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request


def init_db(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)"
        )


def export_tasks(db_path: Path, export_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT id, title FROM tasks ORDER BY id"
        ).fetchall()
    export_path.write_text(
        json.dumps([{"id": task_id, "title": title} for task_id, title in rows]),
        encoding="utf-8",
    )


def create_app(db_path: Path, export_path: Path) -> Flask:
    init_db(db_path)
    app = Flask(__name__)

    @app.get("/tasks")
    def get_tasks():
        with sqlite3.connect(db_path) as connection:
            rows = connection.execute(
                "SELECT id, title FROM tasks ORDER BY id"
            ).fetchall()
        return jsonify([{"id": task_id, "title": title} for task_id, title in rows])

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True)
        title = data.get("title") if isinstance(data, dict) else None
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Поле title є обов'язковим"}), 400

        title = title.strip()
        with sqlite3.connect(db_path) as connection:
            cursor = connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            task_id = cursor.lastrowid
        export_tasks(db_path, export_path)
        return jsonify({"id": task_id, "title": title}), 201

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        with sqlite3.connect(db_path) as connection:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Завдання не знайдено"}), 404
        export_tasks(db_path, export_path)
        return "", 204

    return app
