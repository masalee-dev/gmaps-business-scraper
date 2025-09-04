"""
Google maps Business Scraper - Command Line Interface (CLI)
Author: Haeder Ali
"""

import click
import sys
from pathlib import Path
from google_maps_scraper import GoogleMapsBusinessScraper

@click.command()
@click.option('--query', '-q', required=True, help='Business type to search for (e.g., "restaurants", "retail stores")')
@click.option('--location', '-l', required=True, help='Location to search in (e.g., "New York, NY")')
@click.option('--max-results', '-m', default=50, help='Maximum number of results to scrape')
@click.option('--output', '-o', default='businesses.csv', help='Output CSV filename')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
@click.option('--sheets-id', help='Google Sheets ID to upload results')
@click.option('credentials', help='Path to Google API credentials JSON file')
@click.option('--delay', default=2, help='Delay between requests in seconds')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def scrape(query, location, max_results, output, headless, sheets_id, credentials, delay, verbose):
    """
    Scrape business data from Google Maps.
    
    Example usage:
        pyhton main.py -q "coffee shops" -l "Seattle, WA" -m 100 -o coffee_seattle.csv
        
    """

    if verbose:
        click.echo(f"Starting Google Maps Scraper...")
        click.echo(f"Query: {query}")
        click.echo(f"Location: {location}")
        click.echo(f"Max results: {max_results}")
        click.echo(f"Output: {output}")
        click.echo(f"Headless: {headless}")

    # Validate Google Sheets parameters
    if sheets_id and not credentials:
        click.echo("Error: --credentials required when --sheets-id", err=True)
        sys.exit(1)

    if credentials and not Path(credentials).exists():
        click.echo(f"Error: Credentials file {credentials}", err=True)
        sys.exit(1)

    scraper = None

    try:
        # Intialize scraper
        if verbose:
            click.echo("Initializing scraper...")

        scraper = GoogleMapsBusinessScraper(headless=headless, delay=delay)

        # Perform search
        if verbose:
            click.echo(f"Searching for '{query}' in '{location}'...")

        with click.progressbar(length=max_results, label='Scraping businesses') as bar:
            scraper.search_businesses(
                query=query,
                location=location,
                max_results=max_results,
                progress_callback=bar.update
            )

        if not scraper.businesses:
            click.echo("No businesses found. Try adjusting your search terms.", err=True)
            return
        
        click.echo(f"Successfully scraped {len(scraper.businesses)} businesses.")

        # Save to CSV
        if verbose:
            click.echo(f"Saving to CSV: {output}")

        # Update to Google Sheets if requested
        if sheets_id and credentials:
            if verbose:
                click.echo("Uploading to Google Sheets...")

            try:
                scraper.save_to_google_sheets(sheets_id, credentials)
                click.echo("✅ Data uploaded to Google Sheets")
            except Exception as e:
                click.echo(f"❌ Failed to upload to Google Sheets: {e}", err=True)

        # Display Summary
        click.echo("\n📊 Summary:")
        click.echo(f"Total businesses scraped: {len(scraper.businesses)}")

        # Show sample of data
        if scraper.businesses:
            click.echo("\n📝 Sample data:")
            sample = scraper.businesses[0]
            for key, value in sample.items():
                if value: # Only show non-empty values
                    click.echo(f" {key}: {value}")
    
    except KeyboardInterrupt:
        click.echo("\n⚠ Scraping interrupted by user", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback,format_exc(), err=True)
        sys.exit(1)

    finally:
        if scraper:
            scraper.close()
    
@click.command()
@click.option('--config-file', default='congig.json', help='Configuratuion file path')
def batch(config_file):
    """
    Run batch scraping using a configuration file.
    
    Config file should contain:
    {
        "searches": [
            {
                "query": "restaurants",
                "location": "New York, NY",
                "max_results": 50,
                "output": "ny_restaurants.csv"
            }
        ],
        "settings": {
            "headless": true,
            "delay": 2
        }
    }
    """
    import json

    if not Path(config_file).exists():
        click.echo(f"Config file not found: {config_file}", err=True)
        sys.exit(1)
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)

        searches = config.get('searcher', [])
        settings = config.get('settings', {})

        scraper = GoogleMapsBusinessScraper(
            headless=settings.get('headless', True),
            delay=settings.get('delay', 2)
        )

        for i, search in enumerate(searches, 1):
            click.echo(f"\n🔎 Batch job {i}/{len(searches)}")
            click.echo(f"Query: {search['query']}, Location: {search['location']}")

            scraper.search_businesses(
                query=search['query'],
                location=search['location'],
                max_results=search.get('max_results', 50)
            )

            output_file = search.get('output', f"batch_{i}.csv")
            scraper.save_to_csv(output_file)

            click.echo(f"✅ Saved {len(scraper.businesses)} businesses to {output_file}")

            # Clear businesses for next search
            scraper.businesses = []
        
        scraper.close()
        click.echo("\n🎉 Batch scraping completed.")
    
    except Exception as e:
        click.echo (f"❌ Bacth Error: {e}", err=True)
        sys.exit(1)

@click.group()
def cli():
    """Google Maps Business Scraper - Extract business data from Google Maps."""
    pass

cli.add_command(scrape)
cli.add_command(batch)

if __name__ == '__main__':
    cli()