import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def confirm_user(word1, word2, text):
    regex = r'\b{}\b.*\b{}\b|\b{}\b.*\b{}\b'.format(word1, word2, word2, word1)
    return bool(re.search(regex, text))

# Status check for not practising
def confirm_status(text):
    return "not practising" in text.lower()

def get_user_info(firstName: str, lastName: str, licence_num=""):
    user_status = False
    browser = None

    try: 
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        browser.get("https://www.cpsbc.ca/public/registrant-directory")

        # Form filling
        adv_search = browser.find_element(By.CLASS_NAME, "option")
        actions = webdriver.ActionChains(browser)
        actions.move_to_element(adv_search).click().perform()
        

        last_name = browser.find_element(By.ID, "edit-ps-last-name")
        last_name.send_keys(lastName)

        license_num = browser.find_element(By.ID, "edit-ps-first-name")
        license_num.send_keys(firstName)

        search_btn = browser.find_element(By.CLASS_NAME, "ps-submit")
        actions = webdriver.ActionChains(browser)
        actions.move_to_element(search_btn).click().perform()

        # Delay for the website to process data
        time.sleep(1)

        # print(browser.current_url)
        assert browser.current_url == "https://www.cpsbc.ca/public/registrant-directory/search-result"

        search_res = browser.find_element(By.XPATH, "//*[@id='cpsbc-directory-form']/div/div[2]/div[2]/div[1]/div[1]/h5/a").text
        # print("Name:", search_res)
        assert True == confirm_user(lastName, firstName, search_res)

        status_check = browser.find_element(By.XPATH, "//*[@id='cpsbc-directory-form']/div/div[2]/div[2]/div[2]").text
        # print("Status:", status_check)
        assert True != confirm_status(status_check)
        user_status = True
    except:
        error = browser.find_element(By.XPATH, "//*[@id='cpsbc-directory-form']/div/div[2]/div/div/div").text.strip()
        # print("Error:", error)
        user_status = False
    finally:
        if browser: 
            browser.quit()

    if user_status == True:
        return "VERIFIED"
    else:
        return "NOT FOUND"


if __name__ == "__main__":
    print(get_user_info("Amanpreet", "Gill")) # VERIFIED
    print()
    print(get_user_info("Aalto", "Anu")) # NOT FOUND 
    print()
    print(get_user_info("Davey", "Gin")) # VERFIED
    print()
    print(get_user_info("Ian", "Gillespie")) # VERFIED
    print()
    print(get_user_info("Anthony", "Keen")) # NOT FOUND
