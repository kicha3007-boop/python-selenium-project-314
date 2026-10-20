from tests.data import USER_EMAILS


def test_users_list_shows_all_users(users_page):
    assert len(users_page.rows()) == len(USER_EMAILS)
    assert users_page.column("email") == USER_EMAILS


def test_users_list_shows_key_fields(users_page):
    assert {"Email", "First name", "Last name"} <= set(users_page.headers())
    assert users_page.column("firstName")[:2] == ["John", "Jack"]
    assert users_page.column("lastName")[:2] == ["Doe", "Jons"]


def test_user_create_form_opens(users_page):
    fields = users_page.open_create_form()

    assert [field.get_attribute("name") for field in fields] == ["email", "firstName", "lastName"]
    assert all(field.get_attribute("value") == "" for field in fields)


def test_create_user(users_page, unique):
    email = f"new-{unique}@example.com"

    users_page.create({"email": email, "firstName": "Ivan", "lastName": f"Petrov{unique}"})
    users_page.open()

    assert users_page.has_row(email)
    assert len(users_page.rows()) == len(USER_EMAILS) + 1
    assert f"Petrov{unique}" in users_page.column("lastName")


def test_edit_form_is_prefilled(users_page):
    values = users_page.open_edit("jack@yahoo.com")

    assert values == {"email": "jack@yahoo.com", "firstName": "Jack", "lastName": "Jons"}


def test_edit_user(users_page, unique):
    email = f"jack-{unique}@example.com"

    users_page.update("jack@yahoo.com", {"email": email, "firstName": "Jackie"})

    assert users_page.has_row(email)
    users_page.wait_row_gone("jack@yahoo.com")
    assert "Jackie" in users_page.column("firstName")


def test_edit_user_rejects_invalid_email(users_page):
    users_page.open_edit("jack@yahoo.com")
    users_page.fill_form({"email": "not-an-email"})
    users_page.save()

    assert users_page.field_error("Incorrect email format").is_displayed()
    users_page.open()
    assert users_page.has_row("jack@yahoo.com")
    assert "not-an-email" not in users_page.column("email")


def test_delete_user(users_page):
    users_page.delete("jane@gmail.com")

    users_page.wait_row_gone("jane@gmail.com")
    assert len(users_page.rows()) == len(USER_EMAILS) - 1


def test_delete_selected_users(users_page):
    users_page.select("jack@yahoo.com")
    users_page.select("alice@hotmail.com")
    assert users_page.selected_count() == "2 items selected"

    users_page.bulk_delete()

    users_page.wait_row_gone("jack@yahoo.com")
    users_page.wait_row_gone("alice@hotmail.com")
    assert len(users_page.rows()) == len(USER_EMAILS) - 2


def test_delete_all_users(users_page):
    users_page.select_all()
    assert users_page.selected_count() == f"{len(USER_EMAILS)} items selected"

    users_page.bulk_delete()

    assert users_page.empty_message() == "No Users yet."
    assert users_page.driver.find_elements(*users_page.ROWS) == []
