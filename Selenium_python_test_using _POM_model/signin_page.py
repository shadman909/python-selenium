from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class SignInPage(BasePage):
    # Username/Email inputs
    USERNAME_INPUTS = (
        (By.NAME, "username"),
        (By.ID, "username"),
        (By.NAME, "email"),
        (By.ID, "email"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name*='user' i]"),
        (By.CSS_SELECTOR, "input[name*='mail' i]"),
        (By.CSS_SELECTOR, "input[autocomplete='username']"),
    )

    # Password inputs
    PASSWORD_INPUTS = (
        (By.NAME, "password"),
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
    )

    # Submit controls
    SUBMIT_BUTTONS = (
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[normalize-space()='Sign In' or normalize-space()='Log in']"),
        (By.XPATH, "//button[contains(., 'Sign In') or contains(., 'Log in')]"),
        (By.XPATH, "//input[@type='submit']"),
    )

    ERROR_BANNERS = (
        (By.CSS_SELECTOR, "[role='alert']"),
        (By.CSS_SELECTOR, ".alert-danger, .alert-error, .error-message"),
        (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'invalid')]"),
        (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'incorrect')]"),
    )

    def _first_present(self, locators, timeout=10):
        last = None
        for loc in locators:
            try:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(loc))
            except Exception as e:
                last = e
        if last:
            raise last
        raise RuntimeError("No locator matched")

    def fill_username(self, text, clear_first=True):
        el = self._first_present(self.USERNAME_INPUTS, timeout=10)
        if clear_first:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)

    def fill_password(self, text, clear_first=True):
        el = self._first_present(self.PASSWORD_INPUTS, timeout=10)
        if clear_first:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)

    def submit(self):
        # Prefer a clickable button
        for loc in self.SUBMIT_BUTTONS:
            try:
                btn = WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable(loc))
                btn.click()
                return
            except Exception:
                continue
        # Fallback: press Enter on password field
        try:
            self._first_present(self.PASSWORD_INPUTS, timeout=3).submit()
            return
        except Exception:
            pass
        raise RuntimeError("Could not find a Sign In submit control")

    def wait_for_login_result(self, timeout=15):
        """
        ("ok", None) on success (URL hints OR visible logged-in UI)
        ("error", msg) on clear error banner
        ("timeout", reason) otherwise
        """
        target_host = "qajobs.qaharbor.com"
        success_path_hints = ("/account", "/dashboard", "/profile")

        def has_success(d):
            url = (d.current_url or "").lower()
            if target_host in url and any(h in url for h in success_path_hints):
                return True
            # UI markers that indicate logged-in state
            markers = [
                (By.LINK_TEXT, "My account"),
                (By.LINK_TEXT, "My Account"),
                (By.LINK_TEXT, "Log Out"),
                (By.PARTIAL_LINK_TEXT, "Account"),
            ]
            for m in markers:
                try:
                    el = WebDriverWait(d, 0.2).until(EC.visibility_of_element_located(m))
                    if el and el.is_displayed():
                        return True
                except Exception:
                    continue
            return False

        def get_error(d):
            for loc in self.ERROR_BANNERS:
                try:
                    el = WebDriverWait(d, 0.5).until(EC.visibility_of_element_located(loc))
                    if el:
                        txt = (el.text or "").strip()
                        if txt and len(txt) < 400:
                            return txt
                except Exception:
                    continue
            return None

        import time
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if has_success(self.driver):
                return "ok", None
            err = get_error(self.driver)
            if err:
                return "error", err
            time.sleep(0.3)

        if has_success(self.driver):
            return "ok", None
        err = get_error(self.driver)
        if err:
            return "error", err
        return "timeout", "No success markers or explicit error detected"
