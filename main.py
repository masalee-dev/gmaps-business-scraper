"""
Google maps Business Scraper - Command Line Interface (CLI)
Author: Haeder Ali
"""

import click
import sys
from pathlib import Path
from google_maps_scraper import GoogleMapsScraper

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

        scraper = GoogleMapsScraper(headless=headless, delay=delay)

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