import { Builder, By } from "selenium-webdriver";
import chrome from "selenium-webdriver/chrome";
import fs from "fs";

async function main() {
  const driver = await new Builder().forBrowser("chrome").setChromeOptions(new chrome.Options().headless()).build();

  try {
    await driver.get("https://example.com");

    const rows = await driver.findElements(By.css("tr"));
    const data = [];

    for (let i = 1; i < rows.length; i++) {
      const cols = await rows[i].findElements(By.css("td"));
      const values = await Promise.all(cols.map(async c => (await c.getText()).trim()));
      if (values.length) data.push({ Company: values[0], Contact: values[1], Country: values[2] });
    }

    fs.writeFileSync("table.json", JSON.stringify(data, null, 2));

    const csv = ["Company,Contact,Country", ...data.map(r => `${r.Company},${r.Contact},${r.Country}`)].join("\n");
    fs.writeFileSync("table.csv", csv);

    console.log("Exported table.json and table.csv");
  } finally {
    await driver.quit();
  }
}

main();
