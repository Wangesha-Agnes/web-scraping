
import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    """Fetch and parse a single page."""
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
def parse_articles(html):
    """Extract article data from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    content_container = soup.find("main") or soup.find("div", class_="content")
    if content_container:
        sections = content_container.find_all(["section", "article", "div"], recursive=True)
        for section in sections:
            title = section.find(["h1", "h2", "h3", "h4", "h5", "h6"])
            if title:

                title_text = title.get_text(strip=True)
                
                paragraphs = section.find_all("p", recursive=True)
                content = " ".join(p.get_text(strip=True) for p in paragraphs)
                articles.append({
                    'title': title_text,
                    'content': content
                })
    return articles
def save_articles_to_file(articles, page_number):
    """Save collected articles to a file."""
    filename = f"Fetched_Articles_Page_{page_number}.txt"
    with open(filename, "w", encoding='UTF-8') as f:
        for i, article in enumerate(articles, start=1):
            title = article['title']
            content = article['content']
            f.write(f"Article {i} (Page {page_number}): \n Title : {title} \n Content : \n{content}\n\n")
            print(f"Article {i} (Page {page_number}): \n Title : {title} \n Content : \n{content}\n")
def scrape_all_pages(base_url, max_pages=5):
    """Scrape data from all pages."""
    for page_number in range(1, max_pages + 1):
        url = f"{base_url}?page={page_number}"
        html = fetch_page(url)
        if html is None:
            print(f"Failed to retrieve page {page_number}.")
            continue
        articles = parse_articles(html)
        if not articles:
            print(f"No more articles found on page {page_number}.")
            break
        save_articles_to_file(articles, page_number)
        
        time.sleep(1)
if __name__ == "__main__":
    base_url = "https://lca.logcluster.org/kenya-231-border-crossing-busia"
    scrape_all_pages(base_url, max_pages=10) 




#Another code

import requests
import pdfplumber
import mysql.connector
from io import BytesIO
def fetch_pdf(url):
    """Fetch and read a PDF file from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
def extract_text_from_pdf(pdf_file):
    """Extract text from the PDF file."""
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""
    return extracted_text
def parse_text(text):
    """Parse and categorize text extracted from the PDF."""
    extracted_info = []
    lines = text.split('\n')
    for line in lines:
        if 'tariff' in line.lower():  # Adjust this line based on actual content
            extracted_info.append({
                'title': line,
                'content': line
            })
    return extracted_info
def insert_tariffs_to_db(tariffs):
    """Insert tariff information into the database."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  # Ensure this password is correct
            database='trade_documents'
        )
        cursor = connection.cursor()
        for tariff in tariffs:
            title = tariff['title']
            content = tariff['content']
            cursor.execute(
                "INSERT INTO `tariffs` (`title`, `content`) VALUES (%s, %s)",
                (title, content)
            )
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
def scrape_pdf(url):
    """Fetch, extract, and insert data from a PDF."""
    pdf_file = fetch_pdf(url)
    if pdf_file is None:
        print("Failed to retrieve the PDF file.")
        return
    text = extract_text_from_pdf(pdf_file)
    tariffs = parse_text(text)
    insert_tariffs_to_db(tariffs)
    print('PDF has been processed and data has been inserted into the database.')
if __name__ == "__main__":
    pdf_url = "https://kra.go.ke/images/publications/EAC-CET-2022-VERSION-30TH-JUNE-Fn.pdf"
    scrape_pdf(pdf_url)
    
    
    
#Another one
import requests
from bs4 import BeautifulSoup
import time
def fetch_page(url):
    """Fetch and parse a single page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
def parse_articles(soup):
    """Extract and categorize products from the soup object."""
    categorized_articles = {
        "Agricultural Products": [
            "Beans", "Maize", "Bananas", "Rice", "Potatoes", "Wheat", "Vegetables", "Fruits", "Herbs", "Seeds"
        ],
        "Electronics": [
            "Mobile Phones", "Computers", "Televisions", "Speakers", "Headphones", "Laptops", "Cameras", "Tablets", "Smart Watches"
        ],
        "Clothing": [
            "Shirts", "Pants", "Dresses", "Jackets", "Shoes", "Sweaters", "Hats", "Gloves", "Socks", "Scarves"
        ],
        "Textiles and Fabrics": [
            "Cotton", "Silk", "Wool", "Nylon", "Polyester", "Linen", "Rayon", "Spandex", "Denim", "Fleece"
        ],
        "Automobiles": [
            "Cars", "Motorcycles", "Trucks", "Buses", "Scooters", "Parts", "Accessories"
        ],
        "Household Goods": [
            "Furniture", "ApplianGroup Members"
        ],
        "Health and Beauty": [
            "Cosmetics", "Skincare", "Haircare", "Personal Care", "Supplements", "Health Devices"
        ]
    }
    print("Page source preview:\n", soup.prettify()[:2000])
    products = soup.find_all("div", class_="product-item")
    extracted_info = []
    for index, product in enumerate(products):
        print(f"Parsing product {index + 1}...")
        title_tag = product.find("h3", class_="product-title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        description_tag = product.find("div", class_="product-description")
        description = description_tag.get_text(strip=True) if description_tag else "No description found"
        additional_info = []
        info_tags = product.find_all("span", class_="additional-info")
        for info_tag in info_tags:
            additional_info.append(info_tag.get_text(strip=True))
        category = "Other"
        if any(keyword in title.lower() for keyword in ["beans", "maize", "bananas", "rice", "potatoes", "wheat", "vegetables", "fruits", "herbs", "seeds"]):
            category = "Agricultural Products"
        elif any(keyword in title.lower() for keyword in ["mobile", "phone", "computer", "television", "speaker", "headphone", "laptop", "camera", "tablet", "smart watch"]):
            category = "Electronics"
        elif any(keyword in title.lower() for keyword in ["shirt", "pants", "dress", "jacket", "shoes", "sweater", "hat", "glove", "sock", "scarf"]):
            category = "Clothing"
        elif any(keyword in title.lower() for keyword in ["cotton", "silk", "wool", "nylon", "polyester", "linen", "rayon", "spandex", "denim", "fleece"]):
            category = "Textiles and Fabrics"
        elif any(keyword in title.lower() for keyword in ["car", "motorcycle", "truck", "bus", "scooter", "part", "accessory"]):
            category = "Automobiles"
        elif any(keyword in title.lower() for keyword in ["furniture", "appliance", "decor", "kitchenware", "bedding", "cleaning"]):
            category = "Household Goods"
        elif any(keyword in title.lower() for keyword in ["cosmetic", "skincare", "haircare", "personal care", "supplement", "health device"]):
            category = "Health and Beauty"
        extracted_info.append({
            'title': title,
            'description': description,
            'additional_info': additional_info,
            'category': category
        })
    return extracted_info, categorized_articles
def display_categorized_info(extracted_info, categorized_articles):
    """Display categorized products to the console."""
    categorized_output = {key: [] for key in categorized_articles.keys()}
    for info in extracted_info:
        category = info['category']
        if category in categorized_articles:
            categorized_output[category].append({
                'title': info['title'],
                'description': info['description'],
                'additional_info': info['additional_info']
            })
    for category, documents in categorized_articles.items():
        print(f"\n--- {category} ---")
        print("Examples of Products:")
        for document in documents:
            print(f" - {document}")
        print("\nExtracted Products:")
        if category in categorized_output:
            for i, product in enumerate(categorized_output[category], start=1):
                title = product['title']
                description = product['description']
                additional_info = product['additional_info']
                print(f"\nProduct {i}:")
                print(f" Title: {title}")
                print(f" Description: {description[:500]}...")
                if additional_info:
                    print(f" Additional Info: {', '.join(additional_info)}")
        else:
            print("No products found in this category.")
def scrape_pages(base_url, num_pages=1):
    """Scrape data from a limited number of pages and categorize products."""
    all_extracted_info = []
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}&page={page_number}"
        print(f"Fetching page {page_number}...")
        soup = fetch_page(url)
        if soup is None:
            print(f"Failed to retrieve page {page_number}.")
            continue
        extracted_info, categorized_articles = parse_articles(soup)
        all_extracted_info.extend(extracted_info)
        time.sleep(1)
    display_categorized_info(all_extracted_info, categorized_articles)
    print('Selected pages have been processed and categorized.')
if __name__ == "__main__":
    base_url = "https://infotradekenya.go.ke/Products?l=en"
    scrape_pages(base_url, num_pages=1)


