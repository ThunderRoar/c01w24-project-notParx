import requests
from bs4 import BeautifulSoup

api_url = "https://search.cpsa.ca/"

headers = {
    'Content-Type': 'application/json',
}

payload = {
    'ctl00$ctl16': 'ctl00$ctl16|ctl00$MainContent$physicianSearchView$btnSearch',
    '__EVENTTARGET':'ctl00$MainContent$physicianSearchView$btnSearch',
    'ctl00$MainContent$physicianSearchView$txtFirstName': 'John',
    'ctl00$MainContent$physicianSearchView$txtLastName': '',
    'ctl00$MainContent$physicianSearchView$txtCity': '',
    'ctl00$MainContent$physicianSearchView$txtPostalCode': '',
    'ctl00$MainContent$physicianSearchView$rblPractice': '',
    'ctl00$MainContent$physicianSearchView$ddDiscipline': '',
    'ctl00$MainContent$physicianSearchView$rblGender': '',
    'ctl00$MainContent$physicianSearchView$ddApprovals': '',
    'ctl00$MainContent$physicianSearchView$ddLanguage': '',
    '__ASYNCPOST': 'true',
}

response = requests.post(api_url, headers=headers, data=payload)

soup = BeautifulSoup(response.text, 'html.parser')


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    results_section = soup.find('div', class_='resultsSection')
    results_section_html = str(results_section)
    print(results_section_html)
else:
    print(f"Failed to fetch data from the API. Status code: {response.status_code}")
