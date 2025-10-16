from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://shop.polymer-project.org/")

    # Access shadow root using JavaScript
    host = driver.find_element(By.CSS_SELECTOR, "shop-app")
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", host)

    # Now find element inside shadow DOM
    shop_title = shadow_root.find_element(By.CSS_SELECTOR, "app-header h1")
    print(shop_title.text)
