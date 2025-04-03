import requests
import random
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from traceback import format_exc

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# API URL
URL = "https://www.balticshipping.com/"

# Headers
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.balticshipping.com",
    "referer": "https://www.balticshipping.com/vessels",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": random.choice(USER_AGENTS),
    "x-access-token": ""
}

def save_to_json(data, start, end):
    # right_now = datetime.utcnow()
    final_data = {"all_data": data}
    filename = f"baltic_shipping_{start}_{end}.json"

    # Write JSON data to file
    with open(filename, "w") as file:
        json.dump(final_data, file, indent=4)  # indent=4 for pretty formatting

    print(f"JSON file '{filename}' has been saved successfully!")

# Function to get data
def get_data(page = 0):
    session = requests.Session()
    session.headers.update(HEADERS)

    # Rotate user agent and proxy
    session.headers["user-agent"] = random.choice(USER_AGENTS)

    # Data payload with dynamic ship name
    payload = {
        "request[0][module]": "ships",
        "request[0][action]": "list",
        "request[0][id]": 0,
        "request[0][data][0][name]": "search_id",
        "request[0][data][0][value]": 0,
        "request[0][data][1][name]": "name",
        "request[0][data][1][value]": "",  # Dynamic name input
        "request[0][data][2][name]": "imo",
        "request[0][data][2][value]": "",
        "request[0][data][3][name]": "page",
        "request[0][data][3][value]": page,
        "request[0][limit]": 27,
        "request[0][stamp]": 0,
        "request[1][module]": "top_stat",
        "request[1][action]": "list",
        "request[1][id]": 0,
        "request[1][data]": "",
        "request[1][stamp]": 0
    }

    try:
        print(f"✅ Hitting for Page: {page}")
        response = session.post(URL, data=payload)
        if response.status_code == 200:
            data = response.json()
            return data['data']['request'][0]['ships']
        else:
            print(f"Failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    finally:
        session.close()


def get_all_vessels(start_page, end, batch = 100):
    def process_page(page):
        try:
            report_data = get_data(page)
            return report_data
        except Exception as e:
            return [{
                'error': str(e),
                'traceback': format_exc(),
                'page': page
            }]

    for i1 in range(start_page, end, batch):
        end_page = i1 + batch
        all_vessels = []
        print(f"☑ now starting for i: {i1}")
        with ThreadPoolExecutor(max_workers=4) as executor:  # 4 threads in parallel
            futures = {executor.submit(process_page, i): i for i in range(i1, end_page)}

            for future in as_completed(futures):
                report_data  = future.result()
                if report_data:
                    all_vessels.extend(report_data)
    
        if all_vessels:
            save_to_json(all_vessels, i1, end_page)
    
    # for i in range(start_page, 3000, 100):
    #     print(f"☑ now starting for i: {i}")
    #     page = i
    #     end_page = i + 100
    #     all_vessels = []
    #     while page < end_page:
    #         vessels = get_data(page)
    #         if not vessels:
    #             break
    #         all_vessels.extend(vessels)
    #         page += 1
    #     save_to_json(all_vessels, start_page, page)
    return all_vessels
