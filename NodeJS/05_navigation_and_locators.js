import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(new chrome.Options().headless()).build();

  try {
    await driver.get("https://example.com");
    console.log("Title:", await driver.getTitle());

    // Navigate forward, backward, refresh
    await driver.navigate().refresh();
    await driver.navigate().to("https://example.org");
    await driver.navigate().back();

    // Find elements
    const heading = await driver.findElement(By.css("h1"));
    console.log("Heading:", await heading.getText());

  } finally {
    await driver.quit();
  }
}

main();
