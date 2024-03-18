from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_status(first_name:str, last_name: str, number: str):
    while len(number) < 5:
        number = "0" + number
    url = 'https://www.cmq.org/fr/bottin/medecins?number=' + number + '&lastname=' + last_name + "&firstname=" + first_name

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        options.add_argument("window-size=1920,1080")
        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(options=options, service=service)
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
    finally:
        driver.quit()

if __name__ == "__main__":
    print(get_status(first_name = "Ali", last_name='Lopez Sarmiento', number='4426')) # Verified
    print(get_status(first_name = "Alo", last_name='Lopez Sarmiento', number='4426')) # Not found
    print(get_status(first_name = "Alexia", last_name='Lam', number='96332')) # Not found
    print(get_status(first_name = "Annie", last_name='Li', number='15332')) # Verified
    print(get_status(first_name = "B", last_name='Li', number='15332')) # Not found
    #  print(get_status(first_name = "Alexia", last_name='Auger Labadie', number='27959')) # Not Found
    #  print(get_status(first_name = "Alexia", last_name='Li', number='15333')) # Not Found
    print(get_status(first_name = "", last_name='Shalaby', number='77587')) # Inactive