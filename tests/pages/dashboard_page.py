from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    WELCOME_TITLE = "Welcome to the administration"
    CONTENT = (By.XPATH, "//main//*[normalize-space()='Lorem ipsum sic dolor amet...']")

    def wait_loaded(self):
        self.visible(self.CONTENT)
        return self

    def content(self):
        return self.visible(self.CONTENT).text
