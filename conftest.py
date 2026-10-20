"""Настройка браузера и адреса приложения для всех тестов.

Тесты знают о приложении только его адрес — переменную окружения APP_BASE_URL.
"""

import os
import re
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

HEADLESS = os.getenv("HEADLESS", "true").lower() not in {"false", "0", "no"}
WINDOW_SIZE = os.getenv("BROWSER_WINDOW_SIZE", "1440,900")
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
RESULTS_DIR = Path(os.getenv("TEST_RESULTS_DIR", "test-results"))

# Пути к chromium и chromedriver из пакетов Debian/Ubuntu. Если их нет,
# Selenium Manager сам найдёт установленный Chrome и подходящий драйвер.
CHROME_BINARIES = ("/usr/bin/chromium", "/usr/bin/chromium-browser")
CHROMEDRIVER_BINARIES = ("/usr/bin/chromedriver",)


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: быстрая проверка, что приложение поднялось")


def _first_existing(env_name, candidates):
    path = os.getenv(env_name)
    if path:
        return path
    return next((item for item in candidates if Path(item).exists()), None)


def _chrome_options():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={WINDOW_SIZE}")
    binary = _first_existing("CHROME_BIN", CHROME_BINARIES)
    if binary:
        options.binary_location = binary
    return options


def _chrome_service():
    driver_path = _first_existing("CHROMEDRIVER_BIN", CHROMEDRIVER_BINARIES)
    return Service(executable_path=driver_path) if driver_path else Service()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("APP_BASE_URL")
    if not url:
        pytest.exit("Задайте APP_BASE_URL, например http://localhost:5173", returncode=2)
    return url.rstrip("/")


@pytest.fixture
def driver(request, base_url):
    browser = webdriver.Chrome(options=_chrome_options(), service=_chrome_service())
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    yield browser
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        _save_screenshot(browser, request.node.nodeid)
    browser.quit()


def _save_screenshot(browser, nodeid):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^\w.-]", "_", nodeid)
    browser.save_screenshot(str(RESULTS_DIR / f"{name}.png"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
