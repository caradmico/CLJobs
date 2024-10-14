
Gemini
Hello, Cara
How can I help you today?
What can Gemini do
in Google Drive
Search for files
by name, file type, author, etc
Write a report
using content from your Drive
Gemini for Workspace can make mistakes, including about people, so double-check it. Learn more
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome()

# Define a list of regions and keywords
regions = ['San+Francisco', 'New+York', 'Los+Angeles', 'Chicago', 'Austin']
keywords = ['software engineer', 'developer', 'data analyst', 'marketing', 'project manager']

# Open CSV to save data
with open('indeed_jobs_by_region.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Region', 'Job Title', 'Company', 'Job Link'])

    # Loop through each region and keyword combination
    for region in regions:
        for keyword in keywords:
            for page in range(0, 50, 10):  # Adjust number of pages if needed
                # Construct the Indeed URL
                base_url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={region}&start={page}"
                print(f"Fetching: {base_url}")
                
                driver.get(base_url)

                try:
                    # Explicitly wait until job cards are present
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'job_seen_beacon'))
                    )
                    print(f"Page loaded successfully for {region}, {keyword}, page {page//10 + 1}")
                except Exception as e:
                    print(f"Error waiting for job cards on page {page//10 + 1}: {e}")
                    continue

                # Scrape job cards on this page
                job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

                if not job_cards:
                    print(f"No job cards found on page {page//10 + 1}")
                else:
                    print(f"Found {len(job_cards)} job cards on page {page//10 + 1}")

                # Extract data from job cards
                for card in job_cards:
                    try:
                        job_title_element = card.find_element(By.CSS_SELECTOR, 'h2 a')
                        job_title = job_title_element.text if job_title_element else 'N/A'

                        try:
                            company_name_element = card.find_element(By.CSS_SELECTOR, 'span.companyName')
                            company_name = company_name_element.text if company_name_element else 'N/A'
                        except:
                            company_name = 'N/A'

                        job_link = job_title_element.get_attribute('href') if job_title_element else 'N/A'

                        # Write to CSV with region
                        writer.writerow([region.replace('+', ' '), job_title, company_name, job_link])

                        # Print a few sample entries for debugging
                        print(f"Job Title: {job_title}, Company: {company_name}, Link: {job_link}")
                    except Exception as e:
                        print(f"Error extracting data: {e}")

# Close the browser
driver.quit()
print("Scraping complete! Data saved to indeed_jobs_by_region.csv")