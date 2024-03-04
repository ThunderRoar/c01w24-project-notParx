import requests
from bs4 import BeautifulSoup

def create_list(results_div):
    """
    Processes the results div to create a list of tuples containing the name and profile link.

    Parameters:
    - results_div: BeautifulSoup object representing the div with search results.

    Returns:
    - List of tuples with the name and profile link of each result.
    """
    results_list = []
    # Exclude the header row and iterate over each result row
    for row in results_div.find_all("tr")[1:]:
        name_link = row.find("a")
        if name_link:
            name = name_link.get_text(strip=True)
            link = name_link.get("href")
            results_list.append((name, link))
    return results_list

def open_profile_and_analyze(profile_url):
    """
    Fetches a physician's profile and determines their practicing status.

    Parameters:
    - profile_url: URL to the physician's profile.

    Returns:
    - True if the physician's status is 'Active', False otherwise.
    """
    response = requests.get(profile_url)
    if response.status_code != 200:
        return False
    # with open("./scrapers/tests/alberta_get_response_WilliamA.txt", 'w', encoding="utf-8") as f:
    #     f.write(response.text)
    soup = BeautifulSoup(response.content, 'html.parser')
    status_heading = soup.find("h3", string="Membership Status")
    if status_heading:
        parent_div = status_heading.parent
        if parent_div:
            status_div = parent_div.find_next_sibling("div", class_="medium-8 columns")
            if status_div:
                membership_status = status_div.get_text(strip=True)
                return "Active" == membership_status
    return False

def filter_results(soup, first_name, last_name):
    """
    Filters the search results and returns a list of relevant results.

    Parameters:
    - soup: BeautifulSoup object containing the parsed HTML of the search results page.
    - first_name: The first name to match in the search results.
    - last_name: The last name to match in the search results.

    Returns:
    - List of results if matches are found, False otherwise.
    """
    if "Results: 0 matches" in soup.text:
        return False
    else:
        results_div = soup.find("div", class_="small-12 column resultsTable")
        if results_div:
            return create_list(results_div)
        else:
            return False

def parse_results_page(soup, first_name, last_name):
    """
    Parses the results page and checks for an exact match.

    Parameters:
    - soup: BeautifulSoup object containing the parsed HTML of the results page.
    - first_name: The first name to match in the search results.
    - last_name: The last name to match in the search results.

    Returns:
    - True if an exact match is found and the physician is 'Active', False otherwise.
    """
    results = filter_results(soup, first_name, last_name)
    if results is False:
        return "NOT FOUND"
    elif isinstance(results, list):
        for result in results:
            result_name = result[0].split(", ")
            if len(result_name) > 1 and first_name.lower() in result_name[1].lower() and last_name.lower() in result_name[0].lower():
                # print(result[1])
                status = open_profile_and_analyze(result[1])
                # print(status)
                return("VERIFIED" if status else "INACTIVE")
        return "NOT FOUND"
    else:
        status = open_profile_and_analyze(results[0][1])
        return("VERIFIED" if status else "INACTIVE")

def get_status(last_name: str, first_name: str):
    """
    Retrieves the practicing status of a physician based on their last and first name.

    Parameters:
    - last_name: The last name of the physician.
    - first_name: The first name of the physician.

    Returns:
    - 'Active' if the physician is practicing, 'Non-Practicing' if not, or an error message.
    """
    # Create a session to maintain cookies across requests
    with requests.Session() as session:
        url = "https://search.cpsa.ca/"
        initial_req = session.get(url)
        if initial_req.status_code != 200:
            return "NOT FOUND"
        
        soup = BeautifulSoup(initial_req.text, 'html.parser')
        # with open("scrapers/tests/alberta_get_response.txt", 'w', encoding="utf-8") as f:
        #     f.write(initial_req.text)

        #form_data = {field.get("name"): field.get("value") for field in soup.find_all("input", {"name": True})}
        form_data = {}
        for field in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "__EVENTTARGET"]:
            element = soup.find("input", {"name": field})
            if element:
                form_data[field] = element["value"]
        # Update form data with search parameters
        form_data.update({
            "ctl00$ctl16": "ctl00$ctl16|ctl00$MainContent$physicianSearchView$btnSearch",
            "ctl00$MainContent$physicianSearchView$txtFirstName": first_name,
            "ctl00$MainContent$physicianSearchView$txtLastName": last_name,
            "ctl00$MainContent$physicianSearchView$btnSearch": "Search",
            "__ASYNCPOST": "true",
        })

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": url,
            "Referer": url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

        cookies = requests.utils.dict_from_cookiejar(initial_req.cookies)
        search_req = session.post(url, headers=headers, data=form_data, cookies=cookies)
        # with open("scrapers/tests/alberta_post_response_WilliamA.txt", 'w', encoding="utf-8") as f:
        #     f.write(search_req.text)
        if search_req.status_code != 200:
            return "NOT FOUND"

        search_soup = BeautifulSoup(search_req.text, 'html.parser')
        return parse_results_page(search_soup, first_name, last_name)

# Entry point for script execution
if __name__ == "__main__":
    status = get_status("Atherton", "William")
    print(status)