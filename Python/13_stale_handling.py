from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

with webdriver.Chrome() as driver:
    driver.get("https://example.com/dynamic")

    for _ in range(5):
        try:
            elem = driver.find_element(By.ID, "dynamic-content")
            print(elem.text)
        except StaleElementReferenceException:
            print("Element went stale, retrying...")
            time.sleep(1)
            elem = driver.find_element(By.ID, "dynamic-content")
            print(elem.text)
