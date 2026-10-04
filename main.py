import requests
from bs4 import BeautifulSoup, FeatureNotFound
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

GS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfd2n2HPwYKDYON9NHaR1skIHZzifxPeLmQmaNV-z7Up9KCHA/viewform?usp=preview"
URL  = "https://appbrewery.github.io/Zillow-Clone/?"
GO =  True

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

driver.get(GS_URL)

response = requests.get(URL , timeout= 10)
response.raise_for_status()
soup = BeautifulSoup(response.text , "html.parser")


links = [ ]
soup_link = soup.find_all("a" , class_ = "StyledPropertyCardDataArea-anchor")
try:

        for link in soup_link:

            href = link.get("href")
            if href:
                links.append(href)

except FeatureNotFound:
 print("something went wrong bro")

price = []
soup_price = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")

for amount in soup_price:
    cost  = amount.text.split("/")[0].split(" bd")[0].strip()
    price.append(cost)

address  =  [ ]
soup_address = soup.find_all("address" ,
                             attrs= {"data-test" : "property-card-addr"})

try:

    for location in soup_address:
        clean_address = " ".join(location.text.replace("|", " ").split())
        address.append(clean_address)

except:
    print("something went wrong bruhh ! :( ")

first_count = 0
stop = len(address) - 1

while GO:
    #--------------------ENTERING THE ADDRESS ----------------------#
    address_entry = wait.until(ec.presence_of_element_located((By.XPATH , "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    place_entry = address[first_count]
    address_entry.send_keys(place_entry)

    #-------------------ENTERING THE PRICE --------------------------#
    price_entry =wait.until(ec.presence_of_element_located((By.XPATH , "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    cost_entry = price[first_count]
    price_entry.send_keys(cost_entry)


    #-------------------ENTERING THE LINK ---------------------------#

    link_entry = wait.until(ec.presence_of_element_located((By.XPATH , "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")))
    connection_entry = links[first_count]
    link_entry.send_keys(connection_entry)


    #------------------PRESSING THE SUBMIT KEY ----------------------#
    enter_key = wait.until(element_to_be_clickable((By.XPATH , "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")))
    enter_key.click()



    #------------------PRESSING THE SUMBIT ANOTHER RESPONSE ----------
    driver.find_element(By.LINK_TEXT, "Submit another response").click()

    first_count += 1

    if first_count == stop :
        GO = False
        print("THE TASK IS ALL DONE BRUH !! :)")



