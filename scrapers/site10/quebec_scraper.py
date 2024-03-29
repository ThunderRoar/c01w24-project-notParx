from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import requests
import json
import chompjs

DIRECTORY_URL = "https://www.cmq.org/api/directory"

def get_status(first_name:str, last_name: str, number: str):
    while len(number) < 5:
        number = "0" + number
    url = 'https://www.cmq.org/fr/bottin/medecins?number=' + number + '&lastname=' + last_name + "&firstname=" + first_name

    # r = requests.get("https://www.cmq.org/fr/bottin/medecins?number=77587")
    r = requests.get(url)

    # Locate Prescriber info block
    txt = r.text
    end_idx = -1
    start_idx = txt.find("$MVmgt5UHrw:")
    if start_idx == -1:
        return "ERROR"
    start_idx += 12
    end_idx = txt.find("]", start_idx)
    if end_idx == -1:
        return "ERROR"

    # List of internal website physician Ids resulting from our search
    search_results_list = chompjs.parse_js_object(txt[start_idx:end_idx + 1])

    # List through options, call internal Directory API, and find relevant status.
    for option in search_results_list:
        internal_id = option['physicianId']
        headers = {
            "Content-Type": "application/json",
        }
        data = json.dumps({"language":"fr","method":"getPhysicianDetails","physicianId":internal_id})

        try:
            r = requests.post(DIRECTORY_URL, data = data, headers=headers)
            res_data = json.loads(r.text)
            option_first = res_data.get("firstname", "")
            option_last = res_data.get("lastname", "")
            option_status = res_data.get("status", "")

            if first_name in option_first and last_name in option_last:
                if option_status == 'Inscrit - Actif':
                    return 'VERIFIED'
                else:
                    return "INACTIVE"
        except:
            return "ERROR"
    
    return "NOT FOUND"


if __name__ == "__main__":
    print(get_status(first_name = "Ali", last_name='Lopez Sarmiento', number='4426')) # Verified
    # print(get_status(first_name = "Alo", last_name='Lopez Sarmiento', number='4426')) # Not found
    # print(get_status(first_name = "Alexia", last_name='Lam', number='96332')) # Not found
    # print(get_status(first_name = "Annie", last_name='Li', number='15332')) # Verified
    # print(get_status(first_name = "B", last_name='Li', number='15332')) # Not found
    # print(get_status(first_name = "Alexia", last_name='Auger Labadie', number='27959')) # Not Found
    # print(get_status(first_name = "Alexia", last_name='Li', number='15333')) # Not Found
    # print(get_status(first_name = "", last_name='Shalaby', number='77587')) # Inactive