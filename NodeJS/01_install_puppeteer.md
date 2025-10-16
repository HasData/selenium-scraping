## Install Selenium WebDriver for Node.js (2025)

This guide shows how to set up Selenium for Node.js 18+ with **automatic driver management**.

### Step 1: Initialize your project

```bash
mkdir selenium-nodejs
cd selenium-nodejs
npm init -y
````

### Step 2: Install Selenium

```bash
npm install selenium-webdriver
```

> No need to install `chromedriver` or `geckodriver` manually.
> New Selenium includes **Selenium Manager**, which downloads and manages the correct browser driver automatically.

### Step 3: Create a simple test

Create `test_driver.js`:

```javascript
const { Builder } = require('selenium-webdriver');

(async function test() {
    // Chrome is used by default; Selenium Manager handles the driver
    let driver = await new Builder().forBrowser('chrome').build();

    await driver.get('https://example.com');
    console.log(await driver.getTitle());

    await driver.quit();
})();
```

### Step 4: Run the test

```bash
node test_driver.js
```

You should see the page title printed in the console.

### Notes

* Selenium Manager automatically finds and downloads the correct driver for your browser.
* Works with **Chrome, Firefox, Edge** (Safari uses the built-in driver on MacOS).
* Async/await syntax is recommended for clarity and reliability.
* No additional driver configuration is needed for most use cases.
