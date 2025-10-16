import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(new chrome.Options().headless()).build();

  try {
    await driver.get("https://example.com");

    const element = await driver.findElement(By.css("h1"));
    let text = await element.getText();
    text = text.trim().replace(/\s+/g, " "); // normalize whitespace

    console.log("Normalized text:", text);

    const link = await driver.findElement(By.css("a"));
    const href = await link.getAttribute("href");
    console.log("Link href:", href);

  } finally {
    await driver.quit();
  }
}

main();
