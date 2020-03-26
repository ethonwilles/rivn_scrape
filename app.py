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
    sleep(7)
    try:
        urls = requests.get("http://localhost:5000/audit-results-urls").json()['results']
        checker = False
    except:
        checker = True


def chromedriver(url):
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://{url}")
        scrape = bs(driver.page_source, "html.parser")
        for item in scrape.find_all("a"):
            if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                
                try:
                            requests.get(item.get("href"))
                            r = requests.post("http://localhost:5000/audit-results-post", json={"has_priv" : True , "priv_url" : item.get("href") , "url" : url})
                            print(r.json())
                except:
                            r = requests.post("http://localhost:5000/audit-results-post", json={"has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
                            print(r.json())

for url in urls: 
    try:
        print(requests.get(f"https://{url}").status_code)
        if requests.get(f"https://{url}").status_code < 400:
            try:
                scrape = bs(requests.get(f"https://{url}").content, "html.parser")
                for item in scrape.find_all("a"):
                    if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                        try:
                            requests.get(item.get("href"))
                            r = requests.post("http://localhost:5000/audit-results-post", json={"has_priv" : True , "priv_url" : item.get("href") , "url" : url})
                            print(r.json())
                        except:
                            r = requests.post("http://localhost:5000/audit-results-post", json={"has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
                            print(r.json())
                
            except Exception as e:
                print(e)
        else:
            chromedriver(url)
    except:
        chromedriver(url)
    
print(privacy_urls)

 

