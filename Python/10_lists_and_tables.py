from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://example.com/table")

    # Extract table rows
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    for row in rows:
        cols = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
        print(cols)

    # Extract list items
    items = driver.find_elements(By.CSS_SELECTOR, "ul li")
    for item in items:
        print(item.text)
