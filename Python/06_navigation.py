from selenium import webdriver

with webdriver.Chrome() as driver:
    driver.get("https://example.com")
    print(driver.title, driver.current_url)

    driver.refresh()  # reload page

    driver.get("https://example.com/next")
    driver.back()     # go back
    driver.forward()  # go forward
