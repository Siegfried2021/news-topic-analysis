from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import json
import os

def load_more_articles(driver, button_class, click_count=75):
    """
    Clicks the "Load more articles" button a specified number of times.
    
    Parameters:
    driver (webdriver): The Selenium WebDriver instance.
    button_class (str): The class name of the "Load more" button.
    click_count (int): The number of times to click the button.
    """
    for i in range(click_count):
        try:
            # Find the "Load more articles" button
            load_more_button = driver.find_element(By.CLASS_NAME, button_class)
            load_more_button.click()
            time.sleep(2)  # Wait for new articles to load
            print(f"Clicked {i+1} times")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error clicking the button: {e}")
            break  # Break if the button is no longer available or an error occurs

def get_article_links(url, button_class, click_count=75):
    # Initialize the WebDriver
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    
    # Open the base page
    driver.get(url)
    time.sleep(3)  # Wait for the page to load fully
    driver.find_element(By.ID, "didomi-notice-agree-button").click()
    time.sleep(3)

    # Click the "Load more articles" button multiple times
    load_more_articles(driver, button_class, click_count)

    # Get the full page source after all articles are loaded
    html = driver.page_source
    driver.quit()  # Close the driver

    # Use BeautifulSoup to parse the final HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Example: Find all article links on the page
    article_links = soup.find_all('a', class_='stretched-link')
    list_links = []
    for link in article_links:
        end_link = link.get('href')  # Print or process each article link
        full_link = f"https://www.rtbf.be{end_link}"
        list_links.append(full_link)
    
    return list_links

def scrape_all_articles(article_links):
    """
    Scrapes data from all article URLs.
    
    Parameters:
    article_urls (list): A list of URLs to scrape.
    
    Returns:
    list: A list of dictionaries containing scraped data for each article.
    """
    all_articles_data = []

    for url in article_links:
        article_data = scrape_article_data(url)
        if article_data:  # Only append if data was successfully scraped
            all_articles_data.append(article_data)
    
    return all_articles_data

def scrape_article_data(article_url):
    """
    Scrapes the title and content from an article page.
    
    Parameters:
    article_url (str): The URL of the article to scrape.
    
    Returns:
    dict: A dictionary containing the date, title, and content of the article.
    """
    # Make a request to the article URL
    response = requests.get(article_url, headers={"User-agent": "mathieu", "Authorization": "mathieu"})
    if response.status_code != 200:
        print(f"Failed to fetch {article_url}")
        return None
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get the title
    title_tag = soup.find('h1', {'data-testid': 'title'})
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    
    # Get all paragraph elements within the target div
    content_div = soup.find('div', {'data-elb': 'engagement'})
    paragraphs = content_div.find_all('p') if content_div else []
    
    # Concatenate all paragraphs into a single string for the content
    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Structure the data in a dictionary
    article_data = {
        'date': current_date,
        'title': title,
        'content': content
    }
    
    return article_data

def save_to_json(data, filename="data/articles_RTBF.json"):
    """
    Saves the data to a JSON file at a relative path.
    
    Parameters:
    data (list): The list of dictionaries containing article data.
    filename (str): The relative path to the JSON file.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write data to the JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data successfully saved to {filename}")

# Usage example
article_links = get_article_links("https://www.rtbf.be/en-continu", "border-yellow-500", click_count=100)
all_articles_data = scrape_all_articles(article_links)
save_to_json(all_articles_data, "data/articles_RTBF.json")