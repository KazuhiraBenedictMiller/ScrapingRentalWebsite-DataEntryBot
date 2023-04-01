from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

#Find a Link for a Real Estate Rental Website
QueryLink = 'https://www.immobiliare.it/affitto-case/genova/?criterio=rilevanza'
#Create a Google Form and Share by Link
GoogleForm = YOUR_GOOGLE_FORM_LINK #'https://docs.google.com/forms/d/e/1FAIpQLSeQMsQ0fUBZMV9s9wqzZvlo2tqpFrA1iwnyINIEU8fRENZopQ/viewform?usp=sf_link'

#Your HTTP Headers
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

Response = requests.get(url = QueryLink, headers = Headers)
Soup = BeautifulSoup(Response.text, "html.parser")
nPages = Soup.find_all("div", class_ = "in-pagination__item hideOnMobile in-pagination__item--disabled")[-1].text
MaxPages = 5

# Creating the Dict for all Infos
Infos = []

#Scraping Infos from the Website
x = 1
while x <= int(nPages) and x <= MaxPages:
    NewLink = QueryLink + "&pag=" + str(x)
    Response = requests.get(url = NewLink, headers = Headers)
    Soup = BeautifulSoup(Response.text, "html.parser")
    AllAs = Soup.find_all("a", class_ = "in-card__title")
    AllLis = Soup.find_all("li", class_ = "nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main")

    for y in range(len(AllAs)):
        Infos.append({"Link":AllAs[y]["href"],
                      "Address": AllAs[y].text,
                      "Price": AllLis[y].text
                     })
    x += 1

chrome_driver_path = "./chromedriver.exe"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

Driver = webdriver.Chrome(executable_path = chrome_driver_path, options = chrome_options)
Driver.implicitly_wait(5)

Driver.get(GoogleForm)

#Sending the Informations to the Form with Selenium (XPaths need to be Refreshed everytime, since it pop ups if we want to continue sending indo through the Form.)
for x in Infos:
    Address = Driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    Link = Driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    Price = Driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    Submit = Driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    Address.send_keys(x["Address"])
    Link.send_keys(x["Link"])
    Price.send_keys(x["Price"])
    time.sleep(1)
    Submit.click()
    time.sleep(2)
    Next = Driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    Next.click()

Driver.quit()

#You can now go to your Google Forms -> My Forms -> Your Compiled Form with Scraped Data that you've created at the Start -> Click on "Answers" -> Connect to Google Sheets.
#Enjoy your Spreadsheet compiled with Scraped Data :)
