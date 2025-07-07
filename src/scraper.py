from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_leads(query="AI startup", location="San Francisco", pages=1):
    results = []
    base_url = "https://www.indeed.com/jobs"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 🔍 HEADLESS = False to see the browser
        page = browser.new_page()

        for page_num in range(pages):
            start = page_num * 10
            search_url = f"{base_url}?q={query}&l={location}&start={start}"
            print(f"[INFO] Scraping page {page_num+1}: {search_url}")
            page.goto(search_url, timeout=30000)
            page.wait_for_timeout(5000)  # wait for content to load

            # 💡 Debug: Save HTML to inspect structure
            with open(f"debug_page_{page_num+1}.html", "w", encoding="utf-8") as f:
                f.write(page.content())

            job_cards = page.locator("div.job_seen_beacon")
            count = job_cards.count()
            print(f"[DEBUG] Found {count} job cards on page {page_num+1}")

            for i in range(count):
                try:
                    title = job_cards.nth(i).locator("h2.jobTitle").inner_text()
                except:
                    title = "N/A"
                try:
                    company = job_cards.nth(i).locator("span.companyName").inner_text()
                except:
                    company = "N/A"
                try:
                    loc = job_cards.nth(i).locator("div.companyLocation").inner_text()
                except:
                    loc = "N/A"

                results.append({"title": title, "company": company, "location": loc})

        browser.close()

    if results:
        df = pd.DataFrame(results)
        df.to_csv("data/leads_raw.csv", index=False)
        print(f"[SUCCESS] Scraped {len(df)} leads → data/leads_raw.csv")
        return df
    else:
        print("[WARNING] No data found.")
        return pd.DataFrame()

if __name__ == "__main__":
    scrape_leads()
