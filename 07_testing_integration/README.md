# Звіт до роботи 07.4

**Виконав:** Кушнір Андрій, КН-41

## Тема

Інтеграційне тестування Flask, SQLite та JSON.

## Мета роботи

Перевірити взаємодію HTTP-маршрутів Flask, бази SQLite та файлового експорту на тимчасових ресурсах.

## Виконання роботи

За основу взято [приклад викладача](https://github.com/BobasB/it_college/tree/main/example/testing/04_integration_testing). Фікстура `resources` отримує `tmp_path` і створює для кожного тесту власні шляхи до бази та експорту. HTTP-запити виконує тестовий клієнт Flask. [Маршрути й експорт](app.py) · [Тести](test_app.py)

Команди з кореня репозиторію:

```bash
python -m pip install -r 07_testing_integration/requirements.txt
python -m pytest -v 07_testing_integration
python -m pytest -v 07_testing_integration/test_app.py::test_create_task
```

| Тест | Що перевірено |
| --- | --- |
| `test_create_task` | POST повертає 201 і назву завдання. Назва зберігається в SQLite та JSON. |
| `test_get_tasks` | GET повертає 200 і список двох створених завдань у порядку додавання. |
| `test_create_task_requires_title` | POST без `title` повертає 400 і повідомлення про помилку. Файл не створюється. |
| `test_export_empty_tasks` | Порожня таблиця дає JSON-файл із `[]`, GET повертає 200 і `[]`. |
| `test_export_replaces_corrupted_json` | Початковий JSON не читається. Після POST файл містить коректний запис, такий самий, як у відповіді 201. |
| `test_tasks_are_stored_in_creation_order` | SQLite та JSON містять обидва записи в порядку зростання ідентифікаторів. |
| `test_delete_task` | DELETE повертає 204. GET, SQLite та JSON містять лише другий запис. |
| `test_delete_missing_task` | DELETE невідомого ідентифікатора повертає 404. Наявне завдання залишається у відповіді GET та експорті. |

```text
8 passed
```

[Повний результат локального pytest](pytest-result.txt)

## Висновок

Мету досягнуто. Вісім тестів пройшли. Перевірено створення, читання й видалення завдань та перезапис пошкодженого експорту. Тимчасова SQLite та реальний файл дозволили звірити HTTP-відповіді зі збереженими даними.
