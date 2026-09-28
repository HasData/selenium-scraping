from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://quotes.toscrape.com")

    # element.text normalization
    elem = driver.find_element(By.CSS_SELECTOR, "h1")
    text = elem.text.strip().replace("\n", " ")
    print(text)

    # get_attribute example
    link = driver.find_element(By.CSS_SELECTOR, ".quote span a")
    href = link.get_attribute("href")
    print(href)

    # collecting a list of fields
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"{len(quotes)} quotes, first: {quotes[0].text[:50]}")
