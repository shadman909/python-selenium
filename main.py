from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get("https://www.facebook.com")
time.sleep(3)
print(driver.title)

driver.quit()