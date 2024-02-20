from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def initialize_webdriver():
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)

def submit_search_form(driver, surname):
    driver.get("https://www.cps.sk.ca/imis/CPSS/physician_summary/search/search_results.aspx")
    surname_input = driver.find_element(By.ID, 'ctl01_HomePageSearch_Search_TB_Search')
    surname_input.send_keys(surname)
    search_button = driver.find_element(By.ID, 'ctl01_HomePageSearch_Search_Btn_Search')
    search_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ng-table-responsive')))
