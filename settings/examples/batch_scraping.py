#!/usr/bin/env python3
"""
Batch Scraping Example - Google Maps Business Scraper

This example demonstrates how to scrape multiple business types 
across different locations in batch mode.
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path to import the scraper
sys.path.append(str(Path(__file__).parent.parent))

from google_maps_scraper import GoogleMapsBusinessScraper

def example_batch_scraping():
    """
    Example: Scrape multiple business types across different cities
    """
    
    # Define search configurations
    search_configs = [
        {
            'query': 'coffee shops',
            'location': 'Seattle, WA',
            'max_results': 30,
            'output_file': 'coffee_seattle.csv'
        },
        {
            'query': 'pizza restaurants',
            'location': 'New York, NY',
            'max_results': 50,
            'output_file': 'pizza_nyc.csv'
        },
        {
            'query': 'retail stores',
            'location': 'Los Angeles, CA',
            'max_results': 40,
            'output_file': 'retail_la.csv'
        },
        {
            'query': 'hair salons',
            'location': 'Miami, FL',
            'max_results': 25,
            'output_file': 'salons_miami.csv'
        }
    ]
    
    # Initialize scraper
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        print("🚀 Starting batch scraping...")
        print(f"📊 Total searches: {len(search_configs)}")
        print("-" * 50)
        
        for i, config in enumerate(search_configs, 1):
            print(f"\n🔍 Search {i}/{len(search_configs)}")
            print(f"   Query: {config['query']}")
            print(f"   Location: {config['location']}")
            print(f"   Max results: {config['max_results']}")
            
            # Clear previous results
            scraper.businesses = []
            
            # Perform search
            scraper.search_businesses(
                query=config['query'],
                location=config['location'],
                max_results=config['max_results']
            )
            
            # Save results
            if scraper.businesses:
                scraper.save_to_csv(config['output_file'])
                print(f"   ✅ Saved {len(scraper.businesses)} businesses to {config['output_file']}")
            else:
                print(f"   ⚠️ No businesses found for this search")
            
            # Add delay between searches to be respectful
            if i < len(search_configs):
                print("   ⏳ Waiting 5 seconds before next search...")
                time.sleep(5)
        
        print("\n🎉 Batch scraping completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Batch scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during batch scraping: {e}")
    finally:
        scraper.close()

def example_targeted_scraping():
    """
    Example: Scrape specific business categories with filters
    """
    
    # Target high-rated restaurants in tech hubs
    tech_cities = [
        'San Francisco, CA',
        'Austin, TX', 
        'Seattle, WA',
        'Boston, MA'
    ]
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    all_businesses = []
    
    try:
        print("🎯 Starting targeted scraping for tech hub restaurants...")
        
        for city in tech_cities:
            print(f"\n🏙️ Scraping restaurants in {city}")
            
            # Clear previous results
            scraper.businesses = []
            
            # Search for restaurants
            scraper.search_businesses(
                query='restaurants',
                location=city,
                max_results=30
            )
            
            # Filter for high-rated businesses (4.0+ rating)
            high_rated = []
            for business in scraper.businesses:
                try:
                    rating = float(business.get('rating', 0))
                    if rating >= 4.0:
                        business['city'] = city  # Add city info
                        high_rated.append(business)
                except (ValueError, TypeError):
                    continue
            
            all_businesses.extend(high_rated)
            print(f"   Found {len(high_rated)} high-rated restaurants (4.0+)")
        
        # Save combined results
        if all_businesses:
            scraper.businesses = all_businesses
            scraper.save_to_csv('high_rated_tech_restaurants.csv')
            print(f"\n✅ Saved {len(all_businesses)} high-rated restaurants across tech hubs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

def example_business_analysis():
    """
    Example: Scrape and analyze business data
    """
    import pandas as pd
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        print("📊 Scraping for business analysis...")
        
        # Scrape coffee shops in a specific area
        scraper.search_businesses(
            query='coffee shops',
            location='Portland, OR',
            max_results=50
        )
        
        if scraper.businesses:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(scraper.businesses)
            
            # Basic analysis
            print(f"\n📈 Analysis Results:")
            print(f"   Total businesses: {len(df)}")
            
            # Rating analysis
            if 'rating' in df.columns:
                df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce')
                avg_rating = df['rating_num'].mean()
                print(f"   Average rating: {avg_rating:.2f}")
                
                # Count by rating ranges
                high_rated = len(df[df['rating_num'] >= 4.5])
                good_rated = len(df[(df['rating_num'] >= 4.0) & (df['rating_num'] < 4.5)])
                print(f"   Excellent (4.5+): {high_rated}")
                print(f"   Good (4.0-4.4): {good_rated}")
            
            # Save analysis
            scraper.save_to_csv('portland_coffee_analysis.csv')
            print(f"   💾 Data saved for further analysis")
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    finally:
        scraper.close()

def example_custom_search():
    """
    Example: Custom search with specific requirements
    """
    
    scraper = GoogleMapsBusinessScraper(headless=True)
    
    try:
        print("🔧 Custom search example...")
        
        # Search for businesses that are likely to have phone numbers
        business_types = ['plumbers', 'electricians', 'dentists', 'veterinarians']
        
        for business_type in business_types:
            print(f"\n🔍 Searching for {business_type}...")
            
            scraper.businesses = []  # Clear previous results
            
            scraper.search_businesses(
                query=business_type,
                location='Chicago, IL',
                max_results=20
            )
            
            # Filter businesses that have phone numbers
            businesses_with_phones = [
                business for business in scraper.businesses 
                if business.get('phone') and business.get('phone').strip()
            ]
            
            print(f"   Found {len(businesses_with_phones)} {business_type} with phone numbers")
            
            # Save if we found any
            if businesses_with_phones:
                scraper.businesses = businesses_with_phones
                filename = f'{business_type}_chicago_with_phones.csv'
                scraper.save_to_csv(filename)
                print(f"   💾 Saved to {filename}")
    
    except Exception as e:
        print(f"❌ Custom search error: {e}")
    finally:
        scraper.close()

if __name__ == '__main__':
    print("Google Maps Batch Scraping Examples")
    print("=" * 40)
    
    # Create examples directory if it doesn't exist
    Path('examples_output').mkdir(exist_ok=True)
    os.chdir('examples_output')
    
    try:
        # Run examples
        print("\n1️⃣ Running batch scraping example...")
        example_batch_scraping()
        
        print("\n" + "="*50)
        print("2️⃣ Running targeted scraping example...")
        example_targeted_scraping()
        
        print("\n" + "="*50) 
        print("3️⃣ Running business analysis example...")
        example_business_analysis()
        
        print("\n" + "="*50)
        print("4️⃣ Running custom search example...")
        example_custom_search()
        
    except KeyboardInterrupt:
        print("\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
    
    print(f"\n🏁 All examples completed!")
    print(f"📁 Check the 'examples_output' directory for generated CSV files")