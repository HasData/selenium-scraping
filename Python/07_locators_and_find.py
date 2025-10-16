from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://example.com")

    # Single element
    elem = driver.find_element(By.ID, "main")
    print(elem.text)

    # Multiple elements
    items = driver.find_elements(By.CSS_SELECTOR, ".item")
    for i in items:
        print(i.text)

    # Using other locators
    driver.find_element(By.NAME, "q")
    driver.find_element(By.CLASS_NAME, "btn")
    driver.find_element(By.TAG_NAME, "h1")
    driver.find_element(By.LINK_TEXT, "Read more")
    driver.find_element(By.PARTIAL_LINK_TEXT, "Read")
    driver.find_element(By.XPATH, "//div[@id='content']")
