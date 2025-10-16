from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

with webdriver.Chrome() as driver:
    driver.get("https://example.com/login")

    # Fill input fields
    username = driver.find_element(By.ID, "username")
    username.send_keys("my_user")

    password = driver.find_element(By.ID, "password")
    password.send_keys("my_password")

    # Submit form
    password.send_keys(Keys.RETURN)

    # Click button
    btn = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
    btn.click()
