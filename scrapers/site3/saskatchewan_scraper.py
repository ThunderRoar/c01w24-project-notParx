import requests
from bs4 import BeautifulSoup
import json

def get_status(firstName: str, lastName: str, licenseNumber = ""):
    # Old way to generate session. Keep in case manual cookies fail
    # s = requests.Session()
    # r= s.get("https://www.cps.sk.ca/imis/")

    # Generate session and search token
    try:
        req = requests.get("https://www.cps.sk.ca/imis/")
    except:
        return "ERROR"
    cookies = requests.utils.dict_from_cookiejar(req.cookies)

    soup = BeautifulSoup(req.text, "html.parser")
    inp = soup.find("input", {"id": "__RequestVerificationToken"})
    token = inp["value"]
    headers = {
        "Requestverificationtoken": token
    }

    # Make and parse search results to determine status
    r = requests.get(f"https://www.cps.sk.ca/iMIS/api/iqa?QueryName=$/CPSS/PhysicianSearch/PhysicianSearchResults&parameter=&parameter=&parameter=&parameter=&parameter=&parameter=&parameter=%22{lastName}%22&parameter=&parameter=&limit=21", headers = headers, cookies = cookies)
    resp_json = json.loads(r.text)
    search_results = resp_json["Items"]["$values"]
    for candidate in search_results:
        candidate_first = ""
        candidate_last = ""
        candidate_status = ""
        for value in candidate["Properties"]["$values"]:
            if value["Name"] == "FirstName":
                candidate_first = value["Value"]
            if value["Name"] == "LastName":
                candidate_last = value["Value"]
            if value["Name"] == "Status":
                candidate_status = value["Value"]

        # Is this candidate the correct person?
        if (firstName.strip().lower() in candidate_first.lower() and lastName.strip().lower() in candidate_last.lower()):
            if (candidate_status == "On the Register"):
                return "VERIFIED"
            return "INACTIVE"
    return "NOT FOUND"

if __name__ == "__main__":
    print(get_status('Brittni', 'Webster')) # VERIFIED
    print(get_status('Ben', 'Thistlewood')) # INACTIVE
    print(get_status('Shreya', 'Moodley')) # INACTIVE
    print(get_status('abc123', 'abc123')) # NOT FOUND