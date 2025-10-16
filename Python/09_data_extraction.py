from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://example.com")

    # element.text normalization
    elem = driver.find_element(By.CSS_SELECTOR, "h1")
    text = elem.text.strip().replace("\n", " ")
    print(text)

    # get_attribute example
    link = driver.find_element(By.TAG_NAME, "a")
    href = link.get_attribute("href")
    print(href)
