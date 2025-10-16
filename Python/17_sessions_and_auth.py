from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

with webdriver.Chrome() as driver:
    driver.get("https://example.com")

    # Login
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "login-btn").click()

    # Save cookies
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)

    # Load cookies later
    driver.get("https://example.com")
    with open("cookies.pkl", "rb") as f:
        for cookie in pickle.load(f):
            driver.add_cookie(cookie)
    driver.refresh()
