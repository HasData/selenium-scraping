from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/login")

    # Single element by ID
    elem = driver.find_element(By.ID, "username")
    print("by id:", elem.get_attribute("name"))

    # By NAME
    driver.find_element(By.NAME, "password")

    # By CSS selector, single and multiple
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    print("button text:", button.text.strip())
    labels = driver.find_elements(By.CSS_SELECTOR, "label")
    print("labels:", [l.text for l in labels])

    # By tag and by link text
    h2 = driver.find_element(By.TAG_NAME, "h2")
    print("h2:", h2.text)
    driver.get("https://the-internet.herokuapp.com/")
    link = driver.find_element(By.LINK_TEXT, "Form Authentication")
    partial = driver.find_element(By.PARTIAL_LINK_TEXT, "Form")
    print("link href:", link.get_attribute("href"))

    # By XPath
    header = driver.find_element(By.XPATH, "//h1[@class='heading']")
    print("xpath h1:", header.text)
