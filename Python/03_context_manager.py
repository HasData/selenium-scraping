from selenium import webdriver

# Chrome example
with webdriver.Chrome() as driver:
    driver.get("https://example.com")
    print(driver.title)
# driver.quit() is automatically called after the block
