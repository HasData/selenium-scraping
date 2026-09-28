"""What each Selenium configuration costs, measured.

One scenario (open a page, wait for the data element, read it) runs in eight
configurations, 20 runs each, medians reported:

  headed          - plain webdriver.Chrome()
  headless        - --headless=new
  images-off      - headless + images disabled via prefs
  cdp-block       - headless + CDP Network.setBlockedURLs for images/fonts/css
  js-off          - headless + JavaScript disabled via prefs
  proxy           - headless + a local forward proxy (proxy.py)
  uc              - undetected-chromedriver, headless
  (selenium-wire is tested separately in a throwaway venv, see wire_check.py)

Per run: cold start (driver constructor), time to element (get + explicit wait),
RSS of the whole browser process tree after load, and bytes transferred per the
Resource Timing API. Separately, one sannysoft check per relevant config counts
failed detector rows. Target page: scrapethissite.com/pages/simple/ (a scraping
sandbox). Writes study/config_bench.json incrementally.
"""
import json
import pathlib
import statistics
import subprocess
import sys
import time

import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = pathlib.Path(__file__).resolve().parent.parent / "study"
S.mkdir(parents=True, exist_ok=True)
OUT = S / "config_bench.json"
URL = "https://www.scrapethissite.com/pages/simple/"
WAIT_SEL = ".country"
RUNS = 20
PROXY_PORT = 18931




def tree_rss_mb(root_pid):
    try:
        root = psutil.Process(root_pid)
        procs = [root] + root.children(recursive=True)
        return round(sum(p.memory_info().rss for p in procs
                         if p.is_running()) / 1024 / 1024)
    except psutil.Error:
        return None


def base_options(headless=True):
    o = webdriver.ChromeOptions()
    if headless:
        o.add_argument("--headless=new")
    o.add_argument("--window-size=1280,900")
    return o


def make_driver(config):
    if config == "headed":
        return webdriver.Chrome(options=base_options(headless=False))
    if config == "headless":
        return webdriver.Chrome(options=base_options())
    if config == "images-off":
        o = base_options()
        o.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        return webdriver.Chrome(options=o)
    if config == "cdp-block":
        d = webdriver.Chrome(options=base_options())
        d.execute_cdp_cmd("Network.enable", {})
        d.execute_cdp_cmd("Network.setBlockedURLs",
                          {"urls": ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif",
                                    "*.woff", "*.woff2", "*.ttf", "*.css"]})
        return d
    if config == "js-off":
        o = base_options()
        o.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
        return webdriver.Chrome(options=o)
    if config == "proxy":
        o = base_options()
        o.add_argument(f"--proxy-server=http://127.0.0.1:{PROXY_PORT}")
        return webdriver.Chrome(options=o)
    if config == "uc":
        import undetected_chromedriver as uc
        return uc.Chrome(headless=True, use_subprocess=True)
    raise ValueError(config)


def one_run(config):
    t0 = time.perf_counter()
    d = make_driver(config)
    t1 = time.perf_counter()
    try:
        d.get(URL)
        WebDriverWait(d, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, WAIT_SEL)))
        t2 = time.perf_counter()
        pid = getattr(d, "browser_pid", None)
        if not pid and getattr(d, "service", None) and d.service.process:
            pid = d.service.process.pid
        mem = tree_rss_mb(pid) if pid else None
        try:
            transferred = d.execute_script(
                "var e=performance.getEntriesByType('resource');"
                "var n=performance.getEntriesByType('navigation');"
                "return e.concat(n).reduce(function(a,x){return a+(x.transferSize||0)},0);")
        except Exception:
            transferred = None
        return dict(start=round(t1 - t0, 3), to_element=round(t2 - t1, 3),
                    rss_mb=mem, bytes=transferred)
    finally:
        try:
            d.quit()
        except Exception:
            pass


def sannysoft(config):
    d = make_driver(config)
    try:
        d.get("https://bot.sannysoft.com/")
        time.sleep(4)
        html = d.page_source
        return dict(failed=html.count('class="failed'), passed=html.count('class="passed'))
    finally:
        try:
            d.quit()
        except Exception:
            pass


def run_all(state):
    configs = ["headed", "headless", "images-off", "cdp-block", "js-off", "proxy", "uc"]
    for config in configs:
        if config in state and state[config].get("runs_n", 0) >= RUNS:
            continue
        runs = []
        fails = 0
        for i in range(RUNS):
            try:
                runs.append(one_run(config))
            except Exception as exc:
                fails += 1
                print(f"  {config} run {i+1}: {type(exc).__name__}: {exc}")
                if fails >= 3 and not runs:
                    break
            time.sleep(0.5)
        entry = dict(runs_n=len(runs), failures=fails)
        for key in ("start", "to_element", "rss_mb", "bytes"):
            vals = [r[key] for r in runs if r.get(key) is not None]
            entry[key + "_median"] = round(statistics.median(vals), 3) if vals else None
        state[config] = entry
        OUT.write_text(json.dumps(state, indent=1), encoding="utf-8")
        print(config, "->", entry)

    for config in ["headed", "headless", "uc"]:
        key = "sannysoft_" + config
        if key in state:
            continue
        try:
            state[key] = sannysoft(config)
        except Exception as exc:
            state[key] = dict(error=f"{type(exc).__name__}: {exc}")
        OUT.write_text(json.dumps(state, indent=1), encoding="utf-8")
        print(key, "->", state[key])


def main():
    proxy_proc = subprocess.Popen([sys.executable, "-m", "proxy", "--hostname", "127.0.0.1",
                                   "--port", str(PROXY_PORT), "--log-level", "ERROR"])
    time.sleep(2)
    try:
        one_run("headless")  # warmup, not recorded
    except Exception as exc:
        print("warmup:", type(exc).__name__, exc)
    state = {}
    if OUT.exists():
        state = json.loads(OUT.read_text(encoding="utf-8"))
    try:
        run_all(state)
    finally:
        proxy_proc.terminate()
    print("saved config_bench.json")


if __name__ == "__main__":
    main()
