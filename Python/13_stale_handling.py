from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/dynamic_content")

    # Grab a content block, then reload: the old reference goes stale
    block = driver.find_element(By.CSS_SELECTOR, "#content .row")
    driver.refresh()

    try:
        print(block.text[:40])
    except StaleElementReferenceException:
        print("stale reference after refresh, re-finding")
        block = driver.find_element(By.CSS_SELECTOR, "#content .row")
        print("fresh text:", block.text[:40].replace("\n", " "))
