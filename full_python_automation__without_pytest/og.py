import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ===== Setup Chrome Driver =====
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # Incognito mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

# ===== Login Function =====
def login_to_saucedemo(driver):
    driver.get("https://www.saucedemo.com")
    print("Opened SauceDemo login page")
    time.sleep(2)

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    assert "inventory" in driver.current_url, "Login failed"
    print("Login successful")

# ===== Sort Products =====
def sort_products(driver):
    print("Sorting products using dropdown...")

    def get_dropdown():
        return Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
        ))

    get_dropdown().select_by_visible_text("Name (A to Z)")
    time.sleep(2)
    print("Sorted by Name (A to Z)")

    get_dropdown().select_by_visible_text("Name (Z to A)")
    time.sleep(2)
    print("Sorted by Name (Z to A)")

    get_dropdown().select_by_visible_text("Price (low to high)")
    time.sleep(2)
    print("Sorted by Price (low to high)")

    get_dropdown().select_by_visible_text("Price (high to low)")
    time.sleep(2)
    print("Sorted by Price (high to low)")

# ===== Add to Cart (by fixed ID) =====
def add_to_cart(driver):
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)
    print("Fixed product 'Backpack' added to cart")

# ===== Dynamically Add Product by Name with Index =====

def add_product_by_name_with_index(driver, product_name):
    print(f"Searching for '{product_name}' in the product list...")
    time.sleep(2)  # Added a sleep before starting the search (to make it more visible)

    product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for index, item in enumerate(product_names):
        name = item.text.strip()
        if name.lower() == product_name.lower():
            print(f"Product '{name}' found at position {index}")
            add_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to cart')]")
            if index < len(add_buttons):
                time.sleep(2)  # Slow down before clicking the "Add to Cart" button
                add_buttons[index].click()
                print(f"'{name}' added to cart.")
                time.sleep(2)  # Added delay after the click
                return
            else:
                raise Exception("Button index mismatch")
    raise Exception(f"Product '{product_name}' not found.")

# ===== Dynamically Add Multiple Products =====
def add_multiple_products(driver, product_names):
    print(f"Adding multiple products: {product_names}")
    available_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    add_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to cart')]")

    for index, item in enumerate(available_names):
        name = item.text.strip()
        if name in product_names and index < len(add_buttons):
            add_buttons[index].click()
            print(f"'{name}' added to cart.")
            time.sleep(1)

# ===== Cancel Checkout =====
def cancel_checkout(driver):
    print("Canceling checkout...")

    # Ensure we're on the cart page first
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)

    # Now click the checkout button
    driver.find_element(By.ID, "checkout").click()
    time.sleep(2)

    assert "checkout-step-one" in driver.current_url, "Not on checkout form page"
    print("On checkout info page")

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    time.sleep(1)

    driver.find_element(By.ID, "cancel").click()
    time.sleep(2)

    assert "cart" in driver.current_url, f"Cancel did not return to cart. Current URL: {driver.current_url}"
    print("Checkout canceled and returned to cart.")

# ===== Proceed to Checkout =====
def proceed_to_checkout(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)

    assert "checkout-step-one" in driver.current_url, "Not on checkout form page"
    print("On checkout info page")

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    time.sleep(1)

    driver.find_element(By.ID, "continue").click()
    time.sleep(2)

    assert "checkout-step-two" in driver.current_url, "Did not reach overview page"
    print("Checkout information submitted")

# ===== Finish Checkout =====
def finish_checkout(driver):
    driver.find_element(By.ID, "finish").click()
    time.sleep(2)

    msg = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU FOR YOUR ORDER" in msg.upper(), "Order not completed"
    print("Order completed successfully")

# ===== Logout =====
def logout(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(1)
    assert "saucedemo.com" in driver.current_url and "login" in driver.page_source.lower(), "Logout failed"
    print("Logout successful")

# ===== Main Test Flow =====
def main():
    driver = setup_driver()
    try:
        login_to_saucedemo(driver)
        #sort_products(driver)

        # Add fixed product
       # add_to_cart(driver)

        # Add one product dynamically by name
        add_product_by_name_with_index(driver, "Sauce Labs Onesie")

        # Add multiple products
       # add_multiple_products(driver, ["Test.allTheThings() T-Shirt (Red)", "Sauce Labs Bike Light"])

        # Cancel checkout
        #cancel_checkout(driver)

        # Proceed to checkout (if needed)
        proceed_to_checkout(driver)
        finish_checkout(driver)
        logout(driver)

        print("Selected test steps completed.")
    finally:
        driver.quit()
        print("Browser closed.")

# ===== Run Script =====
if __name__ == "__main__":
    main()
