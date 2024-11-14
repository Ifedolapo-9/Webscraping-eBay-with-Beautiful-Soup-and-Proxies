# Webscraping-eBay-with-Beautiful-Soup-and-Proxies
Webscraping eBay to retrieve product information, seller information, and reviews using proxies. This script also handles pagination.

---

# eBay Web Scraping with BeautifulSoup Using Proxies

This repository contains a Python script for scraping product details from eBay using **BeautifulSoup** and rotating **proxies** to avoid IP bans. The script extracts product information such as titles, prices, and links, helping you gather data efficiently while staying under eBay’s radar.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Proxy Configuration](#proxy-configuration)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

## Introduction
eBay is one of the world's largest online marketplaces, making it a valuable source of product data for analysis, research, or e-commerce. However, scraping data from eBay can be challenging due to rate limits and IP blocking. This script leverages **BeautifulSoup** for parsing HTML and uses proxies to bypass these limitations.

## Features
- Scrapes product titles, prices, and links from eBay search results.
- Utilizes proxies to prevent IP bans and enhance scraping reliability.
- Configurable to extract data from multiple product pages.

## Technologies Used
- **Python** 3.x
- **BeautifulSoup** for HTML parsing
- **Requests** library for sending HTTP requests
- Proxy support for enhanced anonymity

## Requirements
- **Python** 3.7+
- **BeautifulSoup** and **Requests** libraries
- A list of working proxy servers for IP rotation

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ebay-scraper-with-beautifulsoup.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd ebay-scraper-with-beautifulsoup
   ```
3. **Install Required Packages**:
   - Using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

## Usage
1. **Set Up Your Proxies**: Update the script with your list of proxies.
2. **Run the Script**:
   ```bash
   python main_beautiful_soup.py
   ```
3. The script will collect product data from eBay search results and save it in the specified format (e.g., CSV or JSON).

## Proxy Configuration
- Ensure you have secured your proxies from reliable proxy companies. Add them as seen in the script.
- The script will rotate through these proxies when sending requests.

## Notes
- **Rate Limiting**: Be mindful of eBay's rate-limiting policies and adjust the script's request frequency if necessary.
- **Legal and Ethical Use**: Ensure compliance with eBay’s terms of service and use the script responsibly.

## Contributing
Contributions are welcome! If you have ideas for improvements or new features, feel free to fork the project and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

