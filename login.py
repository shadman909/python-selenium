import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Function to perform login
def login_to_saucedemo():
    # Setup Chrome browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.window_handles


    driver.get("https://www.saucedemo.com")
    print(" Opened SauceDemo login page")


    time.sleep(2)


    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    print("Entered username")


    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    print("enter the pass")


    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    print(" Clicked login")


    time.sleep(3)


    current_url = driver.current_url
    if "inventory" in current_url:
        print(" Login successful!")
    else:
        print(" Login failed!")

    # Close the browser
    time.sleep(2)
    driver.quit()
    print(" Browser closed")

# Call the function
login_to_saucedemo()
