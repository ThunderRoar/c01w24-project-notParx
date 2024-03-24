import requests
from bs4 import BeautifulSoup
import json

GET_URL = "https://www.cpsbc.ca/public/registrant-directory"
POST_URL = "https://www.cpsbc.ca/public/registrant-directory/search-result?ajax_form=1&_wrapper_format=drupal_ajax&_wrapper_format=drupal_ajax"

def get_status(firstName: str, lastName: str, licence_num=""):   
    # Generate cookie and form ID
    try:
        req = requests.get(GET_URL)
    except:
        return "ERROR"
    cookies = requests.utils.dict_from_cookiejar(req.cookies)

    # Extract form build ID
    soup = BeautifulSoup(req.text, 'html.parser')
    d = soup.find("input", {"name": "form_build_id"})
    form_build_id = d["value"]

    # Make search request
    data = {
        "form_build_id": form_build_id,
        "form_id":"cpsbc_directory_form",
        "ps_last_name": lastName,
        "ps_first_name": firstName,
        "PracticeTypeSearch": "A",
        "CertificationTypes": 0,
        "status": "A",
        "results_per_page":"10",
        "_triggering_element_name":"op",
        "_triggering_element_value":"Search",
        "ajax_page_state[theme]":"college",
        "ajax_page_state[theme_token]": "",
        "ajax_page_state[libraries]": "addtoany/addtoany.front,big_pipe/big_pipe,classy/base,classy/messages,college/bootstrap,college/global-theming,core/drupal.autocomplete,core/internal.jquery.form,core/normalize,cpsbc_directory/cpsbc_directory,matomo/matomo,search_api_autocomplete/search_api_autocomplete,system/base,views/views.module"
    }
    r = requests.post(POST_URL, data=data, cookies=cookies)

    # Parse results
    j = json.loads(r.text)
    soup = BeautifulSoup(j[2]["data"], 'html.parser')
    result_divs = soup.find_all("div", class_="result-item")
    for div in result_divs:
        
        # Confirm correct name
        name_div = div.find("div", class_="ps-contact__title")
        name = name_div.find("a").text
        if name is not None:
            (last_candidate, first_candidate) = name.split(',')
        if (firstName.lower() not in first_candidate.lower() or lastName.lower() not in last_candidate.lower()):
            continue
        
        # Confirm status
        status_divs = div.find_all("div", class_="ps-contact__element mt-2")
        for st in status_divs:
            txt = st.text
            if txt is None:
                continue
            txt = txt.strip()
            if "Registration status:" in txt:
                if "Practising" == txt[-10:]:
                    return "VERIFIED"
                return "INACTIVE"
        # Name is correct, but no status? Considered inactive
        return "INACTIVE"
    return "NOT FOUND"

if __name__ == "__main__":
    print(get_status("Amanpreet", "Gill")) # VERIFIED
    print(get_status("Aalto", "Anu")) # NOT FOUND 
    print(get_status("Davey", "Gin")) # VERFIED
    print(get_status("Ian", "Gillespie")) # VERFIED
    print(get_status("Anthony", "Keen")) # NOT FOUND
    print(get_status("Jian", "Zhou")) # INACTIVE

