import requests, time, parsing, aiohttp, asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Callable



def sections_to_parse(crd: int) -> List[Dict[str, Callable]]:
    """
    Accepts a CRD number and generates a list of dictionaries, each with the link to scrape and their respective scraping functions
    """
    url = f"https://files.adviserinfo.sec.gov/IAPD/crd_iapd_AdvVersionSelector.aspx?ORG_PK={crd}"
    r = requests.get(url)
    section_links = parsing.get_section_links(r)
    # the below dictionary will not have unique_hrefs, but rather section_links[0, 1, etc.] or something like that
    urls_and_funcs = [
        {"link": section_links['identifyinginfosection'], "function": parsing.identifying_info},
        {"link": section_links["advisorybusinesssection"], "function": parsing.advisory_business_info},
        {"link": section_links["privatefundreporting"], "function": parsing.private_fund_info},
        {"link": section_links["scheduled"], "function": parsing.schedule_d},
        {"link": section_links["signaturesection"], "function": parsing.signee},
    ]
    
    return urls_and_funcs


async def main(links_and_funcs: List[Dict[str, Callable]]) -> Dict:
    """
    Accepts the list of dictionaries with the link and each respective scraping function and awaits and returns the results as a list of dictionaries. This will eventually be processed into one dictionary.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in links_and_funcs:
            link = item["link"]
            func = item['function']
            task = asyncio.create_task(func(session, link))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results
    
    
def process_results(scraping_results: List[Dict]):
    """
    Takes the return values of all of the results, which is a list of dictionaries. It returns a single dictionary for easy return and logic when endpoint requested 
    """
    master_dict = {}
    for result in scraping_results:
        for key, value in result.items():
            master_dict[key] = value
            
    return master_dict
            


def scrape(crd_number):
    """
    Runs the scraping method and processes the result into a master dictionary
    """
    firm_links = sections_to_parse(crd_number)
    results = asyncio.run(main(firm_links))
    master_dict = process_results(results)
    return master_dict
    
    
if __name__ == '__main__':
    print(scrape(79))
