import requests
from bs4 import BeautifulSoup
def check_active_membership(profile_url):
    response = requests.get(profile_url)
    if response.status_code != 200:
        print(f"Error fetching profile: {response.status_code}")
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

# Example usage
profile_url = 'https://search.cpsa.ca/PhysicianProfile?e=cf2d5b79-aad4-44b3-91e7-76cedabbf07f&i=0'
is_active = check_active_membership(profile_url)
print(f"Is the physician an active member? {is_active}")
