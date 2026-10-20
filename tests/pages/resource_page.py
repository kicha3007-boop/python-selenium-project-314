from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage, by_text, xpath_literal


class ResourcePage(BasePage):
    """Раздел react-admin со списком-таблицей и формами создания и редактирования."""

    route = ""
    title_text = ""
    empty_text = ""
    form_fields = ()

    ROWS = (By.XPATH, "//main//table/tbody/tr")
    CREATE = (By.XPATH, "//main//a[@aria-label='Create']")
    SAVE = (By.XPATH, "//main//form//button[@aria-label='Save']")
    DELETE = (By.XPATH, "//main//form//button[@aria-label='Delete']")
    # сам input у чекбокса MUI прозрачный, кликаем по его обёртке
    SELECT_ALL = (By.XPATH, "//main//table/thead//input[@type='checkbox']/parent::span")
    BULK_TOOLBAR = "//main//*[@data-test='bulk-actions-toolbar']"
    BULK_DELETE = (By.XPATH, f"{BULK_TOOLBAR}//button[@aria-label='Delete']")
    SELECTED_COUNT = (By.XPATH, f"{BULK_TOOLBAR}//h6")

    def open(self):
        self.open_route(self.route)
        return self.wait_loaded()

    def wait_loaded(self):
        self.wait.until(EC.url_matches(rf"#/{self.route}/?(\?.*)?$"))
        self.visible(self.ROWS)
        return self

    def rows(self):
        return self.all_visible(self.ROWS)

    def column(self, field):
        locator = (By.XPATH, f"//main//table/tbody/tr/td[contains(@class, 'column-{field}')]")
        return [cell.text for cell in self.all_visible(locator)]

    def headers(self):
        locator = (By.XPATH, "//main//table/thead//th[@scope='col']")
        return [cell.text for cell in self.all_visible(locator) if cell.text]

    def _row(self, text):
        return By.XPATH, f"//main//table/tbody/tr[td[normalize-space()={xpath_literal(text)}]]"

    def has_row(self, text):
        self.visible(self._row(text))
        return True

    def wait_row_gone(self, text):
        self.wait_hidden(self._row(text))

    def _field(self, name):
        return By.XPATH, f"//main//form//*[@name='{name}']"

    def open_create_form(self):
        self.click(self.CREATE)
        self.wait.until(EC.url_contains(f"#/{self.route}/create"))
        return self.form_inputs()

    def form_inputs(self):
        return [self.visible(self._field(name)) for name in self.form_fields]

    def fill_form(self, values):
        for name, value in values.items():
            self.fill(self._field(name), value)

    def form_values(self):
        first_field = self.visible(self._field(self.form_fields[0]))
        # запись подгружается асинхронно: ждём, пока форма заполнится
        self.wait.until(lambda _: first_field.get_attribute("value"))
        return {
            name: self.visible(self._field(name)).get_attribute("value")
            for name in self.form_fields
        }

    def save(self):
        self.click(self.SAVE)

    def create(self, values):
        self.open_create_form()
        self.fill_form(values)
        self.save()
        # после создания react-admin открывает форму редактирования новой записи
        self.wait.until(EC.url_matches(rf"#/{self.route}/\d+$"))

    def open_edit(self, text):
        self.click(
            (By.XPATH, f"//main//table/tbody/tr/td[normalize-space()={xpath_literal(text)}]")
        )
        self.wait.until(EC.url_matches(rf"#/{self.route}/\d+$"))
        return self.form_values()

    def update(self, text, values):
        self.open_edit(text)
        self.fill_form(values)
        self.save()
        return self.wait_loaded()

    def delete(self, text):
        self.open_edit(text)
        self.click(self.DELETE)
        return self.wait_loaded()

    def select(self, text):
        checkbox = (By.XPATH, f"{self._row(text)[1]}/td[1]//input[@type='checkbox']/parent::span")
        self.click(checkbox)

    def select_all(self):
        self.click(self.SELECT_ALL)

    def selected_count(self):
        return self.visible(self.SELECTED_COUNT).text

    def bulk_delete(self):
        self.click(self.BULK_DELETE)

    def empty_message(self):
        return self.visible(by_text(self.empty_text)).text

    def field_error(self, text):
        return self.visible((By.XPATH, f"//main//form//p[normalize-space()={xpath_literal(text)}]"))
