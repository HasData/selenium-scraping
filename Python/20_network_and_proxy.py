from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as wire_webdriver

# CDP example: block images/fonts ---
options = Options()
with webdriver.Chrome(options=options) as driver:
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.png", "*.jpg", "*.woff2"]})
    driver.get("https://example.com")

# Selenium Wire: proxy example ---
proxy_options = {
    'proxy': {
        'http': 'http://user:pass@127.0.0.1:8000',
        'https': 'https://user:pass@127.0.0.1:8000',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

driver = wire_webdriver.Chrome(seleniumwire_options=proxy_options)
driver.get("https://example.com")
for request in driver.requests:
    if "api" in request.url:
        print(request.url, request.response.status_code)
driver.quit()
