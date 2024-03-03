from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def getStatus(last_name: str, number: str):
    url = 'https://www.cmq.org/fr/bottin/medecins?number=' + number + '&lastname=' + last_name

    try:
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        button = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/main/article/section[2]/div/div/table/tbody')
        button.click()

        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='c-modal']")))

        data_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/ul/li[4]/div[2]')
        data = data_element.text

        if (data == 'Inscrit - Actif'): 
            return "VERIFIED"
        else:
            return "INACTIVE"

    except (TimeoutException, NoSuchElementException):
            return "NOT FOUND"

if __name__ == "__main__":
     print(getStatus(last_name='Lam', number='96332')) # Verified
     print(getStatus(last_name='Li', number='15332')) # Verified
     print(getStatus(last_name='Auger Labadie', number='27959')) # Not Found
     print(getStatus(last_name='Li', number='15333')) # Not Found
     print(getStatus(last_name='Shalaby', number='77587')) # Inactive