from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    SIGN_IN = (By.XPATH, "//form//button[@type='submit'][normalize-space()='Sign in']")

    def open(self):
        self.open_route("login")
        self.visible(self.USERNAME)

    def login(self, username, password):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SIGN_IN)

    def form_elements(self):
        return [self.visible(locator) for locator in (self.USERNAME, self.PASSWORD, self.SIGN_IN)]
