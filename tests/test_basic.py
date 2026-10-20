import pytest

from tests.pages.login_page import LoginPage


@pytest.mark.smoke
def test_application_renders(driver, base_url):
    page = LoginPage(driver, base_url)
    page.open_route()

    username, password, sign_in = page.form_elements()

    assert username.get_attribute("type") == "text"
    assert password.get_attribute("type") == "password"
    assert sign_in.text.lower() == "sign in"
    assert sign_in.is_enabled()
