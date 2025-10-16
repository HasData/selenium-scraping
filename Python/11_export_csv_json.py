import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

data = []

with webdriver.Chrome() as driver:
    driver.get("https://example.com/table")
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    for row in rows:
        cols = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            data.append({"col1": cols[0], "col2": cols[1]})

# Export CSV
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["col1", "col2"])
    writer.writeheader()
    writer.writerows(data)

# Export JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
