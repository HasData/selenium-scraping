# Install Selenium for Python

This example shows how to install the latest Selenium version for Python and verify that everything is working.

## Step 1: Install Selenium

Use pip to install Selenium:

```bash
pip install selenium
````

> The version 4.36 was the latest stable at the time of writing.
> Using the latest version ensures compatibility with Selenium Manager and modern browsers.

## Step 2: Verify Installation

Open a Python shell and run:

```python
import selenium
print(selenium.__version__)
```

You should see `4.36.0` (or the version you installed).
This confirms Selenium is installed correctly and ready for use.

## Step 3: Check Browser Compatibility

Selenium 4.10+ comes with **Selenium Manager**, which automatically finds and downloads the correct WebDriver for Chrome, Firefox, Edge, or Safari.
No manual WebDriver download is needed for most cases.

```python
from selenium import webdriver

# Test Chrome
driver = webdriver.Chrome()
driver.quit()

# Test Firefox
driver = webdriver.Firefox()
driver.quit()
```

Once this runs without errors, your environment is ready for web scraping with Selenium.
