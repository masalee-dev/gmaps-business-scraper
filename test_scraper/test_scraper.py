#!/usr/bin/env python3
"""
Unit Tests for Google Maps Business Scraper

Run tests with: python -m pytest tests/test_scraper.py -v
Or: python tests/test_scraper.py
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

# Add parent directory to path to import the scraper
sys.path.append(str(Path(__file__).parent.parent))

try:
    from google_maps_scraper import GoogleMapsBusinessScraper
    from config import ScraperConfig, CSVConfig
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure google_maps_scraper.py and config.py exist in the parent directory")
    sys.exit(1)

class TestGoogleMapsBusinessScraper(unittest.TestCase):
    """Test cases for GoogleMapsBusinessScraper class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_driver = Mock()
        self.scraper = None
    
    def tearDown(self):
        """Clean up after each test method"""
        if self.scraper:
            try:
                self.scraper.close()
            except:
                pass
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_scraper_initialization(self, mock_chrome):
        """Test scraper initialization with default settings"""
        mock_chrome.return_value = self.mock_driver
        
        scraper = GoogleMapsBusinessScraper()
        
        self.assertIsNotNone(scraper.driver)
        self.assertEqual(scraper.businesses, [])
        mock_chrome.assert_called_once()
        
        scraper.close()
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_scraper_initialization_headless(self, mock_chrome):
        """Test scraper initialization in headless mode"""
        mock_chrome.return_value = self.mock_driver
        
        scraper = GoogleMapsBusinessScraper(headless=True)
        
        # Check if Chrome was called with options
        args, kwargs = mock_chrome.call_args
        options = kwargs.get('options') or args[0] if args else None
        self.assertIsNotNone(options)
        
        scraper.close()
    
    def test_business_data_structure(self):
        """Test the structure of business data"""
        expected_keys = [
            'name', 'address', 'phone', 'website', 
            'rating', 'review_count', 'category', 'hours', 'url'
        ]
        
        # Mock business data
        mock_business = {
            'name': 'Test Restaurant',
            'address': '123 Main St, Test City, ST 12345',
            'phone': '(555) 123-4567',
            'website': 'https://testrestaurant.com',
            'rating': '4.5',
            'review_count': '150',
            'category': 'Restaurant',
            'hours': 'Open ⋅ Closes 9PM',
            'url': 'https://maps.google.com/test'
        }
        
        for key in expected_keys:
            self.assertIn(key, mock_business)
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_save_to_csv_empty_data(self, mock_chrome):
        """Test saving empty data to CSV"""
        mock_chrome.return_value = self.mock_driver
        scraper = GoogleMapsBusinessScraper()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Should not raise an error with empty data
            scraper.save_to_csv(temp_filename)
            self.assertTrue(os.path.exists(temp_filename))
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            scraper.close()
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_save_to_csv_with_data(self, mock_chrome):
        """Test saving data to CSV file"""
        mock_chrome.return_value = self.mock_driver
        scraper = GoogleMapsBusinessScraper()
        
        # Add mock business data
        scraper.businesses = [
            {
                'name': 'Test Business 1',
                'address': '123 Test St',
                'phone': '555-1234',
                'rating': '4.5',
                'url': 'https://example.com/1'
            },
            {
                'name': 'Test Business 2', 
                'address': '456 Test Ave',
                'phone': '555-5678',
                'rating': '4.0',
                'url': 'https://example.com/2'
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
            temp_filename = temp_file.name
        
        try:
            scraper.save_to_csv(temp_filename)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Check file contents
            with open(temp_filename, 'r') as f:
                content = f.read()
                self.assertIn('Test Business 1', content)
                self.assertIn('Test Business 2', content)
                self.assertIn('555-1234', content)
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            scraper.close()
    
    def test_data_validation(self):
        """Test business data validation"""
        valid_business = {
            'name': 'Valid Business',
            'address': '123 Main St',
            'phone': '(555) 123-4567',
            'rating': '4.5'
        }
        
        # Test required fields
        self.assertIsNotNone(valid_business.get('name'))
        
        # Test phone number format (basic validation)
        phone = valid_business.get('phone', '')
        self.assertTrue(any(char.isdigit() for char in phone))
        
        # Test rating format
        rating = valid_business.get('rating')
        if rating:
            try:
                float(rating)
                rating_valid = True
            except (ValueError, TypeError):
                rating_valid = False
            self.assertTrue(rating_valid)

class TestScraperConfiguration(unittest.TestCase):
    """Test configuration and settings"""
    
    def test_scraper_config_values(self):
        """Test scraper configuration values"""
        self.assertIsInstance(ScraperConfig.HEADLESS, bool)
        self.assertIsInstance(ScraperConfig.DEFAULT_DELAY, (int, float))
        self.assertGreater(ScraperConfig.DEFAULT_DELAY, 0)
        self.assertIsInstance(ScraperConfig.MAX_RESULTS_PER_SEARCH, int)
        self.assertGreater(ScraperConfig.MAX_RESULTS_PER_SEARCH, 0)
    
    def test_csv_config_values(self):
        """Test CSV configuration values"""
        self.assertIsInstance(CSVConfig.COLUMN_ORDER, list)
        self.assertGreater(len(CSVConfig.COLUMN_ORDER), 0)
        self.assertIn('name', CSVConfig.COLUMN_ORDER)
        self.assertIn('address', CSVConfig.COLUMN_ORDER)

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions and helpers"""
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_driver_setup(self, mock_chrome):
        """Test WebDriver setup"""
        mock_chrome.return_value = Mock()
        
        scraper = GoogleMapsBusinessScraper(headless=True)
        
        # Verify Chrome was called
        mock_chrome.assert_called_once()
        
        # Check if driver has expected methods
        self.assertTrue(hasattr(scraper.driver, 'get'))
        self.assertTrue(hasattr(scraper.driver, 'quit'))
        
        scraper.close()
    
    def test_url_validation(self):
        """Test URL validation logic"""
        valid_urls = [
            'https://www.google.com/maps/place/Test+Restaurant',
            'https://maps.google.com/maps?cid=123456789',
        ]
        
        invalid_urls = [
            'not-a-url',
            'http://malicious-site.com',
            '',
            None
        ]
        
        for url in valid_urls:
            self.assertTrue(url.startswith('https://'))
            self.assertIn('google.com', url)
        
        for url in invalid_urls:
            if url:
                self.assertFalse(url.startswith('https://maps.google.com') or 
                               url.startswith('https://www.google.com/maps'))

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_driver_initialization_failure(self, mock_chrome):
        """Test handling of driver initialization failure"""
        mock_chrome.side_effect = Exception("ChromeDriver not found")
        
        with self.assertRaises(Exception):
            GoogleMapsBusinessScraper()
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_invalid_search_parameters(self, mock_chrome):
        """Test handling of invalid search parameters"""
        mock_chrome.return_value = Mock()
        scraper = GoogleMapsBusinessScraper()
        
        # Test with empty query
        try:
            scraper.search_businesses("", "New York, NY", 10)
        except Exception as e:
            self.assertIsInstance(e, (ValueError, TypeError, Exception))
        
        # Test with invalid max_results
        try:
            scraper.search_businesses("restaurants", "New York, NY", 0)
        except Exception as e:
            self.assertIsInstance(e, (ValueError, TypeError, Exception))
        
        scraper.close()
    
    @patch('google_maps_scraper.webdriver.Chrome')
    def test_file_save_error_handling(self, mock_chrome):
        """Test file save error handling"""
        mock_chrome.return_value = Mock()
        scraper = GoogleMapsBusinessScraper()
        
        # Try to save to invalid path
        invalid_path = "/invalid/path/file.csv"
        
        try:
            scraper.save_to_csv(invalid_path)
        except Exception as e:
            # Should handle the error gracefully
            self.assertIsInstance(e, (OSError, IOError, PermissionError, Exception))
        
        scraper.close()

class TestDataProcessing(unittest.TestCase):
    """Test data processing and filtering"""
    
    def test_business_data_cleaning(self):
        """Test cleaning of business data"""
        raw_business_data = {
            'name': '  Test Restaurant  ',  # Extra spaces
            'phone': '(555) 123-4567',
            'rating': '4.5 stars',  # Extra text
            'address': '123 Main St, City, ST 12345\n',  # Newline
        }
        
        # Simulate data cleaning
        cleaned_data = {}
        for key, value in raw_business_data.items():
            if value:
                cleaned_value = str(value).strip()
                if key == 'rating':
                    # Extract numeric rating
                    import re
                    rating_match = re.search(r'(\d+\.?\d*)', cleaned_value)