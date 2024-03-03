import requests
from bs4 import BeautifulSoup

def create_list(results_div):
    # Process the results div to create a list of tuples (name, profile link)
    results_list = []
    rows = results_div.find_all("tr")[1:]  # Skip the header row
    for row in rows:
        name_link = row.find("a")
        if name_link:
            name = name_link.get_text(strip=True)
            link = name_link.get("href")
            results_list.append((name, link))
    return results_list

def open_profile_and_analyze(profile_url):
    response = requests.get(profile_url)
    if response.status_code != 200:
        #print(f"Error fetching profile: {response.status_code}")
        return False

    # Parse the HTML content of the profile page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <h3> element that contains the text 'Membership Status'
    status_heading = soup.find("h3", string="Membership Status")
    if status_heading:
        # Find the parent <div> of the <h3> tag
        parent_div = status_heading.parent
        if parent_div:
            # Find the next <div> sibling of the parent <div> which should contain the <p> tag with status
            status_div = parent_div.find_next_sibling("div", class_="medium-8 columns")
            if status_div:
                # Get the text from the <p> tag
                membership_status = status_div.get_text(strip=True)
                return "Active" == membership_status

    return False

def filter_results(soup, first_name, last_name):
    if "Results: 0 matches" in soup.text:
        #print("No results found")
        return False
    else:
        results_div = soup.find("div", class_="small-12 column resultsTable")
        if results_div:
            lists = create_list(results_div)
            #print(lists)
            return lists
        else:
            return False

def parse_results_page(soup, first_name, last_name):
    results = filter_results(soup, first_name, last_name)
    if results is False:
        # Case 1: No results found
        #print("No results found")
        return False
    elif isinstance(results, list):
        # If suggested results, check if any match the given first and last name
        for result in results:
            result_name = result[0].split(", ")
            if len(result_name) > 1 and first_name.lower() in result_name[1].lower() and last_name.lower() in result_name[0].lower():
                # Exact match found, open profile and analyze
                #print("Exact match found")
                return open_profile_and_analyze(result[1])
        # No exact match found in suggestions
        #print("No exact match found")
        return False
    else:
        # Case 2.2: We have one exact result, open profile and analyze
        return open_profile_and_analyze(results[0][1])
    

def get_status(last_name: str, first_name: str):
    # Start a session to keep cookies
    with requests.Session() as session:
        url = "https://search.cpsa.ca/"
        
        # Get the initial page and cookies
        initial_req = session.get(url)
        if initial_req.status_code != 200:
            return "ERROR: Could not get initial page"
        
        # Parse initial page to get hidden form fields
        soup = BeautifulSoup(initial_req.text, 'html.parser')
        form_data = {}
        for field in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "__EVENTTARGET"]:
            element = soup.find("input", {"name": field})
            if element:
                form_data[field] = element["value"]

        # Prepare search data with hidden fields and the actual search parameters
        form_data.update({
            "ctl00$ctl16": "ctl00$ctl16|ctl00$MainContent$physicianSearchView$btnSearch",
            "ctl00$MainContent$physicianSearchView$txtFirstName": first_name,
            "ctl00$MainContent$physicianSearchView$txtLastName": last_name,
            "ctl00$MainContent$physicianSearchView$btnSearch": "Search",
            "__ASYNCPOST": "true",
            # You may need to include other fields here depending on how the form is set up
        })

        # Prepare headers as seen in the previous code
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": url,
            "Referer": url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

        # Include the cookies from the initial request
        cookies = requests.utils.dict_from_cookiejar(initial_req.cookies)

        # Post the search request
        search_req = session.post(url, headers=headers, data=form_data, cookies=cookies)
        if search_req.status_code != 200:
            return "ERROR: Could not post search"

        # Parse the search results
        search_soup = BeautifulSoup(search_req.text, 'html.parser')

        return parse_results_page(search_soup, first_name, last_name)
    
# Example usage
if __name__ == "__main__":
    status = get_status("amanie", "John")
    print(status)
