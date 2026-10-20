from tests.data import STATUSES


def test_statuses_list_shows_all_statuses(statuses_page):
    assert len(statuses_page.rows()) == len(STATUSES)
    assert statuses_page.column("name") == list(STATUSES)
    assert statuses_page.column("slug") == list(STATUSES.values())


def test_status_create_form_opens(statuses_page):
    fields = statuses_page.open_create_form()

    assert [field.get_attribute("name") for field in fields] == ["name", "slug"]
    assert all(field.is_enabled() for field in fields)


def test_create_status(statuses_page, unique):
    name = f"In Progress {unique}"

    statuses_page.create({"name": name, "slug": f"in_progress_{unique}"})
    statuses_page.open()

    assert statuses_page.has_row(name)
    assert f"in_progress_{unique}" in statuses_page.column("slug")
    assert len(statuses_page.rows()) == len(STATUSES) + 1


def test_edit_status(statuses_page, unique):
    assert statuses_page.open_edit("To Review") == {"name": "To Review", "slug": "to_review"}
    statuses_page.open()

    statuses_page.update("To Review", {"name": f"Review {unique}", "slug": f"review_{unique}"})

    assert statuses_page.has_row(f"Review {unique}")
    statuses_page.wait_row_gone("To Review")
    assert f"review_{unique}" in statuses_page.column("slug")


def test_delete_status(statuses_page):
    statuses_page.delete("To Publish")

    statuses_page.wait_row_gone("To Publish")
    assert "To Publish" not in statuses_page.column("name")
    assert len(statuses_page.rows()) == len(STATUSES) - 1


def test_delete_selected_statuses(statuses_page):
    statuses_page.select("Draft")
    statuses_page.select("Published")

    statuses_page.bulk_delete()

    statuses_page.wait_row_gone("Draft")
    statuses_page.wait_row_gone("Published")
    assert statuses_page.column("name") == ["To Review", "To Be Fixed", "To Publish"]


def test_delete_all_statuses(statuses_page):
    statuses_page.select_all()
    statuses_page.bulk_delete()

    assert statuses_page.empty_message() == "No Task statuses yet."
    assert statuses_page.driver.find_elements(*statuses_page.ROWS) == []
