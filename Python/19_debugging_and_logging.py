import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)

with webdriver.Chrome() as driver:
    driver.get("https://quotes.toscrape.com")

    # Screenshot full page
    driver.save_screenshot("screenshot.png")
    logging.info("Screenshot saved as screenshot.png")

    # Screenshot element
    elem = driver.find_element(By.CSS_SELECTOR, "h1")
    elem.screenshot("element.png")
    logging.info("Element screenshot saved as element.png")

    # Log page title
    logging.info(f"Page title: {driver.title}")
