from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://qaharbor.com/"

    QA_JOBS = (By.LINK_TEXT, "QA Jobs")

    def go_to_site(self):
        self.driver.get(self.URL)

    def click_qa_jobs(self):
        self.click(self.QA_JOBS)
