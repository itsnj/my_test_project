import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# -- Dynamic part (e.g., change for each vessel)
IMO_VALUE = "9837121"

# Proxy list (Free or paid proxy list can be used here)
def get_proxies():
    url = "https://www.proxy-list.download/api/v1/get?type=https"
    try:
        r = requests.get(url, timeout=10)
        return r.text.strip().split('\r\n')
    except Exception:
        return []

# Dynamic headers
def get_headers():
    ua = UserAgent()
    return {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.balticshipping.com',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': f'https://www.balticshipping.com/vessel/imo/{IMO_VALUE}',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random,
        'x-access-token': 'null',
        'Cookie': 'id=null; key=null; level=null; _ga=GA1.1.1579364598.1743484457;'  # optionally update or rotate
    }

# Form Data
def get_request_data(imo_value):
    return {
        'templates[]': [
            'modal_validation_errors:0',
            'modal_email_verificate:0',
            'r_vessel_types_multi:0',
            'r_positions_single:0',
            'vessel_profile:0',
        ],
        'request[0][module]': 'ships',
        'request[0][action]': 'list',
        'request[0][id]': '0',
        'request[0][data][0][name]': 'search_id',
        'request[0][data][0][value]': str(int(time.time() * 1000)),
        'request[0][data][1][name]': 'imo',
        'request[0][data][1][value]': imo_value,
        'request[0][sort]': '',
        'request[0][limit]': '1',
        'request[0][stamp]': '0',
        'request[1][module]': 'top_stat',
        'request[1][action]': 'list',
        'request[1][id]': '0',
        'request[1][data]': '',
        'request[1][sort]': '',
        'request[1][limit]': '',
        'request[1][stamp]': '0',
        'dictionary[]': [
            'countrys:0',
            'vessel_types:0',
            'positions:0'
        ]
    }

# Request logic
def fetch_baltic_shipping_data(imo_value, max_retries=5):
    api_url = "https://www.balticshipping.com/"
    proxies = get_proxies()
    retries = 0

    while retries < max_retries:
        proxy = random.choice(proxies) if proxies else None
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

        try:
            print(f"[Attempt {retries+1}] Fetching data for IMO: {imo_value} | Proxy: {proxy or 'None'}")
            response = requests.post(
                api_url,
                headers=get_headers(),
                data=get_request_data(imo_value),
                # proxies=proxy_dict,
                timeout=15
            )
            result = response.json()
            ships_count = result['data']['request'][0]['ships_found']
            ships_data = result['data']['request'][0]['ships']
            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                print("✅ Success")
                return {'ships_count': ships_count, 'ships_data': ships_data}
            else:
                print(f"⚠️ Status code: {response.status_code} | Response: {response.text[:200]}")
                return {}
        except Exception as e:
            print(f"❌ Error: {e}")

        retries += 1
        time.sleep(random.uniform(2, 5))  # Delay between retries

    raise Exception("Failed to fetch after multiple attempts.")

