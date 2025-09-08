#!/usr/bin/env python3
"""
Basic Usage Example - Google Maps Business Scraper

This example demonstrates basic usage of the Google Maps business scraper
with simple, straightforward examples for getting started.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the scraper
sys.path.append(str(Path(__file__).parent.parent))

from google_maps_scraper import GoogleMapsBusinessScraper

def simple_restaurant_search():
    """
    Simple example: Search for restaurants in a city
    """
    print("🍽️ Simple Restaurant Search Example")
    print("-" * 40)
    
    # Initialize the scraper
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        # Search for restaurants
        scraper.search_businesses(
            query="restaurants",
            location="San Francisco, CA", 
            max_results=10
        )
        
        # Print results
        print(f"Found {len(scraper.businesses)} restaurants:")
        for i, business in enumerate(scraper.businesses[:5], 1):  # Show first 5
            print(f"{i}. {business.get('name', 'N/A')}")
            print(f"   Address: {business.get('address', 'N/A')}")
            print(f"   Phone: {business.get('phone', 'N/A')}")
            print(f"   Rating: {business.get('rating', 'N/A')}")
            print()
        
        # Save to CSV
        scraper.save_to_csv("restaurants_sf.csv")
        print("💾 Results saved to 'restaurants_sf.csv'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def coffee_shop_search():
    """
    Example: Search for coffee shops with visible browser
    """
    print("☕ Coffee Shop Search Example (Visible Browser)")
    print("-" * 50)
    
    # Initialize with visible browser (headless=False)
    scraper = GoogleMapsBusinessScraper(headless=False)
    
    try:
        # Search for coffee shops
        scraper.search_businesses(
            query="coffee shops",
            location="Portland, OR",
            max_results=15
        )
        
        # Display summary
        print(f"\n📊 Search Results Summary:")
        print(f"Total coffee shops found: {len(scraper.businesses)}")
        
        # Show businesses with ratings
        rated_businesses = [b for b in scraper.businesses if b.get('rating')]
        if rated_businesses:
            print(f"Businesses with ratings: {len(rated_businesses)}")
            avg_rating = sum(float(b['rating']) for b in rated_businesses if b['rating']) / len(rated_businesses)
            print(f"Average rating: {avg_rating:.1f}")
        
        # Save results
        scraper.save_to_csv("coffee_portland.csv")
        print("💾 Results saved to 'coffee_portland.csv'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def retail_store_search():
    """
    Example: Search for retail stores and filter results
    """
    print("🛍️ Retail Store Search with Filtering")
    print("-" * 40)
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        # Search for retail stores
        scraper.search_businesses(
            query="retail stores",
            location="New York, NY",
            max_results=20
        )
        
        print(f"Found {len(scraper.businesses)} retail stores")
        
        # Filter businesses that have websites
        stores_with_websites = []
        stores_with_phones = []
        
        for business in scraper.businesses:
            if business.get('website'):
                stores_with_websites.append(business)
            if business.get('phone'):
                stores_with_phones.append(business)
        
        print(f"Stores with websites: {len(stores_with_websites)}")
        print(f"Stores with phone numbers: {len(stores_with_phones)}")
        
        # Save filtered results
        if stores_with_websites:
            scraper.businesses = stores_with_websites
            scraper.save_to_csv("retail_with_websites.csv")
            print("💾 Stores with websites saved to 'retail_with_websites.csv'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def google_sheets_example():
    """
    Example: Save results to Google Sheets (requires credentials)
    """
    print("📊 Google Sheets Integration Example")
    print("-" * 40)
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        # Search for businesses
        scraper.search_businesses(
            query="bakeries",
            location="Boston, MA",
            max_results=10
        )
        
        print(f"Found {len(scraper.businesses)} bakeries")
        
        # Save to CSV first
        scraper.save_to_csv("bakeries_boston.csv")
        print("💾 Results saved to CSV")
        
        # Try to save to Google Sheets (requires credentials file)
        credentials_file = "credentials/google_sheets_credentials.json"
        
        if Path(credentials_file).exists():
            try:
                # Replace with your actual Google Sheets ID
                sheet_id = "your_google_sheet_id_here"
                scraper.save_to_google_sheets(sheet_id, credentials_file)
                print("📊 Results uploaded to Google Sheets")
            except Exception as sheets_error:
                print(f"⚠️ Google Sheets upload failed: {sheets_error}")
                print("💡 Make sure you have valid credentials and sheet ID")
        else:
            print("⚠️ Google Sheets credentials not found")
            print(f"💡 Create credentials file at: {credentials_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def search_multiple_locations():
    """
    Example: Search the same business type in multiple locations
    """
    print("🌍 Multi-Location Search Example")
    print("-" * 35)
    
    locations = [
        "Seattle, WA",
        "Portland, OR", 
        "San Francisco, CA"
    ]
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    all_results = []
    
    try:
        for location in locations:
            print(f"\n🔍 Searching in {location}...")
            
            # Clear previous results
            scraper.businesses = []
            
            # Search for pizza places
            scraper.search_businesses(
                query="pizza",
                location=location,
                max_results=8
            )
            
            # Add location info to each business
            for business in scraper.businesses:
                business['search_location'] = location
                all_results.append(business)
            
            print(f"   Found {len(scraper.businesses)} pizza places")
        
        # Save combined results
        scraper.businesses = all_results
        scraper.save_to_csv("pizza_multi_location.csv")
        
        print(f"\n📊 Total Results: {len(all_results)} pizza places")
        print("💾 Combined results saved to 'pizza_multi_location.csv'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def main():
    """
    Run all basic examples
    """
    print("Google Maps Scraper - Basic Usage Examples")
    print("=" * 45)
    
    # Create output directory
    output_dir = Path("basic_examples_output")
    output_dir.mkdir(exist_ok=True)
    
    # Change to output directory
    import os
    os.chdir(output_dir)
    
    examples = [
        ("Simple Restaurant Search", simple_restaurant_search),
        ("Coffee Shop Search", coffee_shop_search),
        ("Retail Store Search", retail_store_search),
        ("Multi-Location Search", search_multiple_locations),
        ("Google Sheets Example", google_sheets_example)
    ]
    
    for name, example_func in examples:
        print(f"\n{'='*50}")
        print(f"Running: {name}")
        print(f"{'='*50}")
        
        try:
            example_func()
        except KeyboardInterrupt:
            print("⚠️ Example interrupted by user")
            break
        except Exception as e:
            print(f"❌ Example failed: {e}")
        
        print(f"✅ {name} completed")
    
    print(f"\n🏁 All basic examples completed!")
    print(f"📁 Check the '{output_dir}' directory for generated files")

if __name__ == '__main__':
    main()