from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10
# пустой выпадающий список MUI содержит невидимый пробел нулевой ширины
ZERO_WIDTH_SPACE = chr(0x200B)


def visible_text(element):
    return element.text.replace(ZERO_WIDTH_SPACE, "").strip()


def by_text(text, tag="*"):
    """XPath-локатор элемента с точным видимым текстом."""
    return By.XPATH, f"//{tag}[normalize-space()={xpath_literal(text)}]"


def xpath_literal(text):
    """Строка в кавычках для XPath: апостроф внутри текста не ломает выражение."""
    return f'"{text}"' if "'" in text else f"'{text}'"


class BasePage:
    """Общие действия со страницами react-admin: ожидания, ввод, выпадающие списки."""

    TITLE = (By.ID, "react-admin-title")
    PROFILE_BUTTON = (By.CSS_SELECTOR, "header button[aria-label='Profile']")
    LOGOUT_ITEM = (By.XPATH, "//li[@role='menuitem'][normalize-space()='Logout']")
    MENU_ITEMS = (By.CSS_SELECTOR, "main ul[role='menu'] a[role='menuitem']")
    OPTION = "//ul[@role='listbox']//li[@role='option'][normalize-space()={}]"

    def __init__(self, driver, base_url, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)
        # для шагов, которые сами повторяют действие, пока страница перерисовывается
        self.retrying_wait = WebDriverWait(
            driver,
            timeout,
            poll_frequency=0.3,
            ignored_exceptions=(
                NoSuchElementException,
                StaleElementReferenceException,
                ElementNotInteractableException,
                ElementClickInterceptedException,
            ),
        )

    def open_route(self, route=""):
        self.driver.get(f"{self.base_url}/#/{route}")

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def all_visible(self, locator):
        self.visible(locator)
        return [item for item in self.driver.find_elements(*locator) if item.is_displayed()]

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_hidden(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))

    def fill(self, locator, value):
        field = self.wait.until(EC.element_to_be_clickable(locator))
        # clear() не вызывает onChange у React-полей, поэтому стираем как пользователь
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(value)

    def choose_option(self, field_name, option_text, scope="//main//form"):
        """Выбирает значение в выпадающем списке MUI и ждёт, пока оно отобразится в поле.

        Список вариантов react-admin подгружает асинхронно и перерисовывает,
        поэтому клик по варианту может не дойти: тогда список открывается заново.
        """
        combobox = (
            By.XPATH,
            f"{scope}//input[@name='{field_name}']/preceding-sibling::div[@role='combobox']",
        )
        option = (By.XPATH, self.OPTION.format(xpath_literal(option_text)))

        def option_selected(driver):
            if visible_text(driver.find_element(*combobox)) == option_text:
                return True
            options = [item for item in driver.find_elements(*option) if item.is_displayed()]
            if options:
                options[0].click()
            elif not driver.find_elements(By.XPATH, "//ul[@role='listbox']"):
                driver.find_element(*combobox).click()
            return False

        self.retrying_wait.until(option_selected)
        self.wait_hidden(option)

    def title(self):
        return self.visible(self.TITLE).text

    def menu_items(self):
        return [item.text for item in self.all_visible(self.MENU_ITEMS)]

    def logout(self):
        self.click(self.PROFILE_BUTTON)
        self.click(self.LOGOUT_ITEM)
