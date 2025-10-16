from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

download_dir = "/downloads"

options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)

with webdriver.Chrome(options=options) as driver:
    driver.get("https://example.com")
    driver.find_element(By.ID, "download-btn").click()

    # Wait for download to complete
    timeout = 10
    while timeout > 0:
        if any(fname.endswith(".crdownload") for fname in os.listdir(download_dir)):
            time.sleep(1)
            timeout -= 1
        else:
            break
