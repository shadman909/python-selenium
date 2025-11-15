import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://qajobs.qaharbor.com/"

    # Exact match for your screenshot
    SIGNIN = (By.CSS_SELECTOR, "a.jet-auth-links__item[href*='/signin']")

    def open(self):
        self.driver.get(self.URL)

    def click_sign_in_once(self, settle_seconds: float = 1.5):

        # Small settle wait to avoid layout shift / click interception
        time.sleep(settle_seconds)
        self.click(self.SIGNIN, timeout=10)
