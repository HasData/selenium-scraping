import { Builder } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const options = new chrome.Options().headless();
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(options).build();

  try {
    // Enable CDP (Chrome DevTools Protocol)
    const cdp = await driver.createCDPSession();
    await cdp.send("Network.enable");

    // Block selected resource types
    await cdp.send("Network.setBlockedURLs", {
      urls: ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.woff2", "*.css"],
    });

    await driver.get("https://example.com");
    console.log("Page loaded with blocked images/fonts/css");

  } finally {
    await driver.quit();
  }
}

main();