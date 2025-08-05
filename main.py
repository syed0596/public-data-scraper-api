import os
import zipfile
from typing import List

import undetected_chromedriver as uc
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException
from pydantic import BaseModel

# Import your new scraper
from scraper.public_scraper import PublicScraper

# --- API Setup ---
app = FastAPI(
    title="Public Data Scraper API",
    description="An API to scrape Google Search results and website content using residential proxies.",
    version="1.0.0",
)


# --- Pydantic Models ---
class ScrapeRequest(BaseModel):
    query: str
    num_results: int = 5


# --- Environment Variables ---
SECRET_API_KEY = os.environ.get("SECRET_API_KEY", "dev-key")
PROXY_HOST = os.environ.get("PROXY_HOST")
PROXY_PORT = os.environ.get("PROXY_PORT")
PROXY_USER = os.environ.get("PROXY_USER")
PROXY_PASS = os.environ.get("PROXY_PASS")


# --- Scraping Logic ---
def run_scrape_task(query: str, num_results: int):
    """
    Initializes the scraper and runs the full process:
    1. Scrapes Google Search results.
    2. Scrapes the content of each resulting URL.
    """
    print("Scrape task started...")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if PROXY_HOST and PROXY_PORT and PROXY_USER and PROXY_PASS:
        proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
        options.add_argument(f"--proxy-server={proxy_url}")
        print(f"Configured to use proxy: {PROXY_HOST}")

    driver = None
    try:
        driver = uc.Chrome(options=options, headless=True, use_subprocess=False)
        scraper = PublicScraper(driver)

        # 1. Scrape Google SERP
        serp_results = scraper.scrape_google_serp(query, num_results)

        # 2. For each result, scrape the content of the page
        scraped_data = []
        for result in serp_results:
            content = scraper.scrape_website_content(result["url"])
            scraped_data.append(
                {
                    "title": result["title"],
                    "url": result["url"],
                    "content": content[:2000],  # Limit content length for API response
                }
            )

        return scraped_data

    except Exception as e:
        print(f"An error occurred during the scrape task: {e}")
        raise  # Re-raise the exception to be caught by the endpoint
    finally:
        if driver:
            driver.quit()
        print("Scrape task finished.")


# --- API Endpoint ---
@app.post("/scrape-public")
async def start_scraping(request: ScrapeRequest, x_api_key: str = Header(None)):
    """
    Accepts a search query and scrapes Google and the resulting websites.
    """
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        results = run_scrape_task(request.query, request.num_results)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An internal error occurred: {str(e)}"
        )


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Public Scraper API."}
