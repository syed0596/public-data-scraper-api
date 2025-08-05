import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from trafilatura import extract


class PublicScraper:
        """
        Scrapes Google Search Engine Results Pages (SERP) and website content.
        """

        def __init__(self, driver):
            self.driver = driver

        def scrape_google_serp(self, query: str, num_results: int = 10):
            """Scrapes the top search results for a given query."""
            print(f"Scraping Google for query: '{query}'")
            search_url = f"https://www.google.com/search?q={query}&num={num_results}"
            self.driver.get(search_url)

            # Handle cookie consent pop-up if it appears
            try:
                consent_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[.//div[contains(text(), 'Accept all')]]")
                    )
                )
                consent_button.click()
                print("Accepted cookie consent.")
            except TimeoutException:
                print("No cookie consent pop-up found.")

            results = []
            try:
                # Wait for search result containers to be present
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
                )
                search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g")

                for result in search_results[:num_results]:
                    try:
                        link_element = result.find_element(By.CSS_SELECTOR, "a")
                        url = link_element.get_attribute("href")

                        title_element = result.find_element(By.CSS_SELECTOR, "h3")
                        title = title_element.text

                        if url and title:
                            results.append({"title": title, "url": url})
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"An error occurred while scraping SERP: {e}")

            return results

        def scrape_website_content(self, url: str):
            """Scrapes the main text content from a given URL."""
            print(f"Scraping content from URL: {url}")
            try:
                self.driver.get(url)
                # Give the page a moment to render JavaScript
                time.sleep(2)
                page_html = self.driver.page_source
                # Use Trafilatura for robust content extraction
                clean_text = extract(
                    page_html, include_comments=False, include_tables=False
                )
                return clean_text or ""
            except Exception as e:
                print(f"Could not scrape content from {url}. Error: {e}")
                return ""
