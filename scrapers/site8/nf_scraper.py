import requests
from bs4 import BeautifulSoup

def is_physician_practicing(soup):
    """
    Determines the practicing status of a physician from the parsed HTML content.

    Parameters:
    - soup: BeautifulSoup object containing the parsed HTML content.

    Returns:
    - "Practicing" if the physician is practicing.
    - "Non-Practicing"" if the physician is non-practicing.
    - None if the status cannot be determined.
    """
    # Iterate through each row in the table body
    for row in soup.find_all('tr', class_='rgRow'):
        # Extract all cells from the row
        cells = row.find_all('td')
        # Check if the status is present in the expected cell
        status_cell = cells[4] if len(cells) > 4 else None
        if status_cell:
            status = status_cell.get_text(strip=True)
            # Return False if 'Non-Practicing', True if 'Practicing'
            if "Non-Practicing" in status:
                return "INACTIVE"
            elif "Practicing" in status:
                return "VERIFIED"
    # Return None if no conclusive status is found
    return None

def perform_search(license_number, first_name, last_name):
    """
    Performs a search on the CPSNL website with the given license number, 
    first name, and last name, and returns the practicing status.

    Parameters:
    - license_number: The physician's license number.
    - first_name: The physician's first name.
    - last_name: The physician's last name.

    Returns:
    - The practicing status of the physician if the search is successful.
    - An error message if the search fails.
    """
    # The URL of the search page
    initial_url = "https://imis.cpsnl.ca/WEB/CPSNL/PhysicianSearch/Physician_Search_New.aspx"
    
    # Create a persistent session to handle cookies
    with requests.Session() as session:
        # Initial GET request to obtain the necessary hidden tokens
        response = session.get(initial_url)
        if response.status_code != 200:
            return "ERROR: Couldn't fetch the search page to initialize session."
        # with open("scrapers/tests/nf_get_response.txt", "w", encoding="utf-8") as file:
        #     file.write(response.text)
        # Parse the page to extract hidden form data for ASP.NET postback
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract tokens and hidden fields
        viewstate = soup.find(id="__VIEWSTATE")["value"] if soup.find(id="__VIEWSTATE") else ""
        eventvalidation = soup.find(id="__EVENTVALIDATION")["value"] if soup.find(id="__EVENTVALIDATION") else ""
        request_verification_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"] if soup.find("input", {"name": "__RequestVerificationToken"}) else ""

        # Prepare the payload with hidden fields and search parameters
        payload = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")["value"],
            "__EVENTVALIDATION": eventvalidation,
            "__RequestVerificationToken": request_verification_token,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input0$TextBox1": license_number,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input1$TextBox1": last_name,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$Input2$TextBox1": first_name,
            "ctl00$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Sheet0$SubmitButton": "Search",
            "__ASYNCPOST": "true",
        }

        # Headers for the POST request
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Referer": initial_url,
            "X-Requested-With": "XMLHttpRequest",
            "X-MicrosoftAjax": "Delta=true",
        }

        # Submit the POST request with the payload and headers
        response = session.post(initial_url, data=payload, headers=headers)
        # with open("scrapers/tests/nf_post_response_WilliamDurocher.txt", "w", encoding="utf-8") as file:
        #     file.write(response.text)
        if response.status_code == 200:
            # Parse the response and check the practicing status
            soup = BeautifulSoup(response.text, 'html.parser')
            return is_physician_practicing(soup)
        else:
            return "NOT FOUND"

# Main execution (Sanity test)
if __name__ == "__main__":
    # Replace with actual search terms
    license_num = "F 03818"
    first_name = "William"
    last_name = "Durocher"

    # Perform the search and print the result
    result = perform_search(license_num, first_name, last_name)
    print(result) # VERIFIED