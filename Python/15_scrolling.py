import time

from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/infinite_scroll")

    for step in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        blocks = driver.find_elements(By.CSS_SELECTOR, ".jscroll-added")
        print(f"after scroll {step + 1}: {len(blocks)} loaded blocks")
