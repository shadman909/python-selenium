from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains

DEFAULT_TIMEOUT = 12

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll_into_view(self, locator, block="center", timeout=DEFAULT_TIMEOUT):
        el = self.wait_visible(locator, timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'instant',block:arguments[1],inline:'nearest'});",
            el, block
        )
        return el

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_center(self, element):
        ActionChains(self.driver).move_to_element(element).pause(0.05).click().perform()

    def click_offset(self, element, dx=6, dy=6):
        ActionChains(self.driver).move_to_element_with_offset(element, dx, dy).pause(0.05).click().perform()

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        last_err = None
        for _ in range(3):
            try:
                el = self.scroll_into_view(locator, block="center", timeout=timeout)
                WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                el.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException) as e:
                last_err = e
        el = self.scroll_into_view(locator, block="center", timeout=timeout)
        self.js_click(el)
        WebDriverWait(self.driver, 2).until(lambda d: True)

    def type(self, locator, text, clear_first=True):
        el = self.scroll_into_view(locator)
        if clear_first:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)
