import requests
from bs4 import BeautifulSoup
import csv
import json

# Proxy settings
proxy_host = "{proxy_host}"
proxy_port = "{proxy_port}"
proxy_username = "{proxy_username}"
proxy_password = "{proxy_password}"
proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

# Set up the session with proxies
proxies = {"http": proxy_url, "https": proxy_url}
session = requests.Session()
session.proxies = proxies

# Define headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://example.com',
    'Connection': 'keep-alive'
}

# URL of the specific product page on eBay
url = "https://www.ebay.com/itm/225614929686?_skw=HINOMI+H1+Pro+V2+Ergonomic+Office+Chair&itmmeta=01J8SBG7E8ZF0HCSKQ7PYM22VA&hash=item3487b29f16:g:l0AAAOSwNyxkhvfS&itmprp=enc%3AAQAJAAAA4HoV3kP08IDx%2BKZ9MfhVJKlHHR9BbtzNdMEOunsS6IF3IYZ9v8%2BMu3sYhHSfU0s8OXCbJWhv6VyTlfsdssHj%2F2J5asoZEBEHHcJziz46F5fH8o3YPJh7gNf0il9wcIG2co4juVQ9uDtElnjm2Ik7Ko8sWeJUygZ%2B4%2Fj0f1O21bNN4JyJWCob536XN49Y5s0T21Oekj74gU4208gRmyx6WGCTSgKrh1guOuW0wHRDTZ6ObCPCB4cBkckoXriVnROReZMexMgUBbrQhbpLeamBxjEpMK2JJzDWEOoNBe0Fr2iv%7Ctkp%3ABk9SR5j3wKvGZA"

# Send a request to the website using the session
response = session.get(url, headers=headers)

# Initialize data containers
product_data = {}
seller_data = {}
reviews_list = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the product title
    title_tag = soup.find('span', class_='ux-textspans--BOLD')
    title = title_tag.text.strip() if title_tag else 'N/A'

    # Extract the price
    price_tag = soup.find('div', class_='x-price-primary')
    price = price_tag.text.strip() if price_tag else 'N/A'

    # Extract product description or other details 
    description_div = soup.select('#desc_ifr')
    iframe = description_div[0] if description_div else None
    desc_text = 'N/A'
    
    if iframe:
        des_link = iframe['src']
        response_2 = session.get(des_link, headers=headers)  # Use session here
        if response_2.status_code == 200:
            pepper_soup = BeautifulSoup(response_2.text, 'html.parser')
            desc = pepper_soup.find('div', class_='x-item-description-child')
            desc_text = desc.text.strip() if desc else 'N/A'

    # Store the results in a product data dictionary
    product_data = {
        "title": title,
        "price": price,
        "description": desc_text
    }

    # Save data to JSON file
    with open('product_data.json', 'w', encoding='utf-8') as product_file:
        json.dump(product_data, product_file, indent=4)

    # Find the div containing seller information
    details = soup.find('div', class_='x-sellercard-atf__info')
    texts = details.find_all(class_='ux-textspans')

    # Check if we have at least 3 elements (office name, number of sales, and rating)
    if len(texts) >= 3:
        seller_data = {
            "office_name": texts[0].text.strip(),
            "number_of_sales": texts[1].text.strip(),
            "positive_feedback": texts[2].text.strip()
        }

    # Save data to JSON file
    with open('seller_data.json', 'w', encoding='utf-8') as seller_file:
        json.dump(seller_data, seller_file, indent=4)    

    # Function to scrape reviews from a given URL
    def scrape_reviews(url):
        review_response = session.get(url, headers=headers)  # Use session here
        if review_response.status_code == 200:
            soup = BeautifulSoup(review_response.text, 'html.parser')
            review_dates = soup.find_all('span', class_='fdbk-container__details__info__divide__time')
            review_texts = soup.find_all('div', class_='fdbk-container__details__comment')

            # Iterate over the reviewers and review texts
            for review_date, review_text in zip(review_dates, review_texts):
                review_data = {
                    'review_date': review_date.text.strip(),
                    'text': review_text.text.strip()
                }
                reviews_list.append(review_data)

            # Check for the next page link
            next_page_link = soup.find('a', {'data-testid': 'pagination-next'})
            if next_page_link:
                href_value = next_page_link['href']
                next_page_url = f"https://www.ebay.com/fdbk/mweb_profile{href_value}"
                return next_page_url
        return None

    # Start scraping reviews
    current_url = "https://www.ebay.com/fdbk/mweb_profile?fdbkType=FeedbackReceivedAsSeller&item_id=225614929686&username=backtotheoffice&filter=feedback_page%3ARECEIVED_AS_SELLER&sort=RELEVANCE"
    
    while current_url:
        current_url = scrape_reviews(current_url)

    # Save data to JSON file
    with open('reviews.json', 'w', encoding='utf-8') as reviews_file:
        json.dump(reviews_list, reviews_file, indent=4)

    print("Data saved to product_data.json, seller_data.json, and reviews.json")

    # Save all data to a CSV file
    with open('product_seller_reviews.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'price', 'description', 'office_name', 'number_of_sales', 'positive_feedback', 'review_date', 'review_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write product and seller data with reviews
        for review in reviews_list:
            writer.writerow({
                'title': product_data['title'],
                'price': product_data['price'],
                'description': product_data['description'],
                'office_name': seller_data.get('office_name', 'N/A'),
                'number_of_sales': seller_data.get('number_of_sales', 'N/A'),
                'positive_feedback': seller_data.get('positive_feedback', 'N/A'),
                'review_date': review['review_date'],
                'review_text': review['text']
            })

    print("Data saved to product_seller_reviews.csv")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
