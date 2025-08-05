import time
import urllib.parse

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from trafilatura import extract


class PublicScraper:
    """
    Scrapes Search Engine Results Pages (SERP) from the main DuckDuckGo website.
    """

    def __init__(self, driver):
        self.driver = driver

    def scrape_serp(self, query: str, num_results: int = 10):
        """Scrapes the top search results for a given query from DuckDuckGo."""
        print(f"Scraping main DuckDuckGo site for query: '{query}'")
        
        # --- CHANGE 1: Use the main DuckDuckGo URL ---
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://duckduckgo.com/?q={encoded_query}"
        self.driver.get(search_url)

        results = []
        try:
            # --- CHANGE 2: Use the selectors for the main JS site ---
            # Wait for the main results container with id="links"
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "links"))
            )
            
            # Find all the individual result articles
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='result']")

            for result in search_results[:num_results]:
                try:
                    # The title and URL are within the same <a> tag inside an <h2>
                    link_element = result.find_element(By.CSS_SELECTOR, "h2 > a")
                    url = link_element.get_attribute("href")
                    title = link_element.text

                    if url and title:
                        results.append({"title": title, "url": url})
                except NoSuchElementException:
                    continue
        except TimeoutException:
            print(f"ERROR: Timed out waiting for search results. The page title is: '{self.driver.title}'")
        except Exception as e:
            print(f"An unexpected error occurred while scraping SERP: {e}")

        return results

    def scrape_website_content(self, url: str):
        """Scrapes the main text content from a given URL."""
        print(f"Scraping content from URL: {url}")
        try:
            self.driver.get(url)
            time.sleep(2)
            page_html = self.driver.page_source
            clean_text = extract(
                page_html, include_comments=False, include_tables=False
            )
            return clean_text or ""
        except Exception as e:
            print(f"Could not scrape content from {url}. Error: {e}")
            return ""