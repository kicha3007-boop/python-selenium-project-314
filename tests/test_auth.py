from selenium.webdriver.support import expected_conditions as EC

from tests.data import MENU, PASSWORD, USERNAME
from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


def test_sign_in(login_page, driver, base_url):
    login_page.login(USERNAME, PASSWORD)

    dashboard = DashboardPage(driver, base_url).wait_loaded()

    assert dashboard.content() == "Lorem ipsum sic dolor amet..."
    assert dashboard.title() == DashboardPage.WELCOME_TITLE
    assert dashboard.menu_items() == MENU


def test_sign_in_with_any_credentials(login_page, driver, base_url):
    login_page.login("someone@example.com", "another-password")

    dashboard = DashboardPage(driver, base_url).wait_loaded()

    assert dashboard.menu_items() == MENU


def test_logout(dashboard, driver, base_url):
    dashboard.logout()

    login_page = LoginPage(driver, base_url)
    assert all(element.is_displayed() for element in login_page.form_elements())
    assert driver.current_url.endswith("#/login")


def test_pages_require_login_after_logout(dashboard, driver, base_url):
    dashboard.logout()
    login_page = LoginPage(driver, base_url)
    login_page.form_elements()

    login_page.open_route("tasks")

    login_page.wait.until(EC.url_contains("#/login"))
    assert all(element.is_displayed() for element in login_page.form_elements())
