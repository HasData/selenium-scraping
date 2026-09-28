"""Is Selenium Wire still usable in 2026, checked in a throwaway venv.

Installs selenium-wire into a fresh venv (so its pins cannot touch the main
environment), records what pip resolves, then tries to import it and drive one
request through its proxy layer with the current Chrome. Also records the GitHub
archive status. Writes study/wire_check.json.
"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = pathlib.Path(__file__).resolve().parent.parent / "study"
S.mkdir(parents=True, exist_ok=True)
VENV = pathlib.Path(__file__).resolve().parent / ".wire-venv"
py = VENV / "Scripts" / "python.exe"

out = {}

r = subprocess.run(["gh", "api", "repos/wkeeling/selenium-wire",
                    "--jq", "{archived, pushed_at, open_issues_count}"],
                   capture_output=True, text=True, encoding="utf-8")
out["github"] = json.loads(r.stdout) if r.returncode == 0 else r.stderr.strip()[:200]

if not py.exists():
    subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
ins = subprocess.run([str(py), "-m", "pip", "install", "-q", "selenium-wire", "setuptools"],
                     capture_output=True, text=True, encoding="utf-8")
out["pip_install"] = dict(rc=ins.returncode, err=ins.stderr.strip()[-600:])

frz = subprocess.run([str(py), "-m", "pip", "list", "--format=freeze"],
                     capture_output=True, text=True, encoding="utf-8")
keep = [l for l in frz.stdout.splitlines()
        if l.split("==")[0].lower() in ("selenium-wire", "selenium", "blinker", "mitmproxy")]
out["resolved"] = keep

probe = r'''
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
try:
    from seleniumwire import webdriver
except Exception as exc:
    print("IMPORT-FAIL", type(exc).__name__, exc)
    raise SystemExit(0)
print("import OK")
try:
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    d = webdriver.Chrome(options=o)
    d.get("https://www.scrapethissite.com/pages/simple/")
    n = len(d.requests)
    statuses = [r.response.status_code for r in d.requests if r.response][:5]
    print("RUN-OK", n, "requests captured, first statuses", statuses)
    d.quit()
except Exception as exc:
    print("RUN-FAIL", type(exc).__name__, str(exc)[:400])
'''
(pathlib.Path(__file__).parent / "_wire_probe.py").write_text(probe, encoding="utf-8")
run = subprocess.run([str(py), str(pathlib.Path(__file__).parent / "_wire_probe.py")],
                     capture_output=True, text=True, encoding="utf-8", timeout=180)
out["probe_stdout"] = run.stdout.strip()
out["probe_stderr"] = run.stderr.strip()[-400:]

(S / "wire_check.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
