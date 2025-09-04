"""
Configuration settings for Google Maps Business Scraper.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
CREDENTIALS_DIR = BASE_DIR / "credentials"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, CREDENTIALS_DIR]:
    directory.mkdir(exist_ok=True)

# Scraper Settings
class ScraperConfig:
    # Browser settings
    HEADLESS = True
    BROWSER_TIMEOUT = 30  # seconds
    PAGE_LOAD_TIMEOUT = 20  # seconds
    IMPLICIT_WAIT = 10  # seconds

    # Rate limiting
    DEFAULT_DELAY = 2  # seconds between requests
    BATCH_DELAY = 5  # seconds between batches
    SCROLL_DELAY = 2  # seconds between scrolls

    # Scraping limits
    MAX_RESULTS_PER_SEARCH = 200
    MAX_SCROLL_ATTEMPTS = 20
    RETRY_ATTEMPTS = 3

    # Chrome options
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    ]

# Google SheetsC settings
class SheetsConfig:
    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    # Default credentials file name
    DEFAULT_CREDENTIALS_FILE = CREDENTIALS_DIR / "google_sheets_credentials.json"

# CSV Export settings
class CSVConfig:
    DEFAULT_OUTPUT_DIR = DATA_DIR
    DEFAULT_FILENAME = "google_mapas_businesses.csv"

    # Columns order for CSV output
    COLUMN_ORDER = [
        'name',
        'address',
        'phone',
        'website',
        'rating',
        'review_count',
        'category',
        'hours',
        'url'
    ]

# Logging settings
class LogConfig:
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / "scraper.log"
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5

# CSS selectors (update these if google maps changes structure)
class Selectors:
    SEARCH_BOX = "input[aria-label*='Search']"
    RESULTS_PANEL = "[role='main']"
    BUSINESS_LINKS = "[data-results-index] a"

    # Business detetails selectors
    BUSINESS_NAME = "h1"
    ADDRESS = "[data-item-id='address']"
    PHONE = "[data-item-id^='phone']"
    WEBSITE = "[data-item-id='authority']"
    RATING = "[jsaction*='pane.rating']"
    CATEGORY = "[jsaction*='pane.rating'] + div button"
    HOURS = "[data-item-id='oh']"

    # Navigation selectors
    BACK_BUTTON = "[aria-label='Back']"
    CLOSE_BUTTIN = "[aria-label='Close']"

# Environment variables
class EnvConfig:
    @staticmethod
    def get_google_sheets_credentials():
        """Get Google Sheets credentials file path from environment."""
        return os.getenv('GOOGLE_SHEETS_CREDENTIALS', SheetsConfig.DEFAULT_CREDENTIALS_FILE)
    
    @staticmethod
    def get_output_dir():
        """Get output directory from environment."""
        return Path(os.getenv('OUTPUT_DIR', CSVConfig.DEFAULT_OUTPUT_DIR))
    
    @staticmethod
    def get_handless_mode():
        """Get headless mode setting from environment."""
        return os.getenv('HEADLESS', 'True').lower() == 'true'
    
    @staticmethod
    def get_delay():
        """Get delay setting from environment."""
        return int(os.getenv('SCRAPER_DELAY', ScraperConfig.DEFAULT_DELAY))
    
# Search templates for common business types
SEARCH_TEMPLATES = {
    'restaurants': {
        'query': 'restaurants',
        'expected_fields': ['name', 'address', 'phone', 'rating', 'category']
    },
    'retail': {
        'query': 'retail stores',
        'expected_fields': ['name', 'address', 'phone', 'website']
    },
    'services': {
        'query': 'services',
        'expected_fields': ['name', 'address', 'phone', 'website', 'rating']
    },
    'healtcare': {
        'query': 'doctors',
        'expected_fields': ['name', 'address', 'phone', 'hours']
    }
}

# Error messages
ERROR_MESSAGES = {
    'no_results': "No search results found. Try different keywords or location.",
    'timeout': "Request timed out. Consider increasing the delay or checking your internet connection.",
    'blocked': "Access blocked by Google. Try using a VPN or changing your IP address.",
    'invalid_location': "The specified location is invalid or not recognized.",
    'scaping_failed': "Scraping failed due to an unexpected error.",
    'export_failed': "Failed to export data to CSV or Google Sheets.",
    'sheets_failed': "Failed to upload data to Google Sheets."
}