import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def login_to_saucedemo():
    # Set up Chrome browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()


    driver.get("https://www.saucedemo.com")
    print("Opened SauceDemo website")


    time.sleep(2)

    # using XPath
    username = driver.find_element("xpath", '//*[@id="user-name"]')
    username.send_keys("standard_user")
    print("Entered username")

    # using XPath
    password = driver.find_element("xpath", '//*[@id="password"]')
    password.send_keys("secret_sauce")
    print("Entered password")

    # using attributes and values
    login_button = driver.find_element("xpath", '//*[@id="login-button"]')
    login_button.click()
    print("Clicked login button")


    time.sleep(3)


    current_url = driver.current_url
    if "inventory" in current_url:
        print("Login successful!")
    else:
        print("Login failed!")

    # Close the browser
    time.sleep(2)
    driver.quit()
    print("Browser closed")

# Call the function
login_to_saucedemo()
