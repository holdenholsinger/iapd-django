from bs4 import BeautifulSoup

def get_section_links(r):
    """
    Takes the home page of the adv and returns the relevant sections' links to pass along to the scraper functions
    """
    soup = BeautifulSoup(r.content, "html.parser")
    navbar_links = soup.find_all("a", class_="navbar-link")
    raw_hrefs = list(set([link.get("href").strip() for link in navbar_links]))
    unique_hrefs = ["https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/" + link[3:] for link in raw_hrefs] 
    substrings = ["IdentifyingInfoSection", "ScheduleD", "PrivateFundReporting","AdvisoryBusinessSection","SignatureSection"]
    
    relevant_hrefs = {}
    for href in unique_hrefs:
        for substring in substrings:
            if substring in href:
                relevant_hrefs[substring.lower()] = href
    
    return relevant_hrefs

async def identifying_info(session, url):
    """
    Finds the name of the firm and the address with logic to add an address line 2 if necessary
    """
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        firm_name = soup.find('span', id='ctl00_ctl00_cphMainContent_cphAdvFormContent_IdentInfoPHSection_ctl00_lblFullLegalName')
        
        address_fields_table = soup.find(lambda tag: tag.name == "i" and "Principal Office and Place of Business" in tag.text).parent.parent.next_sibling.find('table')
        is_address_2_present = address_fields_table.find(lambda tag: tag.name == "td" and "Number and Street 2" in tag.text).find("span").text
        address_fields_raw = address_fields_table.find_all(class_="PrintHistRed")
        
        address_fields_final = address_fields_raw[:6] if is_address_2_present else address_fields_raw[:5]
        
        firm_info = {
            'firm_name': firm_name.get_text(strip=True).title(),
            'address1': address_fields_final[0].get_text(strip=True).title(),
            'address2': address_fields_final[1].get_text(strip=True).title() if is_address_2_present else None,
            'city': address_fields_final[1 if not is_address_2_present else 2].get_text(strip=True).title(),
            'state': address_fields_final[2 if not is_address_2_present else 3].get_text(strip=True),
            'zip': address_fields_final[4 if not is_address_2_present else 5].get_text(strip=True),
        }
        
        return firm_info

async def advisory_business_info(session, url):
    """
    Finds and returns employee count, number of employees providing advisoary functions and AUM
    """
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        employee_count = soup.find(class_="PrintHistRed").get_text(strip=True)
        advisory_employees = soup.find_all(class_="PrintHistRed")[1].get_text(strip=True)
        
        aum_table = soup.find(lambda tag: tag.name == "tr" and "what is the amount of your regulatory" in tag.text)
        aum = aum_table.find_all(class_="PrintHistRed")[4].text[2:]
        
        return {
            "employee_count": employee_count, 
            "advisory_employees": advisory_employees,
            "aum": aum,
            }

async def private_fund_info(session, url):
    """
    Iterates through radio buttons on each private fund to find both number of private funds and number of hedge funds
    """
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        try:
            td_elements = soup.find_all("td", attrs={'colspan': '5'})
            td_elements_filtered = [
            td.parent.next_sibling for td in td_elements
            if td.get_text(strip=True) and "What type of fund is the" in td.get_text(strip=True)
            ]
            
            pf_count = len(td_elements_filtered) if td_elements_filtered else 0
            
            hedge_fund_count = 0
            
            for td in td_elements_filtered:
                hedge_fund_tag = td.find('img')
                is_hedge_fund = "Radio button selected" in hedge_fund_tag.get('alt')
                if is_hedge_fund:
                    hedge_fund_count += 1
            
            return {
                'private_funds_count': pf_count,
                'hedge_fund_count': hedge_fund_count,            
                    }
            
        except:
            return {
                'private_funds_count': 0,
                'hedge_fund_count': 0,            
                    }
        
        


async def schedule_d(session, url):
    """
    Checks (a) and (b) on 5.K.1 on Schedule D and runs some calculations to find the larger of percent derivatives, formats, then returns it
    """
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        # derivatives_tag = soup.find("td", class_="NoLeftWithRightTD",text=lambda text: text and "Derivatives" in text).nextSibling
        derivatives_tags_siblings = soup.find_all("td", class_="NoLeftWithRightTD",text=lambda text: text and "Derivative" in text)[:2]
        derivatives_tags = [
            derivatives_tag.nextSibling.find('span').text
            for derivatives_tag in derivatives_tags_siblings
        ]
        
        derivative_strings = [
            tag_string.replace("\xa0", "").rstrip('%')
            for tag_string in derivatives_tags
            ]
        
        derivate_ints = [
            int(deriv_string) if deriv_string else 0
            for deriv_string in derivative_strings
        ]
        
        percent_derivatives = f'{max(derivate_ints)}%'
        return {"percent_derivatiaves": percent_derivatives}


async def signee(session, url):
    """
    Finds ADV Signee and formats to title case
    """
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')
        signee = soup.find('span', class_="PrintHistRed").text.title()
        return {'signee': signee}

