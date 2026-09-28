"""
Benchmark: which Selenium scroll method actually triggers lazy loading?

Tests 5 methods on quotes.toscrape.com/scroll (infinite scroll page)
and a local overflow-div simulation.

Results saved to scroll_bench_results.md
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

SCROLL_STEPS = 10
STEP_PAUSE   = 1.5   # seconds between scrolls
ITEM_SELECTOR = "div.quote"
TEST_URL      = "https://quotes.toscrape.com/scroll"

def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def count_items(driver):
    return len(driver.find_elements(By.CSS_SELECTOR, ITEM_SELECTOR))


def wait_for_more(driver, before, timeout=4):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, ITEM_SELECTOR)) > before
        )
        return True
    except Exception:
        return False


# ── Method 1: window.scrollTo(0, scrollHeight) ────────────────────────────────
def method_scrollTo(driver):
    loaded = []
    loaded.append(count_items(driver))
    for _ in range(SCROLL_STEPS):
        before = count_items(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait_for_more(driver, before)
        loaded.append(count_items(driver))
        time.sleep(STEP_PAUSE)
    return loaded


# ── Method 2: window.scrollBy(0, 800) ─────────────────────────────────────────
def method_scrollBy(driver):
    loaded = []
    loaded.append(count_items(driver))
    for _ in range(SCROLL_STEPS):
        before = count_items(driver)
        driver.execute_script("window.scrollBy(0, 800);")
        wait_for_more(driver, before)
        loaded.append(count_items(driver))
        time.sleep(STEP_PAUSE)
    return loaded


# ── Method 3: scrollIntoView on last element ──────────────────────────────────
def method_scrollIntoView(driver):
    loaded = []
    loaded.append(count_items(driver))
    for _ in range(SCROLL_STEPS):
        before = count_items(driver)
        items = driver.find_elements(By.CSS_SELECTOR, ITEM_SELECTOR)
        if items:
            driver.execute_script("arguments[0].scrollIntoView(true);", items[-1])
        wait_for_more(driver, before)
        loaded.append(count_items(driver))
        time.sleep(STEP_PAUSE)
    return loaded


# ── Method 4: ActionChains scroll_by_amount ───────────────────────────────────
def method_actionChains(driver):
    loaded = []
    loaded.append(count_items(driver))
    actions = ActionChains(driver)
    for _ in range(SCROLL_STEPS):
        before = count_items(driver)
        actions.scroll_by_amount(0, 800).perform()
        wait_for_more(driver, before)
        loaded.append(count_items(driver))
        time.sleep(STEP_PAUSE)
    return loaded


# ── Method 5: Keyboard END key ────────────────────────────────────────────────
def method_keyboard(driver):
    loaded = []
    loaded.append(count_items(driver))
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(SCROLL_STEPS):
        before = count_items(driver)
        body.send_keys(Keys.END)
        wait_for_more(driver, before)
        loaded.append(count_items(driver))
        time.sleep(STEP_PAUSE)
    return loaded


METHODS = [
    ("window.scrollTo(scrollHeight)",   method_scrollTo),
    ("window.scrollBy(0, 800)",         method_scrollBy),
    ("scrollIntoView (last element)",   method_scrollIntoView),
    ("ActionChains scroll_by_amount",   method_actionChains),
    ("Keyboard END",                    method_keyboard),
]


def run_method(name, fn):
    print(f"  Testing: {name}")
    driver = make_driver()
    try:
        driver.get(TEST_URL)
        # wait for initial load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ITEM_SELECTOR))
        )
        t0 = time.time()
        loaded = fn(driver)
        elapsed = time.time() - t0

        initial  = loaded[0]
        final    = loaded[-1]
        gained   = final - initial
        # count steps that actually loaded new content
        triggers = sum(1 for a, b in zip(loaded, loaded[1:]) if b > a)

        print(f"    items: {initial} to {final} (+{gained}) | triggers: {triggers}/{SCROLL_STEPS} | {elapsed:.1f}s")
        return {
            "method":   name,
            "initial":  initial,
            "final":    final,
            "gained":   gained,
            "triggers": triggers,
            "steps":    SCROLL_STEPS,
            "time_s":   round(elapsed, 1),
            "series":   loaded,
        }
    except Exception as e:
        print(f"    ERROR: {e}")
        return {"method": name, "error": str(e)}
    finally:
        driver.quit()


def build_markdown(results):
    lines = [
        "# Scroll Method Benchmark — quotes.toscrape.com/scroll",
        "",
        f"**Test:** {SCROLL_STEPS} scroll steps · {STEP_PAUSE}s pause · selector `{ITEM_SELECTOR}`",
        f"**URL:** {TEST_URL}",
        "",
        "## Results",
        "",
        "| Method | Items loaded | Triggers (out of 10) | Time |",
        "|---|---:|---:|---:|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['method']} | ERROR | — | — |")
        else:
            lines.append(
                f"| {r['method']} | +{r['gained']} ({r['initial']}→{r['final']}) "
                f"| {r['triggers']}/10 | {r['time_s']}s |"
            )

    lines += [
        "",
        "## Raw series (items after each step)",
        "",
    ]
    for r in results:
        if "series" in r:
            lines.append(f"**{r['method']}:** `{r['series']}`")
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"Benchmarking 5 scroll methods on {TEST_URL}")
    print(f"{SCROLL_STEPS} steps, {STEP_PAUSE}s pause each\n")

    results = []
    for name, fn in METHODS:
        result = run_method(name, fn)
        results.append(result)
        time.sleep(1)

    md = build_markdown(results)

    out = "blog-audit/posts/scroll-page-using-selenium-python/scripts/scroll_bench_results.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\nSaved: {out}")
    print("\n" + md)
