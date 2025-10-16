import { Builder } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const options = new chrome.Options()
    .headless()
    .windowSize({ width: 1280, height: 800 })
    .addArguments("--user-agent=MyNodeSeleniumBot/1.0");

  const driver = await new Builder().forBrowser("chrome").setChromeOptions(options).build();

  try {
    await driver.get("https://example.com");
    console.log(await driver.getCurrentUrl());
  } finally {
    await driver.quit();
  }
}

main();