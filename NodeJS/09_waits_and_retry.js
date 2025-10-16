import { Builder, By, until } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function retry(fn, attempts = 3, delayMs = 500) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (i < attempts - 1) await new Promise(r => setTimeout(r, delayMs * (i + 1)));
    }
  }
  throw lastErr;
}

async function main() {
  const options = new chrome.Options().headless();
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(options).build();

  try {
    await driver.get("https://example.com");

    // Explicit wait: wait until element with ID 'main' is present and visible (it is just example!)
    const locator = By.id("main");
    const el = await driver.wait(until.elementLocated(locator), 10000);
    await driver.wait(until.elementIsVisible(el), 10000);

    // Use retry wrapper for flaky operations
    const text = await retry(async () => {
      const e = await driver.findElement(By.id("main"));
      return e.getText();
    }, 4, 500);

    console.log("Text:", await text);

  } finally {
    await driver.quit();
  }
}

main().catch(console.error);
