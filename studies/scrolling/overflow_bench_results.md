# Overflow-container scroll benchmark (popup simulation)

Local page: 400px overflow-y div, 10-row batches appended ~300ms after the
scroll nears the bottom, 100 rows total. 20 steps max per loop.

| Technique | Rows loaded | Time |
|---|---:|---:|
| scrollTop = scrollHeight, single call (article's current snippet) | 20/100 | 1.5s |
| scrollTop += offsetHeight loop, fixed 1s sleep | 100/100 | 20.5s |
| scrollTop += offsetHeight loop, WebDriverWait on row count | 100/100 | 9.6s |

## Row-count series

**scrollTop = scrollHeight, single call (article's current snippet):** `[10, 20]`
**scrollTop += offsetHeight loop, fixed 1s sleep:** `[10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80, 80, 90, 90, 100, 100, 100, 100]`
**scrollTop += offsetHeight loop, WebDriverWait on row count:** `[10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80, 80, 90, 90, 100, 100, 100, 100]`