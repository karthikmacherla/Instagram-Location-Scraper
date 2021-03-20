from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils import *
import pandas as pd

# options = webdriver.ChromeOptions()
# options.add_argument(
#     "user-data-dir=/Users/karthikmacherla/Library/Application Support/Google/Chrome/Profile 1")

USERNAME = "insert instagram username here"
PASSWORD = "insert instagram password here"
INPUT_CSV = "insert csv with names column here"
CHROME_DRIVER_PATH = "path to chrome driver (required to run selenium)"

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH)


driver.get("https://www.instagram.com/")


# enter username field
username = WebDriverWait(driver, 20).until(
    expected_conditions.presence_of_element_located((By.NAME, "username")))

passwd = WebDriverWait(driver, 20).until(
    expected_conditions.presence_of_element_located((By.NAME, "password")))

username.clear()
username.send_keys(USERNAME)

passwd.clear()
passwd.send_keys(PASSWORD, Keys.RETURN)


# Wait for page to load and send search query
search_bar = WebDriverWait(driver, 20).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME, "XTCLo")))


inp_data = pd.read_csv(INPUT_CSV)
inp_data['Count'] = ''
inp_data['Longitude'] = ''
inp_data['Latitude'] = ''
inp_data['Website'] = ''
inp_data['Profile Pic'] = ''
inp_data['Instagram URL'] = ''

# fetches most relevant tagged location given location name
for i, name in enumerate(inp_data['Name']):
    print(i, name)
    url = find_url(driver, search_bar, name)
    inp_data.at[i, 'Instagram URL'] = url

# fetches all other data i.e. latitude, longitude, # of posts, etc.
for i, url in enumerate(inp_data['Instagram URL']):
    if url != "":
        modified_url = url + "?__a=1"
        print(modified_url)
        info = get_json_info(driver, modified_url)
        inp_data.at[i, 'Count'] = info["count"]
        inp_data.at[i, 'Longitude'] = info['long']
        inp_data.at[i, 'Latitude'] = info['lat']
        inp_data.at[i, 'Website'] = info['website']
        inp_data.at[i, 'Profile Pic'] = info['pic']

# returns completely populated csv
inp_data.to_csv("output.csv")
