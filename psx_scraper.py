import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_kse100_index():
    # URL for PSX indices
    url = "https://dps.psx.com.pk/indices"
    
    # Set up headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("Initializing WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"Loading page: {url}")
        driver.get(url)
        
        # Wait for the page to load fully (wait for spinner to disappear)
        print("Waiting for page to load...")
        time.sleep(10)  # Allow time for JavaScript to load content
        
        # Wait for tables to be visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        print("Page loaded, extracting data...")
        
        # Get the page source after JavaScript has loaded the content
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print(soup)
        # Find the tables on the page
        tables = soup.find_all('table')
        
        if not tables or len(tables) < 2:
            print(f"Could not find the required tables (found {len(tables)} tables)")
            return None, None
        
        # 1. Extract data for KSE100 index from the first table
        kse100_data = None
        index_table = tables[0]
        rows = index_table.find_all('tr')
        
        for row in rows[1:]:  # Skip header row
            cells = row.find_all('td')
            if cells and "KSE100" in cells[0].text:
                kse100_data = {
                    'Index': 'KSE100',
                    'High': cells[1].text.strip(),
                    'Low': cells[2].text.strip(),
                    'Current': cells[3].text.strip(),
                    'Change': cells[4].text.strip(),
                    'Percent_Change': cells[5].text.strip(),
                    'Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                break
        
        if not kse100_data:
            print("KSE100 index data not found in the table")
        
        # 2. Extract KSE100 constituents from the constituents table
        constituents_data = []
        
        # Look for the KSE100 constituents table - usually the second table or after specific heading
        constituents_table = None
        
        # Try to find by heading first
        for header in soup.find_all(['h3', 'h2', 'h4', 'div', 'span']):
            if header.text and "KSE 100 INDEX Constituents" in header.text:
                # Look for the next table after this header
                current = header.next_sibling
                while current:
                    if current.name == 'table':
                        constituents_table = current
                        break
                    current = current.next_sibling
        
        # If not found by heading, use the second table if available
        if not constituents_table and len(tables) >= 2:
            constituents_table = tables[1]
        
        if constituents_table:
            # Get all rows except the header
            constituent_rows = constituents_table.find_all('tr')[1:]  # Skip header
            
            # Process each row to extract company data
            for row in constituent_rows:
                cells = row.find_all('td')
                if len(cells) >= 7:  # Ensure we have enough cells in row
                    constituent = {
                        'Symbol': cells[0].text.strip(),
                        'Name': cells[1].text.strip(),
                        'LDCP': cells[2].text.strip() if len(cells) > 2 else '',
                        'Current': cells[3].text.strip() if len(cells) > 3 else '',
                        'Change': cells[4].text.strip() if len(cells) > 4 else '',
                        'Change_Percent': cells[5].text.strip() if len(cells) > 5 else '',
                        'Volume': cells[7].text.strip() if len(cells) > 7 else '',
                        'Market_Cap': cells[9].text.strip() if len(cells) > 9 else ''
                    }
                    constituents_data.append(constituent)
        
        if not constituents_data:
            print("KSE100 constituent data not found")
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None, None
    finally:
        # Close the browser
        driver.quit()
        
    return kse100_data, constituents_data

def save_to_csv(data, filename="kse100_data.csv"):
    """Save the scraped data to a CSV file"""
    if not data:
        print(f"No data to save to {filename}")
        return
        
    df = pd.DataFrame([data] if not isinstance(data, list) else data)
    
    try:
        # Check if file exists to determine if we need to write headers
        try:
            existing_df = pd.read_csv(filename)
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

if __name__ == "__main__":
    print("Scraping KSE100 index data from PSX website...")
    kse100_data, constituents_data = scrape_kse100_index()
    
    # Save and display index data
    if kse100_data:
        print("\nKSE100 Index Data:")
        for key, value in kse100_data.items():
            print(f"{key}: {value}")
        
        # Save index data to CSV
        save_to_csv(kse100_data, "kse100_index.csv")
    else:
        print("Failed to retrieve KSE100 index data")
    
    # Save and display constituents data
    if constituents_data:
        print(f"\nKSE100 Constituents: {len(constituents_data)} companies found")
        
        # Print the first 5 constituents as a sample
        for i, company in enumerate(constituents_data[:5]):
            print(f"\nCompany {i+1}:")
            for key, value in company.items():
                print(f"  {key}: {value}")
        
        if len(constituents_data) > 5:
            print("... and more companies")
        
        # Save constituents data to CSV
        save_to_csv(constituents_data, "kse100_constituents.csv")
    else:
        print("Failed to retrieve KSE100 constituents data") 