from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/login")

    # Fill the form and submit (the sandbox's published demo credentials)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    banner = driver.find_element(By.ID, "flash")
    print(banner.text.split("\n")[0])

    # Log back out through the button
    driver.find_element(By.CSS_SELECTOR, "a.button").click()
    print("back at:", driver.current_url)
