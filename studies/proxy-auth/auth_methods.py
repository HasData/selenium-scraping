"""Which proxy-authentication methods actually work in Selenium 4 with current Chrome.

Starts a local proxy that demands Basic auth, then drives Chrome through it six ways and records
what happens. Every method is tried headed and headless so the table can say where each one breaks.

Run: python auth_methods.py            (add --headless-only or --headed-only to shorten)
Writes study/auth_methods.json and prints the table.
"""
import argparse
import json
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = pathlib.Path(__file__).resolve().parent
STUDY = HERE.parent / "study"
STUDY.mkdir(parents=True, exist_ok=True)

HOST, PORT = "127.0.0.1", 8899
USER, PASSWORD = "scraper", "s3cret"
TARGET = "https://books.toscrape.com/"
EXPECT = "Books to Scrape"


def free_port(port):
    with socket.socket() as s:
        return s.connect_ex((HOST, port)) != 0


def start_proxy():
    """proxy.py with Basic auth. Returns the process and the log path."""
    log = STUDY / f"proxy-{int(time.time())}.log"
    proc = subprocess.Popen(
        [sys.executable, "-m", "proxy", "--hostname", HOST, "--port", str(PORT),
         "--basic-auth", f"{USER}:{PASSWORD}", "--log-file", str(log), "--log-level", "INFO"],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    for _ in range(40):
        if not free_port(PORT):
            return proc, log
        time.sleep(0.5)
    raise SystemExit("local proxy did not come up")


def auth_extension(directory):
    """MV3 extension that answers the proxy's auth challenge, the documented Chrome route."""
    d = pathlib.Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps({
        "name": "proxy auth",
        "version": "1.0",
        "manifest_version": 3,
        "permissions": ["webRequest", "webRequestAuthProvider"],
        "host_permissions": ["<all_urls>"],
        "background": {"service_worker": "background.js"},
    }), encoding="utf-8")
    (d / "background.js").write_text(
        "chrome.webRequest.onAuthRequired.addListener(\n"
        "  (details, callback) => callback({ authCredentials: { username: '%s', password: '%s' } }),\n"
        "  { urls: ['<all_urls>'] },\n"
        "  ['asyncBlocking']\n"
        ");\n" % (USER, PASSWORD), encoding="utf-8")
    return str(d)


def verdict_from(driver):
    title = (driver.title or "").strip()
    body = driver.page_source or ""
    if EXPECT.lower() in title.lower() or EXPECT.lower() in body.lower():
        return "page loaded", title
    for marker in ("ERR_", "Proxy Authentication Required", "407", "This site can", "not private"):
        if marker.lower() in body.lower():
            return "blocked", title or marker
    return "no page", title


def run_selenium(label, headless, build_options, extra=None):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    build_options(options)
    driver = None
    started = time.time()
    try:
        driver = webdriver.Chrome(options=options)
        if extra:
            extra(driver)
        driver.set_page_load_timeout(45)
        driver.get(TARGET)
        v, detail = verdict_from(driver)
        return {"verdict": v, "detail": detail[:120], "seconds": round(time.time() - started, 1)}
    except Exception as e:
        return {"verdict": "error", "detail": f"{type(e).__name__}: {str(e).splitlines()[0][:110]}",
                "seconds": round(time.time() - started, 1)}
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def run_seleniumbase(headless):
    started = time.time()
    try:
        from seleniumbase import Driver
        driver = Driver(browser="chrome", headless2=headless, proxy=f"{USER}:{PASSWORD}@{HOST}:{PORT}")
        try:
            driver.get(TARGET)
            v, detail = verdict_from(driver)
            return {"verdict": v, "detail": detail[:120], "seconds": round(time.time() - started, 1)}
        finally:
            driver.quit()
    except Exception as e:
        return {"verdict": "error", "detail": f"{type(e).__name__}: {str(e).splitlines()[0][:110]}",
                "seconds": round(time.time() - started, 1)}


def run_selenium_wire(headless):
    started = time.time()
    try:
        from seleniumwire import webdriver as wire_webdriver
        opts = {"proxy": {"http": f"http://{USER}:{PASSWORD}@{HOST}:{PORT}",
                          "https": f"http://{USER}:{PASSWORD}@{HOST}:{PORT}"}}
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        driver = wire_webdriver.Chrome(options=options, seleniumwire_options=opts)
        try:
            driver.get(TARGET)
            v, detail = verdict_from(driver)
            return {"verdict": v, "detail": detail[:120], "seconds": round(time.time() - started, 1)}
        finally:
            driver.quit()
    except Exception as e:
        return {"verdict": "error", "detail": f"{type(e).__name__}: {str(e).splitlines()[0][:110]}",
                "seconds": round(time.time() - started, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headless-only", action="store_true")
    ap.add_argument("--headed-only", action="store_true")
    args = ap.parse_args()
    modes = [False, True]
    if args.headless_only:
        modes = [True]
    if args.headed_only:
        modes = [False]

    proxy_proc, proxy_log = start_proxy()
    ext_dir = tempfile.mkdtemp(prefix="chrome-proxy-auth-")
    auth_extension(ext_dir)
    results = {}
    try:
        methods = [
            ("credentials in --proxy-server",
             lambda o: o.add_argument(f"--proxy-server=http://{USER}:{PASSWORD}@{HOST}:{PORT}")),
            ("--proxy-server without credentials",
             lambda o: o.add_argument(f"--proxy-server=http://{HOST}:{PORT}")),
            ("extension answering onAuthRequired",
             lambda o: (o.add_argument(f"--proxy-server=http://{HOST}:{PORT}"),
                        o.add_argument(f"--load-extension={ext_dir}"))),
        ]
        for headless in modes:
            mode = "headless" if headless else "headed"
            for label, build in methods:
                res = run_selenium(label, headless, build)
                results.setdefault(label, {})[mode] = res
                print(f"{label:38s} {mode:9s} {res['verdict']:12s} {res['seconds']:5.1f}s  {res['detail']}")
            res = run_selenium_wire(headless)
            results.setdefault("selenium-wire", {})[mode] = res
            print(f"{'selenium-wire':38s} {mode:9s} {res['verdict']:12s} {res['seconds']:5.1f}s  {res['detail']}")
            res = run_seleniumbase(headless)
            results.setdefault("seleniumbase proxy option", {})[mode] = res
            print(f"{'seleniumbase proxy option':38s} {mode:9s} {res['verdict']:12s} {res['seconds']:5.1f}s  {res['detail']}")
    finally:
        proxy_proc.terminate()
        try:
            proxy_proc.wait(timeout=10)
        except Exception:
            proxy_proc.kill()
        shutil.rmtree(ext_dir, ignore_errors=True)

    versions = {}
    try:
        import selenium
        versions["selenium"] = selenium.__version__
    except Exception:
        pass
    versions["python"] = sys.version.split()[0]
    out = {"target": TARGET, "proxy": f"{HOST}:{PORT} (proxy.py, Basic auth)", "versions": versions,
           "results": results}
    (STUDY / "auth_methods.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nsaved", STUDY / "auth_methods.json")
    if proxy_log.exists():
        text = proxy_log.read_text(encoding="utf-8", errors="replace")
        print("proxy log lines:", len(text.splitlines()))


if __name__ == "__main__":
    main()
