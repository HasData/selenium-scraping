import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/login")

    # Login with the sandbox's published demo credentials
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Save the session cookies
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)
    print(f"saved {len(cookies)} cookies")

    # A fresh visit plus the saved cookies keeps the session alive
    driver.get("https://the-internet.herokuapp.com/secure")
    with open("cookies.pkl", "rb") as f:
        for cookie in pickle.load(f):
            driver.add_cookie(cookie)
    driver.refresh()
    print("session page:", driver.find_element(By.TAG_NAME, "h2").text)
