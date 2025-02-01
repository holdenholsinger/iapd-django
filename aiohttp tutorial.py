import aiohttp, asyncio

from bs4 import BeautifulSoup

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://httpbin.org/get') as resp:
#             print(resp.status)
#             print(await resp.text())
            
            
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

async def get_page(session, url):
    async with session.get(url) as r:
        return await r.text()
    

async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):
    async with  aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data
    
    
def parse(results):
    for html in results:
        soup = BeautifulSoup(html)
        print(soup.find("form", {'class': "form-horizontal"}).text.strip())
    
if __name__ == '__main__':
    urls = [
        "https://books.toscrape.com/catalogue/page-2.html",
        "https://books.toscrape.com/catalogue/page-3.html",
        "https://books.toscrape.com/catalogue/page-4.html"
    ]
    
    results = asyncio.run(main(urls))
    parse(results)