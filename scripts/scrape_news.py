from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def initialize_web_driver(url):
    # Specify the path to ChromeDriver using the Service object
    service = Service('/usr/local/bin/chromedriver')

    # Initialize the webdriver to automate interactions with the website to be scraped
    driver = webdriver.Chrome(service = service)

    driver.get(url)

    return driver

def click_button(selector_type, selector_name):
    try:
        button = driver.find_element(selector_type, selector_name)
        button.click()
    except Exception as e:
        print(f"Could not find or click the butto: {e}")

driver = initialize_web_driver('https://www.rtbf.be/en-continu')
click_button(By.ID, "didomi-notice-agree-button")
click_button(By.CLASS_NAME, "border-yellow-500")




# driver.quit()

# rejoindre la page source
# s'occuper éventuellement des cookies
# cliquer sur chaque titre while True
# cliquer sur charger 20 articles supplémentaires (100 fois)

# sur la page, scraper le titre, scraper le texte de l'article (peut être en plusieurs morceaux)