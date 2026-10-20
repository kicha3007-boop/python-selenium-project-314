from tests.data import LABELS


def test_labels_list_shows_all_labels(labels_page):
    assert len(labels_page.rows()) == len(LABELS)
    assert labels_page.column("name") == LABELS


def test_label_create_form_opens(labels_page):
    (name,) = labels_page.open_create_form()

    assert name.get_attribute("name") == "name"
    assert name.get_attribute("value") == ""


def test_create_label(labels_page, unique):
    name = f"urgent-{unique}"

    labels_page.create({"name": name})
    labels_page.open()

    assert labels_page.has_row(name)
    assert labels_page.column("name") == [*LABELS, name]


def test_edit_label(labels_page, unique):
    assert labels_page.open_edit("enhancement") == {"name": "enhancement"}
    labels_page.open()

    labels_page.update("enhancement", {"name": f"improvement-{unique}"})

    assert labels_page.has_row(f"improvement-{unique}")
    labels_page.wait_row_gone("enhancement")
    assert len(labels_page.rows()) == len(LABELS)


def test_delete_label(labels_page):
    labels_page.delete("bug")

    labels_page.wait_row_gone("bug")
    assert labels_page.column("name") == LABELS[1:]


def test_delete_selected_labels(labels_page):
    labels_page.select("task")
    labels_page.select("critical")

    labels_page.bulk_delete()

    labels_page.wait_row_gone("critical")
    assert labels_page.column("name") == ["bug", "feature", "enhancement"]


def test_delete_all_labels(labels_page):
    labels_page.select_all()
    labels_page.bulk_delete()

    assert labels_page.empty_message() == "No Labels yet."
    assert labels_page.driver.find_elements(*labels_page.ROWS) == []
