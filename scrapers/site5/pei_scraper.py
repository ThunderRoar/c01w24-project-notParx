import requests, json
import re

QUERY_SID = "1000608"

## Return prescriber status given last name, first name, and licence number in the College of Physicians and Surgeons of Prince Edward Island
def get_status(first_name: str, last_name: str, licence_number: str):
  # Set up search
  url = "https://cpspei.alinityapp.com/client/PublicDirectory/Registrants"

  headers = {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "Origin": "https://cpspei.alinityapp.com",
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
      "Referer": "https://cpspei.alinityapp.com/client/publicdirectory",
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
        "Value": remove_prec_alph(licence_number),
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
    return "TOO_MANY_REQUESTS" # Triggered every ~8 consecutive searches
  elif raw_response.status_code != 200:
    return "ERROR"

  # Check if listed
  res = json.loads(raw_response.text)
  if res['Records']:
    record = res['Records'][0]
    if re.search(r'^' + last_name + ', ' + first_name + '\s((\w+)\s)*\(' + licence_number + '\)', record['rl']):
      return "VERIFIED"

  return "NOT_FOUND"

## Helper function: Remove preceding alphabets of a licence number if present.
#  Note: Some licence numbers have preceding alphabets but the search engine only accepts numerical values.
def remove_prec_alph(licence_number: str):
  match = re.search(r'[A-Za-z]*(\d+)', licence_number)
  if match:
      return match.group(1)
  else:
      return licence_number

if __name__ == "__main__":
  # Sanity tests
  print(get_status("Walid", "Abdelghaffar", "T8408")) # VERIFIED
  print(get_status("Jayani", "Abeysekera", "VC8086")) # VERIFIED
  print(get_status("Lenley", "Adams", "7016")) # VERIFIED
  print(get_status("Victoria", "Ziola", "8187")) # NOT_FOUND
