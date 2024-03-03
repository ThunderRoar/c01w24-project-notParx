import requests
from bs4 import BeautifulSoup

def get_search_results(license_number: str, first_name: str, last_name: str):
    search_url = "https://imis.cpsnl.ca/WEB/CPSNL/PhysicianSearch/Physician_Search_New.aspx"

    with requests.Session() as session:
        # Get the initial page to setup cookies and possibly get viewstate
        initial_response = session.get(search_url)
        if initial_response.status_code != 200:
            return "ERROR: Could not get initial page"
        
        # Parse initial response to obtain VIEWSTATE and other dynamic fields, if present
        # Not all sites require this; you'll need to inspect the site to see if it's necessary
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        viewstate = soup.find(id="__VIEWSTATE")["value"] if soup.find(id="__VIEWSTATE") else ""
        print(viewstate)
        # Construct the payload for the POST request with the search parameters
        payload = {
            "__VIEWSTATE": viewstate,  # Uncomment and adjust if necessary
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input0$TextBox1": license_number,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input1$TextBox1": first_name,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input2$TextBox1": last_name,
            "__ASYNCPOST": "true",
            # ... include all other required fields from your payload example
        }

        # Prepare headers as needed
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            "Referer": search_url,
        }

        # Make the POST request with the payload and headers
        # Cookies are automatically handled by the session
        search_response = session.post(search_url, data=payload, headers=headers)
        if search_response.status_code != 200:
            return "ERROR: Could not perform search"

        # Parse the search results page
        search_soup = BeautifulSoup(search_response.text, 'html.parser')
        return search_soup

# Example usage
if __name__ == "__main__":
    license_number = "F 01923"  # Replace with the actual license number to search
    first_name = "John"  # Replace with the actual first name to search
    last_name = "Abbatt"  # Replace with the actual last name to search
    results_soup = get_search_results(license_number, first_name, last_name)
    if isinstance(results_soup, BeautifulSoup):
        print(results_soup.prettify())  # For debugging, remove or replace with actual data extraction logic
    else:
        print(results_soup)  # In case of errors, this prints the error message
