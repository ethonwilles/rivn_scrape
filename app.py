import requests 
import urllib
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 


privacy_urls = []
cookies = []
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
        scrape = bs(driver.page_source, "html.parser")
        for item in scrape.find_all("a"):
            if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                
                try:
                            requests.get(item.get("href"))
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "privacy","has_priv" : True , "priv_url" : item.get("href") , "url" : url})
                            print(r.json())
                except:
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "privacy", "has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
                            print(r.json())
                privacy_checker = True
            
        # for item in scrape.find_all("a"):
        #     words = item.get_text().split()
        #     for word in words:
        #         if word.lower() == "cookie":
        #             r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie", "url" : url, "html": f'{item.find_parent("div")}', "has_cook" : True})
        #             print(r.json()) r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie", "url" : url, "html": f"{item}", "has_cook" : True})
        #             checker = True
        for item in scrape.find_all("div"):
            
            for word in item.get_attribute_list('id'):
                try:
                    list_of_words = word.split("-")
                    for word_item in list_of_words:
                        if word_item.lower() == "cookie" or word_item.lower() == "cookiebanner" or word_item.lower() == "consent":
                            checker = True
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                            print(r.json())
                            
                            
                            local_check = True
                except:
                    1+1
            for word in item.get_attribute_list("class"):
                
                try:
                    list_of_words = word.split("-")
                    for w in list_of_words:
                        if word == "cc" or word == "cookie":
                            checker = True
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                            print(r.json())
                            
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
            print(r.text)
        driver.quit()
for url in urls: 
    privacy_checker = False
    checker = False
    try:
        print(requests.get(f"https://{url}").status_code)
        if requests.get(f"https://{url}").status_code < 400:
            try:
                scrape = bs(requests.get(f"https://{url}").content, "html.parser")
                for item in scrape.find_all("a"):
                    if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                        try:
                            requests.get(item.get("href"))
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "privacy", "has_priv" : True , "priv_url" : item.get("href") , "url" : url})
                            print(r.json())
                        except:
                            r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "privacy","has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
                            print(r.json())
                        privacy_checker = True
                for item in scrape.find_all("div"):
            
                    for word in item.get_attribute_list('id'):
                        try:
                            list_of_words = word.split("-")
                            for word_item in list_of_words:
                                if word_item.lower() == "cookie" or word_item.lower() == "cookiebanner" or word_item.lower() == "consent":
                                    checker = True
                                    r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                                    print(r.json())
                                    
                                    
                                    local_check = True
                        except:
                            1+1
                    for word in item.get_attribute_list("class"):
                        
                        try:
                            list_of_words = word.split("-")
                            for w in list_of_words:
                                if word == "cc" or word == "cookie":
                                    checker = True
                                    r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "cookie","has_cook" : True , "html" : f"{item}" , "url" : url})
                                    print(r.json())
                                    
                        except:
                            1+1
                if checker:
                    print("Cookie Found!")
                else:
                    r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie boolean", "url" : url, "has_cook" : False})
                    print(r.json())
                if privacy_checker:
                    print("privacy Found!")
                else:
                    r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : 'privacy boolean', "url" : url, "has_priv" : False})
                    print(r.json())
                
            except Exception as e:
                print(e)
        else:
            chromedriver(url)
    except:
        chromedriver(url)
    


 

