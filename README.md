# Google Maps Businees Data Scraper
This is Dummy project I get from proposal on Upwork!

A Python tool for extracting business information from Google Maps search results. This scraper collects business details like names, addresses, phone numbers, and more, then exports the data to CSV or Google Sheets.

## ⚠ Important Legal Notice
This tool is for educational and research purposes. Please ensure you comply with:
- Google's Terms of Service
- Local data protection laws (GDPR, CCPA, etc.)
- Robots.txt guidlines
- Rate limiting best practices
Consider using Google's official [Places API](https://developers.google.com/maps/documentation/places/web-service) for commercial applications.

## Features
- Search business by type and location
- Extract comprehensive business data
- Export to CSV format
- Upload directly to Google Sheets
- Configurable rate limiting
- Headless or visible browser modes

## Data Extracted
- Business name
- Address
- Phone number
- Website
- Rating and review count
- Business category
- Google Maps URL

## Installation

### Prerequisites
- Python 3.7+
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

### Install Dependencies
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install selenium pandas webdriver-manager gspread oauth2client
```

## Quick Start

### Basic Usage
```python
from google_maps_scraper import GoogleMapsBusinessScraper

# Initialize scraper
scraper = GoogleMapsBusinessScraper(headless=True)

try:
    # Search for businesses
    scraper.search_businesses(
        query="restaurants",
        location="San Francisco, CA",
        max_results=50
    )

    # Save to csv
    scraper.save_to_csv("restaurant_sf.csv")

finally:
    scraper.close()
```

### Command Line Usage
```bash
pyhton main.py --query "retail stores" --location "New York, NY" --max-results 100 --output "retail_ny.csv"
```

## Configuration

### Google Sheets Integration
1. Create a Google Cloud project
2. Enable the Google Sheets API
3. Create service account credentials
4. Download the JSON credentials file
5. Share your Google Sheet with the service account email
```python
scrape.save_to_google_sheets(
    sheet_id="your_google_sheet_id",
    credentials_file="path/to/credentials.json"
)
```

### Rate Limiting
The scraper includes built-in rate limiting to prevent IP blocking:
- 2-seconds delays between page loads
- 10-business batches with longer pauses
- Configuration scroll delays

## Examples

### Search Multiple Business Types
```python
business_types = ["restaurant", "retail stores", "coffee shops"]
locations = ["New York, NY", "Los Angeles, CA"]

for business_type in business_types:
    for location in locations:
        scraper.search_businesses(business_type, location, 25)
        scraper.save_to_csv(f"{business_type}_{locations.replace(', ', '_' )}.csv")
```

### Filter Results
```python
# Filter businesses with ratings above 4.0
high_rated = [b for b in scraper.businesses if b.get('rating') and float(b['rating']) > 4.0]
```

## Command Line Interface
```bash
python main.py [OPTIONS]

Options:
    --query TEXT            Business type to search for [required]
    --location TEXT         Location to search in [required]
    --max-results INTEGER   Maximum number of results [default: 50]
    --output TEXT           Output CSV filename [default: businesses.csv]
    --headless              Run in headless mode [default: True]
    --sheets-id TEXT        Google Sheets ID for upload
    --credentials TEXT      Path to Google credentials JSON file
```

## Project Structure
google-maps-scraper/
├── google_maps_scraper.py    # Main scraper class
├── main.py                   # CLI interface
├── requirements.txt          # Dependencies
├── config.py                # Configuration settings
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   └── batch_scraping.py
├── tests/                   # Unit tests
│   └── test_scraper.py
├── .gitignore               # Git ignore rules
└── README.md               # This file

## Error Handling
The scraper includes robust error handling for:
- Network timeouts
- Element not found errors
- Rate limiting responses
- Invalid search queries

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin/feature/amazing-feature`)
5. Open a Pull Request

## Best Practices
- Use reasonable delays between requests
- Implement proper error handling
- Respect rate limits
- Monitor for IP blocking
- Use proxy rotation for large-scale scraping

## Limitations
- Owner names are typically not available information
- Some businesses may have incomplete information
- Rate limits may affect scraping speed
- Google may update their page structure, requiring code updates

## Troubleshooting

### Common Issues
#### ChromeDriver not found:
```bash
pip install webdriver-manager
```

#### Element not found errors:
- Google may have updated their page structure
- Try increasing wait times
- Chechk if you're being rate limited

#### Google Sheets upload fails:
- Verify credentials file path
- Check if the sheet is shared with service account
- Ensure Google Sheets API is enabled

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/masalee-dev/gmaps-business-scraper/blob/main/LICENSE) file for details.

## Disclaimer
This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and TOS. The authors are not responsible for any misuse of this tool.

## Support
If you encounter issues or have questions:
1. Review the troubleshooting section
2. Create a new issue with detailed information

## Roadmap
 Add proxy support
 Implement async scraping
 Add more export formats (JSON, Excel)
 Create web interface
 Add data validation and cleaning
 Implement caching mechanism
