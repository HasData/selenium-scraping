from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://example.com")

    # Open new tab
    driver.execute_script("window.open('https://hasdata.com/');")
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)

    # Switch back
    driver.switch_to.window(driver.window_handles[0])

    # Switch to iframe
    iframe = driver.find_element(By.CSS_SELECTOR, "#my-iframe")
    driver.switch_to.frame(iframe)
    driver.find_element(By.CSS_SELECTOR, "button").click()
    driver.switch_to.default_content()

    # Handle alert
    driver.execute_script("alert('Hello!');")
    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
