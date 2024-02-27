import requests
import re

def get_user_status(firstname: str, lastname: str):
    initial_api_url = f"https://member.cpsm.mb.ca/api/physicianprofile/searchresult?lastname={lastname}&firstname={firstname}&fieldofpractice=&city=&postalcode=&wheelchairaccess=&languages="
    
    try: 
        initial_response = requests.get(initial_api_url)
    except:
        return "ERROR"

    # Successfully got a res
    data = initial_response.json()

    if data.get("items"):
        item = data["items"][0]
        descriptions = item.get("descriptions")
        if descriptions:
            last_name = descriptions[0]
            first_name = descriptions[1]

            # Debug check
            # print("First Name:", first_name)
            # print("Last Name:", last_name)
        else:
            return "ERROR"

        links = item.get("links")
        if links:
            # Note user_id is not the license number
            user_id = links[0].get("parameters")

            # Debug check
            # print("ID from links:", user_id)

            final_api_url = f"https://member.cpsm.mb.ca/api/physicianprofile/practitionerinformation?id={user_id}"

            try:
                final_response = requests.get(final_api_url)
            except:
                return "ERROR"

            # Successfully received a response
            final_data = final_response.json()
            membership_class = final_data.get("membershipClass")

            # Debug check
            # print("Membership Class:", membership_class)

            return check_status(membership_class)
    else:
        return "NOT FOUND"

def check_status(memberClass: str):
    if re.search(r'Regulated Member', memberClass):
        return "VERIFIED"
    return "NOT ACTIVE"


if __name__ == "__main__":
    print(get_user_status("Emily", "Saganski"))   # VERIFIED
    print()
    print(get_user_status("Stuart", "Koensgen"))  # NOT FOUND
    print()
    print(get_user_status("Marina", "Rountree-James"))  # VERIFIED
    print()
    print(get_user_status("Kim", "Rosing"))  # VERFIED


