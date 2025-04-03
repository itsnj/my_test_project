from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import asyncio

async def find_vessel_new_way(imo_number):
    session = AsyncHTMLSession()
    url = f"https://www.vesselfinder.com/vessels/details/{imo_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = await session.get(url, headers=headers)  
    await response.html.arender()  # Render JavaScript
    
    soup = BeautifulSoup(response.html.html, "html.parser")
    table = soup.find_all('table', {'class': 'aparams'})
    
    return table

def run():
    imo_number = "9648714"  # Example IMO number
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Run the coroutine using `ensure_future`
        task = asyncio.ensure_future(find_vessel_new_way(imo_number))
        return task
    else:
        return asyncio.run(find_vessel_new_way(imo_number))

