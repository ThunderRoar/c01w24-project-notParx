import requests, json
import re
from bs4 import BeautifulSoup

QUERY_SID = "1000608"

## Return prescriber status given last name, first name, and licence number in the College of Physicians and Surgeons of New Brunswick
def get_status(first_name: str, last_name: str, licence_number: str):
  # Set up search
  url = "https://cpsnb.alinityapp.com/Client/PublicDirectory/Registrants"

  headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://cpsnb.alinityapp.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Referer": "https://cpsnb.alinityapp.com/Client/PublicDirectory",
  }

  query_parameters = {
    "Parameter": [
      {
        "ID": "TextOptionA",
        "Value": first_name,
        "ValueLabel": "[not entered]"
      },
      {
        "ID": "TextOptionB",
        "Value": last_name,
        "ValueLabel": "[not entered]"
      },
      {
        "ID": "TextOptionC",
        "Value": licence_number,
        "ValueLabel": "[not entered]"
      }
    ]
  }

  data = {
    'queryParameters': json.dumps(query_parameters),
    'querySID': QUERY_SID
  }

  # Search prescriber
  try:
    raw_response = requests.post(url, headers=headers, data=data)
  except:
    return "ERROR"

  # Error handling
  if raw_response.status_code == 403:
    return "TOO_MANY_REQUESTS" # Triggered every ~7 consecutive searches
  elif raw_response.status_code != 200:
    return "ERROR"

  # Get prescriber's id
  res = raw_response.json()
  if res['Records']:
    record = res['Records'][0]
    if re.search(r'^' + last_name + ', ' + first_name + '\s((\w+)\s)*\(' + licence_number + '\)', record['rl']):
      pb_id = record["rg"]
  else:
    return "NOT_FOUND"

  # Search status
  try:
    raw_response = requests.get("https://cpsnb.alinityapp.com/Client/PublicDirectory/Registrant/" + pb_id)
  except:
    return "ERROR"

  res = raw_response.text

  # Parse status
  soup = BeautifulSoup(res, 'html.parser')
  script_tag = soup.find('script', id='detailtemplate')
  info_soup = BeautifulSoup(script_tag.string, 'html.parser')
  h5_elements = info_soup.find_all('h5')
  for h5 in h5_elements:
      if "Current Registration" in h5.get_text():
          # Ensure "Current Registration" is not hidden
          if not any(parent.get('class') and re.match(r'^\[\[_(\w+)_\]\]', parent.get('class')[0]) for parent in h5.parents):
              return "VERIFIED"

  return "INVALID" # Found but not currently registered

if __name__ == "__main__":
  # Sanity tests
  print(get_status("Samantha", "Ables", "11355")) # VERIFIED
  print(get_status("Nizar", "Abdel Samad", "4156")) # VERIFIED
  print(get_status("Eslam", "Abdul", "5961")) # NOT_FOUND
