from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with webdriver.Chrome() as driver:
    driver.implicitly_wait(5)  # implicit wait for all find_element(s)
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

    # The element exists but stays hidden until Start is clicked
    driver.find_element(By.CSS_SELECTOR, "#start button").click()

    # Explicit wait for the text that appears after the loader
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4")))
    print(element.text)
