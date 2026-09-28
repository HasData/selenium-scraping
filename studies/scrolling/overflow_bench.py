"""Benchmark: scrolling INSIDE an overflow container (the popup case).

A local page simulates an Instagram-followers-style popup: a fixed-height
overflow-y div that lazy-appends a batch of 10 rows ~300ms after the scroll
position nears the bottom, up to 100 rows. Three techniques run against it:

  jump_once      driver.execute_script("scrollTop = scrollHeight") one time,
                 the snippet the article currently shows for overflow elements
  step_sleep     scrollTop += offsetHeight in a loop, fixed 1s pause per step
  step_wait      the same stepwise loop, but WebDriverWait for the row count
                 to grow instead of a fixed pause

Recorded per technique: rows loaded, wall time, and the row-count series.
Writes overflow_bench_results.md next to this script.
"""
import json
import pathlib
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = pathlib.Path(__file__).resolve().parent

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
#popup { height: 400px; width: 360px; overflow-y: scroll; border: 1px solid #999; }
.row { height: 48px; border-bottom: 1px solid #eee; padding: 4px; }
</style></head><body>
<div id="popup"></div>
<script>
const popup = document.getElementById('popup');
let total = 0, pending = false;
function addBatch() {
  for (let i = 0; i < 10 && total < 100; i++) {
    total += 1;
    const d = document.createElement('div');
    d.className = 'row'; d.textContent = 'follower ' + total;
    popup.appendChild(d);
  }
  pending = false;
}
popup.addEventListener('scroll', () => {
  if (pending || total >= 100) return;
  if (popup.scrollTop + popup.clientHeight >= popup.scrollHeight - 40) {
    pending = true;
    setTimeout(addBatch, 300);
  }
});
addBatch();
</script></body></html>"""

PAGE_FILE = HERE / "overflow_page.html"
PAGE_FILE.write_text(PAGE, encoding="utf-8")
URL = PAGE_FILE.as_uri()
MAX_STEPS = 20


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def rows(driver):
    return len(driver.find_elements(By.CSS_SELECTOR, "#popup .row"))


def run(name, technique):
    driver = make_driver()
    driver.get(URL)
    time.sleep(0.5)
    popup = driver.find_element(By.ID, "popup")
    series = [rows(driver)]
    t0 = time.time()
    technique(driver, popup, series)
    result = {"name": name, "rows": rows(driver), "seconds": round(time.time() - t0, 1),
              "series": series}
    driver.quit()
    print(result)
    return result


def jump_once(driver, popup, series):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", popup)
    time.sleep(1.5)
    series.append(rows(driver))


def step_sleep(driver, popup, series):
    for _ in range(MAX_STEPS):
        driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", popup)
        time.sleep(1.0)
        series.append(rows(driver))


def step_wait(driver, popup, series):
    stall = 0
    for _ in range(MAX_STEPS):
        before = rows(driver)
        driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", popup)
        at_bottom = driver.execute_script(
            "return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight - 1;", popup)
        if at_bottom:
            try:
                WebDriverWait(driver, 2).until(lambda d: rows(d) > before)
            except Exception:
                pass
        series.append(rows(driver))
        if at_bottom and series[-1] == before:
            stall += 1
            if stall >= 2:
                break
        else:
            stall = 0


results = [
    run("scrollTop = scrollHeight, single call (article's current snippet)", jump_once),
    run("scrollTop += offsetHeight loop, fixed 1s sleep", step_sleep),
    run("scrollTop += offsetHeight loop, WebDriverWait on row count", step_wait),
]

lines = ["# Overflow-container scroll benchmark (popup simulation)", "",
         f"Local page: 400px overflow-y div, 10-row batches appended ~300ms after the",
         f"scroll nears the bottom, 100 rows total. {MAX_STEPS} steps max per loop.", "",
         "| Technique | Rows loaded | Time |", "|---|---:|---:|"]
for r in results:
    lines.append(f"| {r['name']} | {r['rows']}/100 | {r['seconds']}s |")
lines += ["", "## Row-count series", ""]
for r in results:
    lines.append(f"**{r['name']}:** `{r['series']}`")
(HERE / "overflow_bench_results.md").write_text("\n".join(lines), encoding="utf-8")
print("saved overflow_bench_results.md")
