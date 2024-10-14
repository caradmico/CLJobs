from time import sleep
from random import randint
from warnings import warn
from bs4 import BeautifulSoup
import requests
from jobs.models import Job  # Import the Django model

# Define the search queries and locations
queries = [
    'admin+office', 'real+estate', 'nonprofit', 'accounting+finance',
    'systems+networking', 'manufacturing', 'sales', 'technical+support',
    'business+management', 'software+QA+DBA', 'art+media+design',
    'marketing+advertising+PR', 'tv+film+video+radio'
]

# Define the locations (subdomains)
locations = ['sfbay', 'newyork', 'losangeles']  # Add more as needed

# Number of pages to scrape (120 posts per page)
num_pages_to_scrape = 2
pages = range(0, num_pages_to_scrape * 120, 120)

# Scraping process
def scrape_craigslist():
    # Loop through each location and query
    for location in locations:
        for query in queries:
            # Loop through each page of results
            for page in pages:
                # Construct the URL
                base_url = f"https://{location}.craigslist.org/search/jjj?query={query}&s={page}"
                response = requests.get(base_url)

                # Add random delay to avoid getting blocked
                sleep(randint(1, 5))

                # Error handling for non-200 status codes
                if response.status_code != 200:
                    warn(f'Request failed; Status code: {response.status_code}')
                    continue

                # Parse the HTML content of the page
                page_html = BeautifulSoup(response.text, 'html.parser')

                # Find all job posts on the page
                posts = page_html.find_all('li', class_='cl-static-search-result')

                # Scrape each post
                for post in posts:
                    try:
                        # Job link
                        job_link = post.find('a')['href']
                        
                        # Job title
                        job_title = post.find('div', class_='title').text.strip()

                        # Placeholder for company and description (Craigslist doesn't have these fields, so we might leave them blank)
                        company_name = "N/A"
                        description = "No description available."

                        # Extract salary if available (Craigslist doesn't always show salary)
                        salary = post.find('span', class_='result-price')
                        salary = salary.text.strip() if salary else "N/A"

                        # Extract the posting date if available
                        date_posted = post.find('time', class_='result-date')
                        date_posted = date_posted['datetime'] if date_posted else "N/A"

                        # Save job data to the database
                        Job.objects.get_or_create(
                            title=job_title,
                            company=company_name,
                            location=location,
                            salary=salary,
                            date_posted=date_posted,
                            url=job_link,
                            description=description,
                            source='Craigslist'
                        )

                        # Debugging: Print each scraped job
                        print(f"Scraped Job: {job_title} | Location: {location} | Category: {query}")

                    except Exception as e:
                        print(f"Error extracting data from post: {e}")

print("\nScrape complete! Data saved to the database.")
