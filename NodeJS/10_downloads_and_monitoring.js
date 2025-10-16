import { Builder } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";
import fs from "fs";
import path from "path";

async function waitForDownload(dir, timeout = 30_000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const files = fs.readdirSync(dir);
    // Chrome temp extension while downloading: .crdownload
    const inProgress = files.some(f => f.endsWith(".crdownload"));
    const finished = files.filter(f => !f.endsWith(".crdownload") && !f.endsWith(".tmp"));
    if (!inProgress && finished.length > 0) return finished;
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error("Download timeout");
}

async function main() {
  const downloadDir = path.resolve("./downloads");
  if (!fs.existsSync(downloadDir)) fs.mkdirSync(downloadDir, { recursive: true });

  const options = new chrome.Options().headless();
  options.addArguments(`--window-size=1200,800`);

  const driver = await new Builder().forBrowser("chrome").setChromeOptions(options).build();

  try {
    // create CDP session and set download behavior
    const cdp = await driver.createCDPSession();
    await cdp.send("Page.enable");
    await cdp.send("Browser.setDownloadBehavior", {
      behavior: "allow",
      downloadPath: downloadDir,
    });

    await driver.get("https://example.com");
    // Trigger download (update selector as needed)
    const btn = await driver.findElement({ css: "#download-btn" });
    await btn.click();

    const files = await waitForDownload(downloadDir, 30_000);
    console.log("Downloaded files:", files);

  } finally {
    await driver.quit();
  }
}

main().catch(console.error);
