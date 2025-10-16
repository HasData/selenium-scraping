from selenium import webdriver

# Chrome
driver = webdriver.Chrome()
driver.get("https://example.com")
driver.quit()

# Firefox
driver = webdriver.Firefox()
driver.get("https://example.com")
driver.quit()

# Edge
driver = webdriver.Edge()
driver.get("https://example.com")
driver.quit()

# Safari (Mac only)
driver = webdriver.Safari()
driver.get("https://example.com")
driver.quit()
