from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
from time import sleep

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

check_spot = requests.get("https://admin-dev.rivn.com/new-placeholder").json()["num"]

checker = True
while checker:
    sleep(8)
    try:
       
        urls = requests.get("https://admin-dev.rivn.com/audit-results-urls").json()['results']
        checker = False
    except:
        checker = True

def chromedriver(url):
        privacy_checker = False
        checker = False
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://{url}")
        sleep(2)
        scrape = bs(driver.page_source, "html.parser")
        for item in scrape.find_all("a"):
            if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                
                try:
                            requests.get(item.get("href"))
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "privacy","has_priv" : True , "priv_url" : item.get("href") , "url" : url})
                            print(r.text)
                except:
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "privacy", "has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
                            print(r.text)
                privacy_checker = True
            
        
        local_check = False
        
        for item in scrape.find_all("div"):
            
            for word in item.get_attribute_list("class"):
                if checker == False:
                    try:
                        list_of_words = word.split("-")
                        for w in list_of_words:
                            if w == "cc" or w == "cookie":
                                r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                                print(r.text)
                                
                                checker = True
                    except:
                        1+1
            for word in item.get_attribute_list('id'):
                if checker == False:
                    try:
                        list_of_words = word.split("-")
                        for word_item in list_of_words:
                            if word_item.lower() == "cookie" or word_item.lower() == "cookiebanner" or word_item.lower() == "consent":
                                r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                                print(r.text)
                                
                                checker = True
                                local_check = True
                    except:
                        1+1
            

            
                
        
        if checker:
            print("Cookie Found!")
        else:
            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie boolean", "url" : url, "has_cook" : False})
            print(r.text)
        if privacy_checker:
            print("privacy Found!")
        else:
            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : 'privacy boolean', "url" : url, "has_priv" : False})
            print("status code from db ",r.status_code)

        

for url in urls:
    chromedriver(url)
    check_spot += 1
    r = requests.post("https://admin-dev.rivn.com/new-placeholder" ,json={'number' : check_spot})
    