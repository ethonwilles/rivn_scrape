from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def chromedriver(url):
        privacy_checker = False
        checker = False
        driver = webdriver.Chrome()
        driver.get(f"https://{url}")
        scrape = bs(driver.page_source, "html.parser")
        # for item in scrape.find_all("a"):
        #     if item.get_text().lower() == "privacy policy" or item.get_text().lower() == "privacy" or item.get_text().lower() == "privacy and cookies":
                
        #         try:
        #                     requests.get(item.get("href"))
        #                     r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "privacy","has_priv" : True , "priv_url" : item.get("href") , "url" : url})
        #                     print(r.json())
        #         except:
        #                     r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice": "privacy", "has_priv" : True , "priv_url" : f"https://{url}{item.get('href')}" , "url" : url})
        #                     print(r.json())
        #         privacy_checker = True
            
        # for item in scrape.find_all("a"):
        #     words = item.get_text().split()
        #     for word in words:
        #         if word.lower() == "cookie":
        #             r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie", "url" : url, "html": f'{item.find_parent("div")}', "has_cook" : True})
        #             print(r.json())
        #             checker = True
        for item in scrape.find_all("div"):
                    for word in item.get_attribute_list('id'):
                        try:
                            list_of_words = word.split("-")
                            for word_item in list_of_words:
                                if word_item.lower() == "cookie" or word_item.lower() == "cookiebanner":
                                    # r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie", "url" : url, "html": f"{item}", "has_cook" : True})
                                    # print(r.json())
                                    print(item)
                                    checker = True

                        except:
                            1+1
        # if checker:
        #     print("Cookie Found!")
        # else:
        #     r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : "cookie boolean", "url" : url, "has_cook" : False})
        #     print("status code from db ",r.status_code)
        # if privacy_checker:
        #     print("privacy Found!")
        # else:
        #     r = requests.post("https://admin-dev.rivn.com/audit-results-post", json={"choice" : 'privacy boolean', "url" : url, "has_priv" : False})
        #     print("status code from db ",r.status_code)

chromedriver("rubiconproject.com")