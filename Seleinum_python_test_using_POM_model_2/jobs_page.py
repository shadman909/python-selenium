from selenium.webdriver.common.by import By
from .base_page import BasePage

class JobsPage(BasePage):
    SIGN_UP_BUTTON = (By.LINK_TEXT, "Sign Up")

    def click_sign_up(self):
        self.click(self.SIGN_UP_BUTTON)
