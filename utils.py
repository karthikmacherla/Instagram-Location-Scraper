from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import json


def find_url(driver, search_bar, query):
    """
      Finds the most relevant location corresponding to a search query
      - search_bar = element
      - query = the string
    """
    # make sure there aren't previous search results
    search_bar.clear()
    try:
        # press the clear search results button
        x_button = driver.find_element_by_class_name("aIYm8")
        x_button.click()
    except Exception:
        pass

    search_bar.send_keys(query)
    results = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "fuqBx")))

    links = results.find_elements_by_tag_name("a")

    print(f"Results: {len(links)} found")

    # get the first result i.e. the most relevant one that corresponds to a location
    res = ""
    for link in links:
        absolute_url = link.get_attribute('href')
        if absolute_url.startswith("https://www.instagram.com/explore/locations"):
            res = absolute_url
            break

    search_bar.clear()
    return res


def get_json_info(driver, url):
    driver.get(url)

    content = driver.find_element_by_tag_name('pre').text
    json_data = json.loads(content)

    json_data = json_data["graphql"]["location"]
    lat = json_data["lat"]
    long = json_data["lng"]
    website = json_data["website"]
    profile_pic_url = json_data["profile_pic_url"]
    count = json_data["edge_location_to_media"]["count"]

    return {
        "count": count,
        "lat": lat,
        "long": long,
        "website": website,
        "pic": profile_pic_url
    }
