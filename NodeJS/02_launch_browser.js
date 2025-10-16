import { Builder } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";

async function main() {
  const driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(new chrome.Options())
    .build();

  try {
    await driver.get("https://example.com");
    const title = await driver.getTitle();
    console.log("Title:", title);
  } finally {
    await driver.quit();
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
