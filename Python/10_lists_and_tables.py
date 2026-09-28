from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/tables")

    # Rows of the first table
    rows = driver.find_elements(By.CSS_SELECTOR, "#table1 tbody tr")
    print(f"{len(rows)} rows")

    # Cells per row, as a list of dicts
    headers = [th.text for th in driver.find_elements(By.CSS_SELECTOR, "#table1 thead th")]
    data = []
    for row in rows:
        cells = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
        data.append(dict(zip(headers, cells)))

    for entry in data[:2]:
        print(entry)
