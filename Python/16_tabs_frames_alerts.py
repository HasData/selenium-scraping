from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://the-internet.herokuapp.com/iframe")

    # Open new tab and switch between windows
    driver.execute_script("window.open('https://the-internet.herokuapp.com/javascript_alerts');")
    driver.switch_to.window(driver.window_handles[1])
    print("second tab:", driver.title)

    # Handle an alert on this tab
    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    alert = driver.switch_to.alert
    print("alert says:", alert.text)
    alert.accept()

    # Back to the first tab and into its iframe
    driver.switch_to.window(driver.window_handles[0])
    iframe = driver.find_element(By.ID, "mce_0_ifr")
    driver.switch_to.frame(iframe)
    body = driver.find_element(By.TAG_NAME, "body")
    print("iframe body:", body.text[:40])
    driver.switch_to.default_content()
