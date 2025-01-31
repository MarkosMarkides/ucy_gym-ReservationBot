import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from datetime import datetime, timedelta  # For dynamic date and time
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={os.getenv('CHROME_USER_DATA_DIR')}")
chrome_options.binary_location = os.getenv("CHROME_BINARY_LOCATION")

driver = webdriver.Chrome(options=chrome_options)
url = os.getenv("GYM_URL")
driver.get(url)

try:
    id = 'tpe'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))
    element.click()

    time.sleep(2)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="doing"]/b/font/b/font/div/article/button[1]/a')))
    element.click()

    # Ensure that login is complete
    time.sleep(10)

    cookies = driver.get_cookies()
    session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

    # Convert cookies to the correct format
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    reservation_url = os.getenv("RESERVATION_URL")

    headers = {
        'Host': 'applications2.ucy.ac.cy',
        'Cookie': cookie_string,  
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://applications2.ucy.ac.cy',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryTB670PeCHazqAW42',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://applications2.ucy.ac.cy/sportscenter/SPORTSCENTER.online_reservations_gym_pck2.insert_reservation2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i',
        'Connection': 'keep-alive'
    }

    today = datetime.now().strftime("%d/%m/%Y")
    reservation_date = (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")  # 5 days from now
    
    start_time = "14:45"
    end_time = "16:15"

    if today.weekday() == 0:
        start_time = "12:15"
        end_time = "13:45"

    form_data = (
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_system_id\"\r\n\r\n"
        "24573\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_class_code\"\r\n\r\n"
        "41\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_sttime\"\r\n\r\n"
        f"{start_time}\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_entime\"\r\n\r\n"
        f"{end_time}\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_cost\"\r\n\r\n"
        ".00\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_reservation_date\"\r\n\r\n"
        f"{reservation_date}\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_skopos_list\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_skopos\"\r\n\r\n"
        "GYM\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_persons\"\r\n\r\n"
        "1\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_sport\"\r\n\r\n"
        "6\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_reservation_type\"\r\n\r\n"
        "multible_independent\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42\r\n"
        "Content-Disposition: form-data; name=\"p_lang\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryTB670PeCHazqAW42--"
    )

    response = requests.post(reservation_url, headers=headers, data=form_data)

    if response.status_code == 200:
        print("Reservation submitted successfully!")
        print(response.text)
    else:
        print(f"Failed to submit reservation! Status code: {response.status_code}")
        print(response.text) 

except TimeoutException:
    print("TimeoutException!!!")
finally:
    # Close the Selenium browser
    driver.quit()
