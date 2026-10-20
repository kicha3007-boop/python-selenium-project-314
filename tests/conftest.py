import uuid

import pytest

from tests.data import PASSWORD, USERNAME
from tests.pages.dashboard_page import DashboardPage
from tests.pages.labels_page import LabelsPage
from tests.pages.login_page import LoginPage
from tests.pages.statuses_page import StatusesPage
from tests.pages.tasks_page import TasksPage
from tests.pages.users_page import UsersPage


@pytest.fixture
def unique():
    """Короткий суффикс, чтобы созданные записи не путались с исходными."""
    return uuid.uuid4().hex[:6]


@pytest.fixture
def login_page(driver, base_url):
    page = LoginPage(driver, base_url)
    page.open()
    return page


@pytest.fixture
def dashboard(login_page, driver, base_url):
    login_page.login(USERNAME, PASSWORD)
    return DashboardPage(driver, base_url).wait_loaded()


@pytest.fixture
def users_page(dashboard, driver, base_url):
    return UsersPage(driver, base_url).open()


@pytest.fixture
def statuses_page(dashboard, driver, base_url):
    return StatusesPage(driver, base_url).open()


@pytest.fixture
def labels_page(dashboard, driver, base_url):
    return LabelsPage(driver, base_url).open()


@pytest.fixture
def tasks_page(dashboard, driver, base_url):
    return TasksPage(driver, base_url).open()
