import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 




checker = True
while checker:
    sleep(7)
    try:
        urls = requests.get("http://10.0.0.214:5000/audit-results-urls").json()['results']
        checker = False
    except:
        checker = True

for url in urls:
    checker = False
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://{url}")
    scrape = bs(driver.page_source, "html.parser")

    for item in scrape.find_all("a"):
        words = item.get_text().split()
        for word in words:
            if word.lower() == "cookie":
                print(item.find_parent('div'))
                checker = True
    
    for item in scrape.find_all("div"):
        for word in item.get_attribute_list('id'):
            try:
                list_of_words = word.split("-")
                for word_item in list_of_words:
                    if word_item.lower() == "cookie":
                        print(item)
                        checker = True

            except:
                1+1
    if checker:
        print("Found a Cookie!")
    else:
        print("Did not find a cookie.")

    # scrape = bs(requests.get('https://rivn.com').content, "html.parser")
    # for item in scrape.find_all('a'):
    #     words = item.get_text().split()
    #     for word in words:
    #         if word.lower() == "cookie":
    #             print(item)