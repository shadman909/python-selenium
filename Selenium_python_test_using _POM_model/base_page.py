from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout=10):
        self.wait_clickable(locator, timeout).click()

    def type(self, locator, text, clear_first=True, timeout=10):
        el = self.wait_visible(locator, timeout)
        if clear_first:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)
