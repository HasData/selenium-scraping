import asyncio
import aiohttp
import requests

api_key = "YOUR_API_KEY"

# Get available concurrency for your HasData API key
# Get API key here: https://app.hasdata.com/sign-up
def get_available_concurrency():
    url = "https://api.hasdata.com/user/me/usage"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # return available concurrency, fallback to 1
        return data.get("data", {}).get("availableConcurrency", 1)
    return 1

# Build payload for scraping a single URL
def make_payload(url):
    return {
        "url": url,
        "proxyType": "datacenter",
        "proxyCountry": "US",
        "js_rendering": True,
        "aiExtractRules": {
            "companyName": {"description": "Company name", "type": "string"},
            "email": {"description": "Email addresses", "type": "string"}
        }
    }

# Async function to scrape one site
async def scrape_site(session, url):
    payload = make_payload(url)
    async with session.post(
        "https://api.hasdata.com/scrape/web",
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json"
        },
        json=payload
    ) as response:
        if response.status == 200:
            data = await response.json()
            ai_resp = data.get("aiResponse", {})

            company = ai_resp.get("companyName", "-")
            emails = ai_resp.get("email", "")

            return {
                "url": url,
                "company": company,
                "emails": emails
            }
        else:
            return {"url": url, "error": response.status}

# Async scrape for multiple sites
async def scrape_all(urls):
    concurrency = get_available_concurrency()
    # limit concurrent connections to API's availableConcurrency
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [scrape_site(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

# Run scraper
if __name__ == "__main__":
    urls_to_scrape = [
        "https://example.com",
        "https://hasdata.com",
        # add more URLs
    ]
    all_results = asyncio.run(scrape_all(urls_to_scrape))
    for r in all_results:
        print(r)
