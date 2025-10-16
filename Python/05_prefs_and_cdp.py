from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
prefs = {
    "profile.default_content_setting_values.images": 2,  # disable images
    "download.default_directory": "/tmp/downloads"       # auto-download path
}
options.add_experimental_option("prefs", prefs)

with webdriver.Chrome(options=options) as driver:
    driver.get("https://example.com")

    # Example of CDP command: block network requests to images
    driver.execute_cdp_cmd(
        "Network.setBlockedURLs", {"urls": ["*.png", "*.jpg", "*.gif"]}
    )