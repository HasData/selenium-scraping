from selenium import webdriver
from selenium.webdriver.common.by import By
import time

with webdriver.Chrome() as driver:
    driver.get("https://example.com/infinite-scroll")

    # Scroll to element
    elem = driver.find_element(By.CSS_SELECTOR, "#footer")
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)

    # Infinite scroll
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
