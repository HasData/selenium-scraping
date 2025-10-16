from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with webdriver.Chrome() as driver:
    driver.implicitly_wait(5)  # implicit wait for all find_element(s)
    driver.get("https://example.com")

    # Explicit wait
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, "main")))
    print(element.text)
