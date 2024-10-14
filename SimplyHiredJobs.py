import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Uncomment for headless mode if needed
# chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Define job categories and locations
categories = [
    "software+engineer",
    "data+scientist",
    "project+manager",
    "product+designer",
    "marketing",
    "sales",
    "administrative+assistant"
]

locations = ["San+Francisco", "New+York", "Los+Angeles"]

# Open CSV file for writing
with open('simplyhired_jobs.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Location", "Job Title", "Company", "Job Location", "Salary", "Posted Date"])  # CSV headers

    # Loop through each category and location
    for category in categories:
        for city in locations:
            # Construct URL for SimplyHired job search for the given category and location
            url = f"https://www.simplyhired.com/search?q={category}&l={city}"
            print(f"Opening URL: {url}")
            driver.get(url)

            # Wait for the main content to load
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, '__next'))
                )
                print(f"Main content loaded for {category} jobs in {city}.")

                # Extract job cards
                job_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="searchSerpJob"]')
                print(f"Found {len(job_cards)} job cards for {category} in {city}.\n")

                # Loop through the job cards and extract information
                for card in job_cards:
                    try:
                        # Extract job title
                        job_title = card.find_element(By.TAG_NAME, 'a').text if card.find_element(By.TAG_NAME, 'a') else "N/A"
                        
                        # Extract company name (if present)
                        company_name = card.find_element(By.CSS_SELECTOR, 'span[data-testid="companyName"]').text if card.find_element(By.CSS_SELECTOR, 'span[data-testid="companyName"]') else "N/A"
                        
                        # Extract job location
                        job_location = card.find_element(By.CSS_SELECTOR, 'span.css-1t92pv').text if card.find_element(By.CSS_SELECTOR, 'span.css-1t92pv') else "N/A"
                        
                        # Extract salary (if present)
                        salary = card.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobSalaryConfirmed"]').text if card.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobSalaryConfirmed"]') else "N/A"
                        
                        # Extract posted date (fallback for missing dates)
                        try:
                            date_posted = card.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobDateStamp"]').text
                        except:
                            date_posted = "N/A"
                            print(f"Error extracting date posted for job: {job_title}")

                        # Write the row to CSV (with category and city info)
                        writer.writerow([category.replace("+", " "), city.replace("+", " "), job_title, company_name, job_location, salary, date_posted])

                    except Exception as e:
                        print(f"Error extracting data from job card: {e}")

            except Exception as e:
                print(f"Error loading job cards for {category} in {city}: {e}")

# Close the browser
driver.quit()
print("Browser session closed. Job data has been written to simplyhired_jobs.csv")
