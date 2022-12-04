from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys

website="https://propertysearch.altusgroup.com/Property/Search/All/All/For-Sale-and-To-Let/All/All/All/All/recently-added-first/All"
path="C:\Developer\chromedriver.exe"


options = webdriver.ChromeOptions()

# options.headless=True 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
s=Service(executable_path=path)
driver = webdriver.Chrome(service=s,options=options)
driver.get(website)

outcome=int(driver.find_element(by="xpath",value='//p[@class="search-count title6 d-block"]').text.split()[0])

box=12


element=driver.find_element(by="xpath",value="//html//body")
element.send_keys(Keys.END)
time.sleep(2)
element.send_keys(Keys.PAGE_UP)
element.send_keys(Keys.UP)


# Loading page to get all the available property

while True:
    if box<outcome:
        loadmore_button=driver.find_element(by="xpath",value='//button[contains(text(),"Load")]').click()
        time.sleep(2)
        box+=12
        outcome=int(driver.find_element(by="xpath",value='//p[@class="search-count title6 d-block"]').text.split()[0])
        element.send_keys(Keys.END)
        #time for the page to refresh
        time.sleep(1)
        #for scrolling (the click function was not working without scrolling)
        element.send_keys(Keys.PAGE_UP)
        element.send_keys(Keys.UP)
        time.sleep(1)

    else:
        break


# scraping starts from here
containers=driver.find_elements(by="xpath",value='//div[@class="property-grid d-flex flex-row flex-wrap justify-content-start"]//div[@class="property-card d-block w-100"]')
#preceding-sibling example
property_status=[ container.find_element(by="xpath",value='.//p[2]//preceding::p[1]').text for container in containers]
# following-sibling example
property_address=[ container.find_element(by="xpath",value='.//p//following::p').text for container in containers]
# contains example
property_image=[container.find_element(by="xpath",value='.//div[contains(@style,"background")]').get_attribute("style").split('"')[1] for container in containers]
# child example
property_weblink=[ container.find_element(by="xpath",value='.//child::a').get_attribute("href") for container in containers]

my_dict={
    "property_status":property_status,
    "property_address":property_address,
    "property_image":property_image,
    "property_weblink":property_weblink
}
file=pd.DataFrame(my_dict)
file.to_csv("nimbus_maps.csv")    #extract scraped data in csv file
time.sleep(5)
driver.quit()
