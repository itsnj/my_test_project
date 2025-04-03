from bs4 import BeautifulSoup
import requests
import re
import asyncio
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException
['Predicted ETA : -', 'Distance / Time : -', 'Course / Speed : 67.7° / 0.4 kn', 'Current draught : 19.1 m', 'Navigation Status : -', 'Position received : 29 days ago', 'IMO / MMSI : 9648714 / 503000101', 'Callsign : VNKL', 'Flag : Australia', 'Length / Beam : 488 / 74 m']

def find_vessel(imo_number, driver):
    print(f"Starting for imo number: {imo_number}")
    if not imo_number:
        return []
    url = f"https://www.vesselfinder.com/vessels/details/{imo_number}"
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find_all('table', {'class': 'aparams'})
        headings_text = [item.text for item in table[0].find_all('td')]
        final_headings = ['Vessel Name']
        heading_values = [soup.find('h1', {'class': 'title'}).text]
        for i in range(0, len(headings_text), 2):
            final_headings.append(headings_text[i].strip())
            heading_values.append(headings_text[i + 1].strip())
        final_headings.append('IMO')
        heading_values.append(imo_number)
        return {'final_headings': final_headings, 'heading_values': heading_values, 'imo_number': imo_number}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
