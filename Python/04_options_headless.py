from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1280,800")
options.add_argument("user-agent=UserAgent/1.0")

with webdriver.Chrome(options=options) as driver:
    driver.get("https://example.com")
    print(driver.current_url)


# Get the latest User-Agents here:
# https://hasdata.com/blog/user-agents-for-web-scraping