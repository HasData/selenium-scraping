![Python](https://img.shields.io/badge/python-3.7+-blue)
![Node.js](https://img.shields.io/badge/node.js-18+-green)
![Selenium](https://img.shields.io/badge/selenium-4.36+-blueviolet)

# Selenium Scraping Examples (Python & Node.js)
[![HasData_bannner](banner.png)](https://hasdata.com/)

This repo contains working **Selenium examples** for web scraping in **Python** and **Node.js**.  
It covers everything from driver setup, navigation, waits, element extraction, downloads, network/proxy management, to scaling strategies (Grid) and async scraping.

## Table of Contents

1. [Requirements](#requirements)  
2. [Project Structure](#project-structure)  
3. [Python Selenium Examples](#python-selenium-examples)  
4. [Node.js Selenium Examples](#nodejs-selenium-examples)   
5. [Notes](#notes)
6. [More Resources](#-more-resources)


## Requirements

- **Python 3.8+**  
- **pip**  
- **Node.js 18+**  
- **npm** or **yarn**


## Requirements

- **Node.js 18+**
- **npm** or **yarn**


## Project Structure

```
selenium-scraping/
│
├── python/
│   ├── 01_install_selenium.md
│   ├── 02_driver_initialization.py
│   ├── 03_context_manager.py
│   ├── 04_options_headless.py
│   ├── 05_prefs_and_cdp.py
│   ├── 06_navigation.py
│   ├── 07_locators_and_find.py
│   ├── 08_shadow_dom.py
│   ├── 09_data_extraction.py
│   ├── 10_lists_and_tables.py
│   ├── 11_export_csv_json.py
│   ├── 12_waits_and_sync.py
│   ├── 13_stale_handling.py
│   ├── 14_interactions.py
│   ├── 15_scrolling.py
│   ├── 16_tabs_frames_alerts.py
│   ├── 17_sessions_and_auth.py
│   ├── 18_downloads_and_monitoring.py
│   ├── 19_debugging_and_logging.py
│   ├── 20_network_and_proxy.py
│   ├── 21_grid_examples.py
│   ├── 22_scrapy_integration.py
│   └── 23_hasdata_async_example.py
│
├── nodejs/
│   ├── 01_install_selenium.md
│   ├── 02_launch_browser.js
│   ├── 03_options_headless.js
│   ├── 04_block_resources_cdp.js
│   ├── 05_navigation_and_locators.js
│   ├── 06_shadow_dom.js
│   ├── 07_data_extraction.js
│   ├── 08_tables_and_export.js
│   ├── 09_waits_and_retry.js
│   ├── 10_downloads_and_monitoring.js
│   └── 11_proxy_and_stealth.js
│
└── README.md
```

## Python Selenium Examples

All examples use **selenium 4+**:

- `02_driver_initialization.py` — Chrome/Firefox/Edge/Safari drivers  
- `03_context_manager.py` — auto-quit with context manager  
- `04_options_headless.py` — headless mode, window size, user-agent  
- `05_prefs_and_cdp.py` — prefs and CDP commands  
- `06_navigation.py` — get, refresh, back, forward  
- `07_locators_and_find.py` — By API, find_element(s)  
- `08_shadow_dom.py` — accessing shadow root  
- `09_data_extraction.py` — element.text normalization, get_attribute  
- `10_lists_and_tables.py` — scrape lists and tables  
- `11_export_csv_json.py` — CSV/JSON export  
- `12_waits_and_sync.py` — implicit vs explicit waits  
- `13_stale_handling.py` — StaleElementReferenceException  
- `14_interactions.py` — clicks, send_keys, forms  
- `15_scrolling.py` — scrollIntoView, infinite scroll  
- `16_tabs_frames_alerts.py` — tabs, iframes, alerts  
- `17_sessions_and_auth.py` — login and cookies  
- `18_downloads_and_monitoring.py` — auto-download, monitor completion  
- `19_debugging_and_logging.py` — screenshots, logs  
- `20_network_and_proxy.py` — CDP, Selenium Wire, proxies  
- `21_grid_examples.py` — Selenium Grid remote driver examples  
- `22_scrapy_integration.py` — scrapy-selenium integration  
- `23_hasdata_async_example.py` — async scraping example

---

## Node.js Selenium Examples

All examples use **selenium-webdriver**:

- `02_driver_initialization.js` — Chrome/Firefox drivers  
- `03_options_headless.js` — headless mode, options, window size  
- `04_block_resources_cdp.js` — CDP commands to block images/fonts  
- `05_navigation_and_locators.js` — get, click, locators  
- `06_shadow_dom.js` — access shadow DOM via JS execution  
- `07_data_extraction.js` — text, attributes extraction  
- `08_tables_and_export.js` — build CSV/JSON from scraped data  
- `09_waits_and_retry.js` — implicit/explicit waits and retry  
- `10_downloads_and_monitoring.js` — download handling  
- `11_proxy_and_stealth.js` — proxies, stealth patterns


## Disclaimer

These examples are for **educational purposes** only. Learn more about [the legality of web scraping](https://hasdata.com/blog/is-web-scraping-legal).


## Notes

* Use context managers in Python to avoid leftover browser processes.
* CDP features work best with Chrome/Chromium.
* For large-scale scraping, consider Selenium Grid or Scrapy integration.
* All code is ready-to-run: adapt snippets to your own scraping tasks.

## 📎 More Resources

* Full tutorial: [The Complete Guide to Web Scraping with Selenium in Python](https://hasdata.com/blog/web-scraping-using-selenium-python)
* [Join the community on Discord](https://discord.com/invite/QeuPtWpkAt)

* [Star this repo if helpful ⭐](#)
