import os
import time
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup

def load_more_articles(driver, button_class, click_count=75):
    for i in range(click_count):
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, button_class)
            driver.execute_script("arguments[0].click();", load_more_button)  # Using JS to bypass click interception
            time.sleep(2)  # Wait for articles to load
            print(f"Clicked {i + 1} times")
        except NoSuchElementException:
            print("Load more button not found.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

def get_article_links(url, button_class, click_count=75):
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.ID, "didomi-notice-agree-button").click()
    time.sleep(3)

    load_more_articles(driver, button_class, click_count)
    html = driver.page_source
    driver.quit()

    # Use BeautifulSoup to parse the final HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Example: Find all article links on the page
    article_links = soup.find_all('a', class_='stretched-link')
    list_links = []
    for link in article_links:
        end_link = link.get('href')
        full_link = f"https://www.rtbf.be{end_link}"
        list_links.append(full_link)
    
    return list_links

def scrape_article_data(article_url):
    response = requests.get(article_url, headers={"User-agent": "mathieu", "Authorization": "mathieu"})
    if response.status_code != 200:
        print(f"Failed to fetch {article_url}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('h1', {'data-testid': 'title'})
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    content_div = soup.find('div', {'data-elb': 'engagement'})
    paragraphs = content_div.find_all('p') if content_div else []
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

def scrape_all_articles(article_links):
    all_articles_data = []
    for url in article_links:
        article_data = scrape_article_data(url)
        if article_data:  # Only append if data was successfully scraped
            all_articles_data.append(article_data)
    
    return all_articles_data

def save_to_json(data):
    # Generate a filename with the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"data/articles_RTBF_{current_date}.json"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write data to the JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data successfully saved to {filename}")

def run_scraping():
    article_links = get_article_links("https://www.rtbf.be/en-continu", "border-yellow-500", click_count=150)
    articles_data = scrape_all_articles(article_links)
    save_to_json(articles_data)