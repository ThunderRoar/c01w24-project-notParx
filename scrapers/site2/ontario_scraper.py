import requests
from bs4 import BeautifulSoup

## (Helper Function) Return prescriber status given a BeautifulSoup object of a prescriber page 
def parse_prescriber_page(soup, last_name: str, first_name: str):
    # Note: we assume that a license number HAD to have been passed. In this case, the ontario website always returns either a prescriber page for the given number or 0 results as the numbers are unique.
    # At this point, there are 3 cases: We receive a single page with some prescriber, we found no-one, or there was some server error

    ## Check for server error
    err_span = soup.find("span", {"id": "lblInfo"})
    if err_span != None and err_span.string != None and "error" in err_span.string:
        return "ERROR"

    ## Check prescriber name matches
    name_correct = False
    if soup.find("div", class_="name_cpso_num") != None:
        possible_name = soup.find("div", class_="name_cpso_num").find("h1", {"id": "docTitle"})
        if possible_name != None:
            name_str = possible_name.string
            if name_str != None: 
                name_split = name_str.split(",")
                if last_name.lower().strip() not in name_split[0].lower() or first_name.lower().strip() not in name_split[1].lower():
                    name_correct = False
                else:
                    name_correct = True
    
    # If we could not find the correct (or any) prescriber name, then we found no one. This accounts for the 0 results case as well.
    if not name_correct: 
        return "NOT FOUND"

    ## Check prescriber status
    candidates = soup.find("div", class_="doctor-info").find_all("strong") # First doctor info should always contain member status
    if len(candidates) > 0:
        for c in candidates:
            possible_status = c.string
            if possible_status != None: 
                if "Active Member" in possible_status:
                    return "VERIFIED"
                elif "Expired" in possible_status:
                    return "INACTIVE"

    # Only reachable if there is no information on prescriber status
    return "ERROR"

## Return prescriber status given last name, first name, and license number in the College of Physicians and Surgeons of Ontario
def get_status(last_name: str, first_name: str, number: str):
    ## Generate session
    url = "https://doctors.cpso.on.ca/?refine=true&search=quick"
    
    try:
        req = requests.get(url)
    except:
        return "ERROR"
    cookies = requests.utils.dict_from_cookiejar(req.cookies)

    soup = BeautifulSoup(req.text, 'html.parser')
    data = {}
    for asp_id in ["__VIEWSTATEGENERATOR", "__CMSCsrfToken", "__EVENTTARGET", "__EVENTARGUMENT", "__LASTFOCUS", "__VIEWSTATE"]:
        d = soup.find("input", {"id": asp_id})
        if d != None:
            data[asp_id] = d['value']

    ## Set up search
    search_data = {
        "searchType":"general",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtCPSONumberGeneral":number,
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtLastName":last_name,
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$txtFirstName":first_name,
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$grpDocType":"rdoDocTypeAll",
        "lng":"en-CA",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkActiveDoctors":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkInactiveDoctors":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$btnSubmit1":"Submit",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddHospitalName":-1,
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$ddLanguage":"08",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPracticeRestrictions":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPendingHearings":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkPastHearings":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkHospitalNotices":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkConcerns":"on",
        "p$lt$ctl01$pageplaceholder$p$lt$ctl02$CPSO_AllDoctorsSearch$chkNotices":"on",
    }
    data.update(search_data)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://doctors.cpso.on.ca",
        "Referer": "https://doctors.cpso.on.ca/?refine=true&search=quick",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    try:
        res = requests.post(url, cookies=cookies, headers=headers, data=data)
    except:
        return "ERROR"

    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        return parse_prescriber_page(soup, last_name, first_name)
    except:
        return "ERROR"

if __name__ == "__main__":
    # Sanity tests
    print(get_status("Edwards", "Bonnie", 30722)) # 'VERIFIED'
    print(get_status("Aaen", "Gregory", 89942)) # 'INACTIVE'    
    print(get_status("Pins", "Gregory", 54111)) # 'NOT FOUND' 