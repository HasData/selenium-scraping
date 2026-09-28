# Scroll Method Benchmark — quotes.toscrape.com/scroll

**Test:** 10 scroll steps · 1.5s pause · selector `div.quote`
**URL:** https://quotes.toscrape.com/scroll

## Results

| Method | Items loaded | Triggers (out of 10) | Time |
|---|---:|---:|---:|
| window.scrollTo(scrollHeight) | +90 (10→100) | 9/10 | 26.3s |
| window.scrollBy(0, 800) | +40 (10→50) | 4/10 | 42.5s |
| scrollIntoView (last element) | +90 (10→100) | 9/10 | 27.5s |
| ActionChains scroll_by_amount | +40 (10→50) | 4/10 | 43.6s |
| Keyboard END | +90 (10→100) | 9/10 | 27.0s |

## Raw series (items after each step)

**window.scrollTo(scrollHeight):** `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100]`
**window.scrollBy(0, 800):** `[10, 10, 20, 20, 20, 30, 30, 40, 40, 50, 50]`
**scrollIntoView (last element):** `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100]`
**ActionChains scroll_by_amount:** `[10, 10, 20, 20, 20, 30, 30, 40, 40, 50, 50]`
**Keyboard END:** `[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100]`