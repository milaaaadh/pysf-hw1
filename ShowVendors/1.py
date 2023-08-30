from datetime import datetime
import time
import pandas as pd
from pandas.errors import SettingWithCopyWarning
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import warnings


def wait_page(timeout):
    for i in range(timeout):
        try:
            assert driver.execute_script("return document.readyState") == "complete"
            return
        except:
            time.sleep(0.5)


warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

chrome_options = Options()
chrome_options.add_argument("--headless")
path_file = "vendors502.csv"
data = pd.read_csv(path_file)
df = pd.DataFrame(data)
check_time = datetime.now().strftime("%Y-%m-%d %H")

driver = webdriver.Chrome(service=Service(r"C:\Users\mehdi.habibi\PycharmProjects\QA\ShowVendors\chromedriver.exe"))
driver.implicitly_wait(5)
driver.get("https://newbackend.zoodfood.com/auth/login")
driver.find_element(By.NAME, "_username").send_keys("09011358315")
driver.find_element(By.NAME, "_password").send_keys("743100",Keys.RETURN)
driver.find_element(By.NAME, "_two_factor_code").send_keys("212161",Keys.RETURN)
driver.get("https://newbackend.zoodfood.com/vendor/")
wait_page(7)
for i in range(2013,1911,-1):
    if df["Found_2023-08-22 14"][i] == "not found":
        vendor_id = str(df["Vendor Id"][i])
        print(vendor_id)
        driver.get(f"https://newbackend.zoodfood.com/vendor/{vendor_id}/edit")
        wait_page(7)

        try:
            driver.find_element(By.ID, "vendor-button").click()
            wait_page(7)
            driver.find_element(By.CLASS_NAME, "kk_vendor_submit").click()
            wait_page(7)
            df["UpdateProfile"][i] == "True"


        except:
            driver.get(f"https://newbackend.zoodfood.com/vendor/{vendor_id}/edit")
            wait_page(7)
            try:
                driver.find_element(By.CLASS_NAME, "kk_vendor_submit").click()
                wait_page(7)
                df["UpdateProfile"][i] == "True"
            except:
                driver.find_element(By.ID, "vendor-button").click()
                wait_page(7)
                driver.find_element(By.CLASS_NAME, "kk_vendor_submit").click()
                wait_page(7)
                df["UpdateProfile"][i] == "True"


df.to_csv(r"vendors506.csv")
