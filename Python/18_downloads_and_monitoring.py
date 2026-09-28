import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)

with webdriver.Chrome(options=options) as driver:
    driver.get("https://the-internet.herokuapp.com/download")

    # Click the first listed file
    link = driver.find_element(By.CSS_SELECTOR, ".example a")
    filename = link.text
    link.click()

    # Wait for the download to land
    timeout = 15
    path = os.path.join(download_dir, filename)
    for _ in range(timeout):
        if os.path.exists(path) and not os.path.exists(path + ".crdownload"):
            break
        time.sleep(1)

    if os.path.exists(path):
        print(f"downloaded {filename}, {os.path.getsize(path)} bytes")
    else:
        print(f"download did not finish within {timeout}s")
