import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.signin_page import SignInPage

USERNAME_OR_EMAIL = "shad009"
PASSWORD = "12345sqa"

@pytest.mark.order(1)
def test_qajobs_login_flow(driver):
    home = HomePage(driver)
    signin = SignInPage(driver)


    home.open()

   
    time.sleep(2)

    # 3) Click the Sign In button (from your screenshot)
    home.click_sign_in_once(settle_seconds=0)  # we already slept above

    # 4) Ensure we actually navigated to /signin
    WebDriverWait(driver, 10).until(lambda d: "/signin" in (d.current_url or "").lower())

    # 5) Fill the form
    signin.fill_username(USERNAME_OR_EMAIL)
    signin.fill_password(PASSWORD)

    # 6) Submit
    signin.submit()

    # 7) Verify success (URL hints OR logged-in UI)
    result, detail = signin.wait_for_login_result(timeout=15)
    assert result == "ok", f"Login failed: {detail or 'Stayed on /signin'}"
