from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class JobsPage(BasePage):
    # Only prod
    DOMAINS = ("qajobs.qaharbor.com",)
    SIGN_IN = (By.LINK_TEXT, "Sign In")

    def wait_for_jobs_domain(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(host in d.current_url for host in self.DOMAINS)
        )
