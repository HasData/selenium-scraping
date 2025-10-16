import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(new chrome.Options().headless()).build();

  try {
    await driver.get("https://example.com/");

    // Example of accessing shadow DOM element
    const host = await driver.findElement(By.css("shadow-elem"));
    const shadowRoot = await driver.executeScript("return arguments[0].shadowRoot", host);
    const child = await driver.executeScript("return arguments[0].querySelector('shadow-elem')", shadowRoot);

    console.log("Found element inside shadow DOM:", !!child);
  } finally {
    await driver.quit();
  }
}

main();
