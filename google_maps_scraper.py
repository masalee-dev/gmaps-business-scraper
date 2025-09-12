import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import re

class GoogleMapsBusinessesScraper:
    def __init__(self, headless=True):
        """Intialize the scraper with Chrome WebDriver"""
        self.driver = self._setup_driver(headless)
        self.businesses = []

    def _setup_driver(self, headless):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationsControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def search_businesses(self, query, location, max_results=50):
        """
        Search for businesses on Google Maps
        
        Args: 
            query (str): Business type (e.g., "restaurants", "retail stores)
            location (str): Location to search in (e.g., "New York, NY")
            max_results (int): Maximum number of business results to scrape
        """
        search_url = f"https://www.google.com/maps/search/{query}+in+{location}/"
        self.driver.get(search_url)

        # Wait for the results to load
        time.sleep(3)

        # Scroll and load more results
        self._scroll_results_panel(max_results)

        # Extract business links
        business_links = self._get_business_links()

        print(f"Found {len(business_links)} business links")

        # Extract data from each business
        for i, link in enumerate(business_links[:max_results]):
            if i > 0 and i % 10 == 0:
                print(f"Processed {i} businesses...")
                time.sleep(2) # Rate limiting

            business_data = self._extract_business_data(link)
            if business_data:
                self.businesses.append(business_data)

    def _scroll_results_panel(self, target_count):
        """Scrool the results panel to load more businesses"""
        results_panel = self.driver.find_element(By.CSS_SELECTOR, "[role='main']")

        last_height = 0
        scroll_attempts = 0
        max_scrolls = 20

        while scroll_attempts < max_scrolls:
            # Scroll down in the results panel
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                results_panel
            )

            time.sleep(2)

            # Check if new content loaded
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight",
                results_panel
            )

            if new_height == last_height:
                break

            last_height = new_height
            scroll_attempts += 1

            # Check if we have enaough results
            current_results = len(self.driver.find_elements(By.CSS_SELECTOR, "[data-results-index]"))
            if current_results >= target_count:
                break

    def _get_business_links(self):
        """Extract links to individual business pages"""
        business_elements = self.driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
        return [elem.get_attribute('href') for elem in business_elements if elem.get_attribute('href')]
    
    def _extract_business_data(self, url):
        """Extract data from a single business page"""
        try:
            self.driver.get(url)
            time.sleep(2)

            business_data = {
                'name': '',
                'address': '',
                'phone': '',
                'website': '',
                'rating': '',
                'reviews_count': '',
                'category': '',
                'hours': '',
                'owner_name': '', # This is typically not available on Google Maps
                'url': url
            }

            # Business name
            try:
                name_elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                )
                business_data['name'] = name_elem.text
            except:
                pass

            # Address
            try:
                address_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']")
                business_data['address'] = address_elem.text
            except:
                pass

            # Phone number
            try:
                phone_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id^='phone']")
                business_data['phone'] = phone_elem.text
            except:
                pass

            # Website
            try:
                website_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
                business_data['website'] = website_elem.text
            except:
                pass

            # Rating and review count
            try:
                rating_elem = self.driver.find_element(By.CSS_SELECTOR, "[jsaction*='pane.rating']")
                rating_text = rating_elem.text
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    business_data['rating'] = rating_match.group(1)
                
                review_match = re.search(r'\(([0-9,]+)\)', rating_text)
                if review_match:
                    business_data['reviews_count'] = review_match.group(1)
            except:
                pass

            # Category
            try:
                category_elem = self.driver.find_element(By.CSS_SELECTOR, "[jsaction*='pane.rating'] + div button")
                business_data['category'] = category_elem.text
            except:
                pass

            return business_data
        
        except Exception as e:
            print(f"Error extraction data from {url}: {e}")
            return None
        
    def save_to_csv(self, filename="google_maps_businesses.csv"):
        """Save scraped data to a CSV file"""
        if not self.businesses:
            print("No business data to save")
            return
        
        df = pd.DataFrame(self.businesses)
        df.to_csv(filename, index=False)
        print(f"Saved {len(self.businesses)} businesses to {filename}")

    def save_to_google_sheets(self, sheet_id, credentials_file):
        """
        Save data to Google Sheets using Google Sheets API
        Requires: pip install gspread oauth2client
        """
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials

            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            client = gspread.authorize(creds)

            sheet = client.open_by_key(sheet_id).sheet1

            if self.businesses:
                df = pd.DataFrame(self.businesses)

                # Clear existing data
                sheet.clear()

                # Add headers
                headers = df.columns.tolist()
                sheet.append_row(headers)

                # Add data rows
                for _, row in df.iterrows():
                    sheet.append_row(row.tolist())

                print(f"Successfully uploaded {len(self.businesses)} businesses to Google Sheets")

        except ImportError:
            print("Please install required packages: pip install gspread oauth2client")
        except Exception as e:
            print(f"Error uploading to Google Sheets: {e}")

    def close(self):
        """Close the WebDriver"""
        self.driver.quit()

# Example usage
def main():
    scraper = GoogleMapsBusinessesScraper(headless=True)

    try:
        # Search for retail businesses
        scraper.search_businesses(
            query="cafe",
            location="New York, NY",
            max_results=50
        )

        # Save results
        scraper.save_to_csv("cafe_businesses_ny.csv")

        # Optionally save to Google Sheets (requires setup)
        # scraper.save_to_google_sheets("your_sheet_id", "credentials.json")

        print("Scraping completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scraper.close()

if __name__ == "__main__":
    main() 