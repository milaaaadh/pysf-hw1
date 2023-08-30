from datetime import datetime
import time
import pandas as pd
from pandas.errors import SettingWithCopyWarning
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import warnings

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
chrome_options = Options()
chrome_options.add_argument("--headless")
path_file = "vendors502.csv"
data = pd.read_csv(path_file)
df = pd.DataFrame(data)
check_time = datetime.now().strftime("%m/%d %H")

if f"Found_{check_time}" not in df.columns.values:
    df[f"Found_{check_time}"] = ""

for i in range(1908, 2165):
    if df["FinalShow"][i] == "not found":
        driver = webdriver.Chrome(
            service=Service(r"C:\Users\mehdi.habibi\PycharmProjects\QA\ShowVendors\chromedriver.exe"),
            options=chrome_options)
        driver.implicitly_wait(5)
        res = df['Name'][i]
        driver.get(f"https://snappfood.ir/search?query={res}&page=0")
        a = driver.find_elements(By.CLASS_NAME, "VendorCard__VendorTitle-sc-6qaz7-5")
        if res in [i.text for i in a]:
            print(f"{res}  found")
            df[f"Found_{check_time}"][i] = "found"
        elif res not in [i.text for i in a]:
            print(f"{res} not found")
            df[f"Found_{check_time}"][i] = "not found"
        else:
            print("Error in Code")
            df[f"Found_{check_time}"][i] = "Error"

        driver.quit()

df.to_csv(rf"final_vendors{check_time}.csv")
