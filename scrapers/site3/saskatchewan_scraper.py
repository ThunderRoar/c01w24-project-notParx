from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

def initialize_webdriver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    return webdriver.Chrome(options=options, service=service)

def submit_search_form(driver, surname):
    driver.get("https://www.cps.sk.ca/imis/CPSS/physician_summary/search/search_results.aspx")
    surname_input = driver.find_element(By.ID, 'ctl01_HomePageSearch_Search_TB_Search')
    surname_input.send_keys(surname)
    search_button = driver.find_element(By.ID, 'ctl01_HomePageSearch_Search_Btn_Search')
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(search_button).click().perform()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ng-table-responsive')))


def scrape_table_data(driver):
    table = driver.find_element(By.CSS_SELECTOR, '.ng-table-responsive')
    rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
    all_rows_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = {
            'LastName': cells[0].text,
            'FirstName': cells[1].text,
            'MiddleName': cells[2].text,
            'City': cells[3].text,
            'Province': cells[4].text,
            'Country': cells[5].text,
            'Language': cells[6].text,
            'PostalCode': cells[7].text,
            'Phone': cells[8].text,
            'Fax': cells[9].text,
            'ProfileLink': cells[10].find_element(By.TAG_NAME, 'a').get_attribute('href')
        }
        all_rows_data.append(row_data)
    return all_rows_data

def check_status_on_register(driver, profile_url):
    driver.get(profile_url)
    try:
        wait = WebDriverWait(driver, 10)
        status_present = EC.presence_of_element_located(
            (By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpciNewSummaryDisplayCommon_ciNewSummaryDisplayCommon_Status'))
        wait.until(status_present)
        status_element = driver.find_element(By.ID, 'ctl01_TemplateBody_WebPartManager1_gwpciNewSummaryDisplayCommon_ciNewSummaryDisplayCommon_Status')
        if status_element.text == "On the Register" :
            return "VERIFIED"
        return "INACTIVE"
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
        print("Timed out waiting for the status element to load")
        return "NOT FOUND"

# Get status for person in table with first and last name
# Search parameter is 'Last Name', but we need 'First Name' to verify a specific person
def getStatus(firstName: str, lastName: str):
    try: 
        driver = initialize_webdriver()
        submit_search_form(driver, lastName)
        doctors_data = scrape_table_data(driver)

        status = "NOT FOUND"
        for doctor in doctors_data:
            if doctor['FirstName'] == firstName and doctor['LastName'] == lastName:
                status = check_status_on_register(driver, doctor['ProfileLink'])
                break
        return status
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
        return "NOT FOUND"
    finally:
        driver.quit()

def main():
    driver = initialize_webdriver()
    try:
        submit_search_form(driver, 'Shreya')
        doctors_data = scrape_table_data(driver)
        for doctor in doctors_data:
            if check_status_on_register(driver, doctor['ProfileLink']) == "VERIFIED":
                print(f"{doctor['FirstName']} {doctor['LastName']} is on the register")
            else:
                print(f"{doctor['FirstName']} {doctor['LastName']} is not on the register")
    finally:
        driver.quit()

if __name__ == "__main__":
    print(getStatus('Shreya', 'Moodley')) # INACTIVE
    print(getStatus('Brittni', 'Webster')) # VERIFIED
    print(getStatus('abc123', 'abc123')) # NOT FOUND
    main()