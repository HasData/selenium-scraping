// nodejs/11_proxy_and_stealth.js
import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";
import proxy from "selenium-webdriver/proxy";

async function applyBasicStealth(driver) {
  // remove navigator.webdriver and set some common properties
  await driver.executeScript(function () {
    Object.defineProperty(navigator, "webdriver", { get: () => undefined });
    // emulate languages
    Object.defineProperty(navigator, "languages", { get: () => ["en-US", "en"] });
    // emulate plugins length
    Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3] });
  });
}

async function main() {
  // Example proxy (host:port). For proxies with auth, use a proxy tool or extension.
  const proxyHost = "127.0.0.1:3128";

  const options = new chrome.Options().headless();
  options.addArguments("--window-size=1280,800");
  options.addArguments("--disable-blink-features=AutomationControlled");
    // Get the latest User-Agents here:
    // https://hasdata.com/blog/user-agents-for-web-scraping

  options.addArguments("--user-agent=UserAgent/1.1");

  const driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(options)
    .setProxy(proxy.manual({ http: proxyHost, https: proxyHost }))
    .build();

  try {
    await driver.get("https://example.com");
    await applyBasicStealth(driver);

    const title = await driver.getTitle();
    console.log("Title via proxy:", title);

    // example request/response check
    const el = await driver.findElement(By.css("h1"));
    console.log("H1:", await el.getText());

  } finally {
    await driver.quit();
  }
}

main().catch(console.error);