from tests.data import STATUSES, TASKS_BY_STATUS, TASKS_OF_JOHN


def test_board_shows_columns_for_statuses(tasks_page):
    assert tasks_page.column_titles() == list(STATUSES)


def test_board_shows_all_tasks(tasks_page):
    all_tasks = [title for titles in TASKS_BY_STATUS.values() for title in titles]

    assert sorted(tasks_page.card_titles()) == sorted(all_tasks)
    for status, titles in TASKS_BY_STATUS.items():
        assert tasks_page.cards_in(status) == titles


def test_task_create_form_opens(tasks_page):
    title, content = tasks_page.open_create_form()

    assert title.get_attribute("value") == ""
    assert content.get_attribute("value") == ""


def test_create_task(tasks_page, unique):
    title = f"Write tests {unique}"

    tasks_page.create(title, "Cover the board", assignee="jane@gmail.com", status="To Review")

    tasks_page.wait_card_in(title, "To Review")
    assert tasks_page.status_of(title) == "To Review"
    assert "Cover the board" in tasks_page.card_text(title)
    assert sorted(tasks_page.cards_in("To Review")) == sorted(
        [*TASKS_BY_STATUS["To Review"], title]
    )


def test_task_details(tasks_page):
    details = tasks_page.open_show("Task 2")

    assert "Task 2" in details
    assert "Description of task 2" in details
    assert "john@google.com" in details


def test_edit_form_is_prefilled(tasks_page):
    values = tasks_page.open_edit("Task 7")

    assert values == {"title": "Task 7", "content": "Description of task 7", "status": "To Review"}


def test_edit_task(tasks_page, unique):
    title = f"Task 7 updated {unique}"

    tasks_page.update("Task 7", title=title, content="New description")

    tasks_page.wait_card_gone("Task 7")
    assert tasks_page.status_of(title) == "To Review"
    assert "New description" in tasks_page.card_text(title)


def test_change_status_in_form(tasks_page):
    tasks_page.update("Task 1", status="Published")

    tasks_page.wait_card_in("Task 1", "Published")
    assert tasks_page.status_of("Task 1") == "Published"
    assert "Task 1" not in tasks_page.cards_in("To Be Fixed")


def test_drag_card_to_next_column(tasks_page):
    tasks_page.move_card_right("Task 5")

    tasks_page.wait_card_in("Task 5", "To Review")
    assert "Task 5" not in tasks_page.cards_in("Draft")
    tasks_page.open_route()
    tasks_page.open()
    assert tasks_page.status_of("Task 5") == "To Review"


def test_delete_task(tasks_page):
    tasks_page.delete("Task 8")

    tasks_page.wait_card_gone("Task 8")
    assert tasks_page.cards_in("To Be Fixed") == ["Task 1", "Task 13"]


def test_filter_by_status(tasks_page):
    tasks_page.filter_by("status_id", "Draft")

    tasks_page.wait_card_gone("Task 1")
    assert sorted(tasks_page.card_titles()) == sorted(TASKS_BY_STATUS["Draft"])


def test_filter_by_assignee(tasks_page):
    tasks_page.filter_by("assignee_id", "john@google.com")

    tasks_page.wait_card_gone("Task 3")
    assert sorted(tasks_page.card_titles()) == sorted(TASKS_OF_JOHN)


def test_filter_by_label(tasks_page):
    tasks_page.filter_by("label_id", "critical")

    tasks_page.wait_card_gone("Task 1")
    assert "Task 15" in tasks_page.card_titles()
