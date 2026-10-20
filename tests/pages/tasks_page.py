from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage, visible_text, xpath_literal

COLUMN = "//main//div[@data-rfd-droppable-id]"
CARD = "//div[@data-rfd-draggable-id]"
CARD_TITLE = "//div[contains(@class, 'MuiTypography-h5')]"
ANNOUNCEMENTS_SCRIPT = (
    "return Array.from(document.querySelectorAll('[aria-live]'))"
    ".map((node) => node.textContent).join(' ');"
)


class TasksPage(BasePage):
    """Канбан-доска: колонки — статусы, карточки — задачи."""

    route = "tasks"

    COLUMNS = (By.XPATH, COLUMN)
    COLUMN_TITLES = (By.XPATH, f"{COLUMN}/preceding-sibling::h6")
    CARD_TITLES = (By.XPATH, f"{COLUMN}{CARD}{CARD_TITLE}")
    CREATE = (By.XPATH, "//main//a[@aria-label='Create']")
    SAVE = (By.XPATH, "//main//form//button[@aria-label='Save']")
    DELETE = (By.XPATH, "//main//form//button[@aria-label='Delete']")
    TITLE_INPUT = (By.XPATH, "//main//form//input[@name='title']")
    CONTENT_INPUT = (By.XPATH, "//main//form//textarea[@name='content']")

    def open(self):
        self.open_route(self.route)
        return self.wait_loaded()

    def wait_loaded(self):
        self.wait.until(EC.url_matches(r"#/tasks/?(\?.*)?$"))
        self.visible(self.CARD_TITLES)
        return self

    def column_titles(self):
        return [title.text for title in self.all_visible(self.COLUMN_TITLES)]

    def card_titles(self):
        return [title.text for title in self.all_visible(self.CARD_TITLES)]

    def _column(self, status):
        return f"{COLUMN}[preceding-sibling::h6[normalize-space()={xpath_literal(status)}]]"

    def _card(self, title, scope="//main"):
        return f"{scope}{CARD}[.{CARD_TITLE}[normalize-space()={xpath_literal(title)}]]"

    def cards_in(self, status):
        self.visible((By.XPATH, self._column(status)))
        titles = self.driver.find_elements(By.XPATH, f"{self._column(status)}{CARD}{CARD_TITLE}")
        return [title.text for title in titles if title.is_displayed()]

    def wait_card_in(self, title, status):
        self.visible((By.XPATH, self._card(title, scope=self._column(status))))

    def wait_card_gone(self, title):
        self.wait_hidden((By.XPATH, self._card(title)))

    def status_of(self, title):
        locator = (By.XPATH, f"{self._card(title)}/ancestor::div[@data-rfd-droppable-id]")
        column = self.visible(locator)
        return column.find_element(By.XPATH, "./preceding-sibling::h6").text

    def card_text(self, title):
        return self.visible((By.XPATH, self._card(title))).text

    def fill_task_form(self, title=None, content=None, assignee=None, status=None):
        if assignee is not None:
            self.choose_option("assignee_id", assignee)
        if title is not None:
            self.fill(self.TITLE_INPUT, title)
        if content is not None:
            self.fill(self.CONTENT_INPUT, content)
        if status is not None:
            self.choose_option("status_id", status)

    def open_create_form(self):
        self.click(self.CREATE)
        self.wait.until(EC.url_contains("#/tasks/create"))
        return [self.visible(locator) for locator in (self.TITLE_INPUT, self.CONTENT_INPUT)]

    def create(self, title, content, assignee, status):
        self.open_create_form()
        self.fill_task_form(title=title, content=content, assignee=assignee, status=status)
        self.click(self.SAVE)
        # после создания react-admin открывает форму редактирования новой задачи
        self.wait.until(EC.url_matches(r"#/tasks/\d+$"))
        return self.open()

    def open_edit(self, title):
        self.click((By.XPATH, f"{self._card(title)}//a[@aria-label='Edit']"))
        self.wait.until(EC.url_matches(r"#/tasks/\d+$"))
        return self.form_values()

    def form_values(self):
        title = self.visible(self.TITLE_INPUT)
        status = self.visible(
            (By.XPATH, "//main//form//input[@name='status_id']/preceding-sibling::div")
        )
        # задача и список статусов подгружаются асинхронно: ждём, пока форма заполнится
        self.wait.until(lambda _: title.get_attribute("value") and visible_text(status))
        return {
            "title": title.get_attribute("value"),
            "content": self.visible(self.CONTENT_INPUT).get_attribute("value"),
            "status": visible_text(status),
        }

    def update(self, card_title, **changes):
        self.open_edit(card_title)
        self.fill_task_form(**changes)
        self.click(self.SAVE)
        return self.wait_loaded()

    def delete(self, title):
        self.open_edit(title)
        self.click(self.DELETE)
        return self.wait_loaded()

    def open_show(self, title):
        self.click((By.XPATH, f"{self._card(title)}//a[@aria-label='Show']"))
        self.wait.until(EC.url_matches(r"#/tasks/\d+/show$"))
        return self.visible((By.XPATH, "//main//form")).text

    def filter_by(self, field, option):
        self.choose_option(field, option, scope="//main//form")
        self.wait.until(EC.url_contains(f"{field}%22"))
        return self.wait_loaded()

    def move_card_right(self, title):
        """Перетаскивает карточку в соседнюю колонку справа с клавиатуры.

        Доска построена на @hello-pangea/dnd: пробел поднимает карточку,
        стрелка переносит её, повторный пробел — бросает.
        """
        card = self.wait.until(EC.element_to_be_clickable((By.XPATH, self._card(title))))
        card.send_keys(Keys.SPACE)
        self._wait_announcement("lifted")
        card.send_keys(Keys.ARROW_RIGHT)
        self._wait_announcement("moved")
        card.send_keys(Keys.SPACE)
        self._wait_announcement("dropped")

    def _wait_announcement(self, word):
        self.wait.until(lambda driver: word in driver.execute_script(ANNOUNCEMENTS_SCRIPT))
