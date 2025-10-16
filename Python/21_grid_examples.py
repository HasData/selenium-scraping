# This example demonstrates how to run Selenium tests in parallel using Selenium Grid.
# Pre-requisites:
# 1. Download Selenium Server (standalone or hub/node setup) from https://www.selenium.dev/downloads/
# 2. Start the Hub: java -jar selenium-server-<version>.jar hub
# 3. Start one or more Nodes: java -jar selenium-server-<version>.jar node --hub http://localhost:4444/grid/register

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

grid_url = "http://localhost:4444/wd/hub"

# Remote Chrome instances
driver1 = webdriver.Remote(
    command_executor=grid_url,
    desired_capabilities=DesiredCapabilities.CHROME
)
driver2 = webdriver.Remote(
    command_executor=grid_url,
    desired_capabilities=DesiredCapabilities.CHROME
)

driver1.get("https://example.com")
driver2.get("https://example.org")

driver1.quit()
driver2.quit()
