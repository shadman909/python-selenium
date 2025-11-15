from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import time

class SignUpPage(BasePage):
    # Top menu
    SIGN_UP_HOVER = (By.XPATH, "//span[contains(@class,'jet-nav-link-text')][normalize-space()='Sign Up']")
    CANDIDATE_OPTION = (By.XPATH, "(//span[normalize-space()='Candidate'])[1]")

    # Registration fields
    USERNAME = (By.ID, "login")
    EMAIL = (By.ID, "_candidate-email")
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "first_name_copy")  # as confirmed

    # Checkbox: real input + the visual square
    TERMS_CHECKBOX = (By.CSS_SELECTOR, "label.jet-form-builder__field-label.for-checkbox input[type='checkbox']")
    TERMS_SQUARE   = (By.XPATH, "//label[contains(@class,'jet-form-builder__field-label') and contains(@class,'for-checkbox')]/span[1]")
    TERMS_LABEL    = (By.XPATH, "//label[contains(@class,'jet-form-builder__field-label') and contains(@class,'for-checkbox')]")

    # Register controls
    REGISTER_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Register Now') or contains(normalize-space(),'Register')]")
    REGISTER_LINK   = (By.XPATH, "//a[contains(normalize-space(),'Register Now') or contains(normalize-space(),'Register')]")

    # Disable links inside label temporarily
    def _disable_label_links(self, label_el):
        self.driver.execute_script(
            """
                       (function(lbl){
                         if(!lbl) return;
                         lbl.querySelectorAll('a').forEach(a=>{
                           a.dataset._orig_href = a.getAttribute('href') || '';
                           a.setAttribute('href','javascript:void(0)');
                           a.style.pointerEvents='none';
                         });
                       })(arguments[0]);
                       """,
            label_el
        )

    def _restore_label_links(self, label_el):
        self.driver.execute_script(
            """
            (function(lbl){
              if(!lbl) return;
              lbl.querySelectorAll('a').forEach(a=>{
                const href=a.dataset._orig_href||'';
                if(href) a.setAttribute('href',href); else a.removeAttribute('href');
                a.style.pointerEvents='';
                delete a.dataset._orig_href;
              });
            })(arguments[0]);
            """,
            label_el
        )

    # Actions
    def select_candidate(self):
        self.scroll_into_view(self.SIGN_UP_HOVER)
        self.click(self.CANDIDATE_OPTION)

    def fill_registration_form(self, username, email, first_name, last_name):
        self.type(self.USERNAME, username)
        self.type(self.EMAIL, email)
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)

    def agree_to_terms_and_conditions(self):
        square = self.scroll_into_view(self.TERMS_SQUARE, block="center", timeout=8)
        label  = self.scroll_into_view(self.TERMS_LABEL,  block="center", timeout=8)

        self._disable_label_links(label)
        try:
            try:
                self.click_offset(square, 6, 6)   # click inside the square
            except Exception:
                self.click_center(square)
        finally:
            self._restore_label_links(label)

        # Ensure real input is checked
        try:
            checkbox = self.wait_visible(self.TERMS_CHECKBOX, timeout=3)
            if not self.driver.execute_script("return arguments[0].checked===true;", checkbox):
                self.driver.execute_script(
                    "arguments[0].checked=true;"
                    "try{arguments[0].dispatchEvent(new Event('input',{bubbles:true}));}catch(e){}"
                    "try{arguments[0].dispatchEvent(new Event('change',{bubbles:true}));}catch(e){}",
                    checkbox
                )
        except Exception:
            pass

    def click_register_link(self, stay_seconds: int = 10):
        """Click Register, detect outcome, and keep page open for stay_seconds."""
        start_url = self.driver.current_url

        for locator in (self.REGISTER_BUTTON, self.REGISTER_LINK):
            try:
                self.scroll_into_view(locator)
                try:
                    self.click(locator)
                except Exception:
                    el = self.wait_visible(locator, timeout=2)
                    self.js_click(el)

                # Detect outcome
                outcome = "No visible change"
                try:
                    WebDriverWait(self.driver, 12).until(
                        EC.any_of(
                            EC.url_changes(start_url),
                            EC.presence_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Success')]")),
                            EC.presence_of_element_located((By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'error') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'failed')]")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".jet-form-builder-message, .jet-form-builder__message"))
                        )
                    )
                    new_url = self.driver.current_url
                    if new_url != start_url:
                        outcome = f"Page navigated to: {new_url}"
                    else:
                        try:
                            err = self.driver.find_element(By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'error') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'failed')]")
                            outcome = f"Error message: {err.text.strip()}"
                        except Exception:
                            try:
                                ok = self.driver.find_element(By.XPATH, "//*[contains(normalize-space(),'Success')]")
                                outcome = f"Success message: {ok.text.strip()}"
                            except Exception:
                                try:
                                    msg = self.driver.find_element(By.CSS_SELECTOR, ".jet-form-builder-message, .jet-form-builder__message")
                                    outcome = f"Message: {msg.text.strip()}"
                                except Exception:
                                    pass
                except TimeoutException:
                    outcome = "No navigation or message detected within 12s"

                print(f"[DEBUG] After Register click: {outcome}")

                # Keep page visible
                if stay_seconds and stay_seconds > 0:
                    time.sleep(stay_seconds)

                return outcome
            except Exception:
                continue

        raise TimeoutException("Could not click Register (button or link).")
