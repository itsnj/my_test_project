from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from vessel_finder.vessel_tracking import find_vessel
from io import StringIO
import csv
from datetime import datetime
from traceback import format_exc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import json
import time
# errored imo_numbers for 185-195: [9723174, 9701358, 9552410, 9479307, 9595591, 9520716, 9511947, 9595606, 9463334, 9256200, 9463322, 9241657, 8213627]
# errors in page 177 for 170-185 retry it

# 3 to 10 done 
# 199 to 200 done
# 195 to 199 done
# 185 to 195 done
# 170 to 185 done
# 160 to 170 done
# 150 to 151 done
# 151 to 160 done
# 140 to 150 done
# 130 to 140 done
# 120 to 130 done
# 110 to 120 done
# 100 to 110 retry
# 15 to 17 done
# 10 to 11 done

count = 0

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def initialise_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

    # Set a custom User-Agent to mimic a regular browser
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")  # Prevent memory issues
    driver = webdriver.Chrome(options=chrome_options)
    # driver.set_page_load_timeout(30)  # Set timeout to 30 seconds
    return driver

def get_all_vessel_pages(start_page, end_page, count=0):
    final_report_data = []
    final_headings = []
    errors = []
    print_start_page = start_page
    for i in range(start_page, end_page):
        try:
            print(f"☑ Started for page {i}")
            report_data, headings = get_all_vessels(i+1, count)
            if report_data:
                final_report_data.extend(report_data)
            final_headings.extend(headings)
            print(f"✅ Done for page {i}")
        except Exception as e:
            print(f"❌ Error for page {i} as : {e}")
            errors.append({
                'error': str(e),
                'traceback': format_exc(),
                'page': i
            })
            if len(errors) > 2:
                save_to_json({'error': f"Stopping the loop for start {start_page} and end {end_page} at page {i}"}, start_page, end_page)
                break
            continue
        right_now = datetime.utcnow()

        if i > start_page and i % 5 == 0 and final_report_data:
            csv_filename = f"vessel_tracking_from_vessel_finder_{i-5}_{i}.csv"
            csv_output = StringIO()
            writer = csv.writer(csv_output)
            final_report_data = [data for data in final_report_data if data]
            writer.writerow(final_headings[0])
            writer.writerow([])
            writer.writerows(final_report_data)
            
            with open(csv_filename, "w", newline="") as file:
                file.write(csv_output.getvalue())
            
            final_report_data = []
            final_headings = []
            print(f"Sleeping for 60 seconds")
            time.sleep(60)
            print(f"Done sleeping for 60 seconds")
        
        if i >= end_page:
            print_start_page = i - 5
    
    if final_report_data:
        csv_filename = f"vessel_tracking_from_vessel_finder_{print_start_page}_{end_page}.csv"
        csv_output = StringIO()
        writer = csv.writer(csv_output)
        final_report_data = [data for data in final_report_data if data]
        writer.writerow(final_headings[0])
        writer.writerow([])
        writer.writerows(final_report_data)
        
        with open(csv_filename, "w", newline="") as file:
            file.write(csv_output.getvalue())
    
    return final_report_data, errors

def get_vessel_html(page):
    url = f"https://www.vesselfinder.com/vessels?page={page}"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.vesselfinder.com/vessels",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Cookie": "ROUTEID=.1; _ga=GA1.1.1111779247.1743407228; usprivacy=1---; _sharedID=44c0c535-fb6a-4b78-abb6-3a8c68de0351; _cc_id=a35ba6c6431e18daf8c8d4cd8cdb2258; panoramaId_expiry=1744012028324; panoramaId=967e0898d03d5fd7835371c294124945a702114c41c7a694d37687c784538a53; panoramaIdType=panoIndiv; _sharedid=c9a9009d-b0c4-463b-bf61-61bf81d841e1; _sharedid_cst=TyylLI8srA%3D%3D; _ga_0MB1EVE8B7=GS1.1.1743503177.4.0.1743503177.0.0.0; __gads=ID=836799654205b455:T=1743407232:RT=1743503179:S=ALNI_MYjQNS4gsC44Qch0FQcj-JVvQVVRQ; __gpi=UID=000010808e7d36a9:T=1743407232:RT=1743503179:S=ALNI_MZFTuq9P95paDPimplri6ZIBkcSrw; __eoi=ID=c1639508f17d6c74:T=1743407232:RT=1743503179:S=AA-AfjaE03MojJLEsPPCECjcbcn8; _sharedID_cst=kSylLAssaw%3D%3D; cto_bundle=e0HIqF8lMkJXb1Zkb0xRU3dQOG1rNWFJdkFRJTJCNHlnZmZsJTJCRkVTVzMzdFdoZW03NzFNakdpbmtSUGRFMEI0RlJUTlJDYXpaZ1hRWEtrUjAwUmgwY29MMDZMYnhaQkphUUZNZlJqZVRkYnQ5SmhMSHhHaFprSkkwWXlzNG5ocWtJclRCWmp2ZmJqZmlrcXlwbVZHZkh6MERJOHlEcHBxUUo5d25EaE1ySXgxZHUzdHNMNWt3QjY4eElhS1NOMWdORm5rSmFudjRPODNqYUxSVFU4UXlwSHh4NHpSMXpaYkVMdGRROTI5VFM5VkpHa2JzeENidVo0VkI5MjYwUzU3Z3hISkclMkY2T3NsZEJGQiUyQkZHa0ZDZTlvZlF5ckdqbGclM0QlM0Q; cto_bidid=eyjoLF9Gd3JhNWElMkZQTUVQMWZ1QzJXTU53U0Fhbm95NEp5b3ZDbGc4QkR1YXFVcnU0UmJJMm1xZVIlMkZzZnFmWW1VcDBTS0pOWlQzTG10RGlNMEM1cDBGNnZzcER1dUpQS2FqQnhtajMlMkZTJTJCem42cmxEZDJ4bWdZWkRXR3BYV2UlMkJQQkZZQk8"
}

    response = requests.get(url, headers=headers)
    html = response.text.strip()
    return html

def get_all_vessels(page, count):
    html = get_vessel_html(page)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all('table', {'class': 'results'})
    elements = table[0].find_all('tr')
    element_href = []
    for element in elements:
        a_element = element.find('a')
        if a_element:
            href = a_element.get('href')
            element_href.append(href)
    
    all_imo_numbers = []
    error_count = 0
    for href in element_href:
        parts = href.split('/')
        all_imo_numbers.append(parts[-1])
    
    all_vessel_data = []
    headings = []
    # imo_numbers = all_imo_numbers[0:1]
    driver = None
    print(f"Extracted all the imo numbers for page: {page}")
    for imo_number in all_imo_numbers:
        if count % 10 == 0 or not driver:
            if driver:
                print(f"Quitting Driver at count {count} at Page {page}")
                driver.quit()
            driver = initialise_driver()
        try:
            vessel_data = find_vessel(imo_number, driver)
            all_vessel_data.append(vessel_data.get('heading_values') or (['']*11).append(imo_number))
            headings.append(vessel_data.get('final_headings') or (['']*11).append('IMO'))
        except Exception as e:
            error_count += 1
            print(f"❌ Error for page {page} imo number: {imo_number} as : {e}")
            all_vessel_data.append({
                'imo_number': imo_number,
                'error': str(e)
            })
            if error_count > 3:
                print(f"❌ Error count exceeded for page {page}")
                save_to_json({'error': f"Stopping at imo number {imo_number} for page {page}"}, page, imo_number)
                break
        count += 1
    
    if driver:
        print(f"Quitting Driver finally at count {count} at Page {page}")
        driver.quit()
    return all_vessel_data, headings

def using_scraper_api():
    payload = { 'api_key': 'cbf61dfa877ddd3e4d4810967ef0af42', 'url': 'https://www.vesselfinder.com/vessels/details/9540120' }
    r = requests.get('https://api.scraperapi.com/', params=payload)
    return r.text

def save_to_json(data, start, end):
    # right_now = datetime.utcnow()
    final_data = {"all_data": data}
    filename = f"error_{start}_{end}.json"

    # Write JSON data to file
    with open(filename, "w") as file:
        json.dump(final_data, file, indent=4)  # indent=4 for pretty formatting

    print(f"JSON file '{filename}' has been saved successfully!")