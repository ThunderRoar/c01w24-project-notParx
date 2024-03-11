import requests
from bs4 import BeautifulSoup


## Return prescriber status given last name, first name, and license number in the College of Physicians and Surgeons of Nova Scotia
def get_status(first_name: str, last_name: str, number: str):
    ## Generate session
    url = "https://cpsnsphysiciansearch.azurewebsites.net/"
    
    try:
        req = requests.get(url)
    except:
        return "ERROR"
    cookies = requests.utils.dict_from_cookiejar(req.cookies)

    soup = BeautifulSoup(req.text, 'html.parser')
    data = {}
    for asp_id in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]:
        d = soup.find("input", {"id": asp_id})
        if d != None:
            data[asp_id] = d['value']

    ## Set up search
    search_data = {
        "action":"Search",
        "licencenumber":number,
        "lastname":last_name,
        "firstname":first_name,
        "rbphysiciantype":1,
        "isonatlanticregistry":0,
        "rbgender":3
    }
    data.update(search_data)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://cpsnsphysiciansearch.azurewebsites.net",
        "Referer": "https://cpsnsphysiciansearch.azurewebsites.net/",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    ## Make Search
    res = requests.post("https://cpsnsphysiciansearch.azurewebsites.net/SearchResults.aspx", cookies=cookies, headers=headers, data=data)
    soup = BeautifulSoup(res.text, 'html.parser')

    ## Have to pad id with 0s to align with website ID format
    strnum = str(number)
    while len(strnum) < 6:
        strnum = "0"+strnum

    ## Parse search results
    tbody = soup.find("tbody")
    for tr in tbody.find_all("tr"):
        a = tr.find("a", {"href":f"/PhysicianDetails.aspx?LicenceNumber={strnum}"})
        if a == None:
            continue
        # Found a physician tbody with given id
        
        ## Parse name
        name_str = a.text
        if name_str == None or name_str == "":
            continue
        name_split = name_str.split(",")
        if last_name.lower().strip() not in name_split[0].lower() or first_name.lower().strip() not in name_split[1].lower():
            continue
        
        ## Parse status
        tds = tr.findAll("td")
        if len(tds) == 0:
            return "ERROR" # Website format has changed if this is reached
        if len(tds) > 1 and tds[1].find("span"): # SearchResults.aspx returns a span with text inside the second td for inactive members
            return "INACTIVE"
        return "VERIFIED"

    return "NOT FOUND" 

if __name__ == "__main__":
    ## Sanity Tests
    print(get_status("David", "Ley", 10819)) # Verified
    print(get_status("David", "Abriel", 6371)) # Inactive
    print(get_status("Wilfrid", "Bent", 5492)) # Inactive
    print(get_status("Allen", "Finley", 7959)) # Not Found