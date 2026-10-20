# Тестирование канбан-доски с Selenium (Python)

[![hexlet-check](https://github.com/kicha3007-boop/python-selenium-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/python-selenium-project-314/actions)

UI-тесты для Task Manager — канбан-доски на react-admin. В приложении есть пользователи,
статусы (колонки доски), метки и задачи; бэкенда нет, данные живут в памяти браузера,
поэтому каждый тест начинает с одного и того же набора записей.

Тесты написаны на pytest и Selenium WebDriver, взаимодействие со страницами вынесено
в Page Object-классы. Каждый тест проверяет результат действия — видимые строки таблицы,
карточки в колонках, значения в формах, — а не только факт клика или перехода.

## Что проверяется

| Файл | Сценарии |
| --- | --- |
| `tests/test_basic.py` | приложение открывается и показывает форму входа (smoke) |
| `tests/test_auth.py` | вход с любыми логином и паролем, выход, закрытые страницы после выхода |
| `tests/test_users.py` | список и поля пользователей, создание, редактирование, проверка формата email, удаление одной, нескольких и всех записей |
| `tests/test_statuses.py` | список статусов, создание, редактирование, удаление, массовое удаление |
| `tests/test_labels.py` | список меток, создание, редактирование, удаление, массовое удаление |
| `tests/test_tasks.py` | колонки и карточки доски, создание задачи в нужной колонке, просмотр, редактирование, смена статуса в форме и перетаскиванием, удаление, фильтры по статусу, исполнителю и метке |

## Структура

```text
conftest.py            # браузер (headless Chrome/Chromium), APP_BASE_URL, скриншот при падении
tests/
  conftest.py          # фикстуры страниц: вход, разделы приложения
  data.py              # исходные данные приложения и учётные данные
  pages/               # Page Object-классы
    base_page.py       # ожидания, ввод, выпадающие списки, выход
    login_page.py
    dashboard_page.py
    resource_page.py   # общий раздел-таблица react-admin
    users_page.py
    statuses_page.py
    labels_page.py
    tasks_page.py      # канбан-доска
  test_*.py
```

## Требования

- Python 3.14 и [uv](https://docs.astral.sh/uv/)
- Docker — чтобы поднять приложение
- Google Chrome или Chromium (драйвер Selenium Manager подберёт сам; в Debian/Ubuntu
  используются пакеты `chromium` и `chromium-driver`)

## Запуск

```bash
make install   # uv sync
make start     # приложение на http://localhost:5173 (docker run hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app)
```

В другом терминале:

```bash
make smoke     # uv run pytest -k smoke
make test      # все тесты
make lint      # ruff
make stop      # остановить контейнер приложения
```

Адрес приложения тесты берут только из переменной окружения `APP_BASE_URL`
(по умолчанию в `Makefile` — `http://localhost:5173`):

```bash
APP_BASE_URL=http://localhost:5174 uv run pytest
```

### Переменные окружения

| Переменная | Обязательна | Назначение |
| --- | --- | --- |
| `APP_BASE_URL` | да | адрес запущенного приложения |
| `HEADLESS` | нет | `false` — показать окно браузера |
| `BROWSER_WINDOW_SIZE` | нет | размер окна, по умолчанию `1440,900` |
| `CHROME_BIN`, `CHROMEDRIVER_BIN` | нет | явные пути к браузеру и драйверу |

Скриншоты упавших тестов сохраняются в `test-results/`.
