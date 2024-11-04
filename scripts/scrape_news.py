from selenium.webdriver.chrome.service import Service
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

driver = initialize_web_driver('https://www.rtbf.be/en-continu')


# time.sleep(10)

# driver.quit()

# rejoindre la page source
# s'occuper éventuellement des cookies
# cliquer sur chaque titre while True
# cliquer sur charger 20 articles supplémentaires (100 fois)

# sur la page, scraper le titre, scraper le texte de l'article (peut être en plusieurs morceaux)