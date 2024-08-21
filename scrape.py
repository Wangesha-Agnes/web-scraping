import requests
from bs4 import BeautifulSoup
import sqlite3
import time


def connect_db(db_name="scraped_data.db"):
    conn = sqlite3.connect(db_name)
    return conn


def create_tables(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                category TEXT,
                page_number INTEGER
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                additional_info TEXT,
                category TEXT
            )
        ''')


def insert_article(conn, title, content, category, page_number):
    with conn:
        conn.execute('''
            INSERT INTO articles (title, content, category, page_number)
            VALUES (?, ?, ?, ?)
        ''', (title, content, category, page_number))


def insert_product(conn, title, description, additional_info, category):
    with conn:
        conn.execute('''
            INSERT INTO products (title, description, additional_info, category)
            VALUES (?, ?, ?, ?)
        ''', (title, description, ', '.join(additional_info), category))

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
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_articles(soup):
    """Extract and categorize articles from the soup object."""
    categorized_articles = {
        "Agricultural Documents": [
            "Certificate of Origin",
            "Phytosanitary Certificate",
            "Export License",
            "Bill of Lading",
            "Invoice",
            "Packing List"
        ],
        "Electronics": [
            "Certificate of Conformity",
            "Export License",
            "Bill of Lading",
            "Invoice",
            "Packing List",
            "Declaration of Conformity"
        ],
        "Clothing": [
            "Certificate of Origin",
            "Export License",
            "Bill of Lading",
            "Invoice",
            "Packing List",
            "Customs Declaration"
        ],
        "Textiles and Fabrics": [
            "Certificate of Origin",
            "Export License",
            "Bill of Lading",
            "Invoice",
            "Packing List",
            "Certificate of Authenticity"
        ]
    }
    
    articles = soup.find_all("article", class_="col-sm-6")
    extracted_info = []

    for index, article in enumerate(articles):
        print(f"Parsing article {index + 1}...")
        title_tag = article.find("h4", class_="card-title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        content_parts = []
        body = article.find("div", class_="card-body")
        if body:
            for element in body.find_all(["p", "div", "span"], recursive=True):
                text = element.get_text(strip=True)
                if text:
                    content_parts.append(text)
        content = " ".join(content_parts).strip() if content_parts else "No content found"
        category = "Other"
        if any(keyword in title.lower() for keyword in ["agriculture", "farm", "crops"]):
            category = "Agricultural Documents"
        elif any(keyword in title.lower() for keyword in ["electronics", "devices"]):
            category = "Electronics"
        elif any(keyword in title.lower() for keyword in ["clothing", "apparel"]):
            category = "Clothing"
        elif any(keyword in title.lower() for keyword in ["textiles", "fabrics"]):
            category = "Textiles and Fabrics"
        extracted_info.append({
            'title': title,
            'content': content,
            'category': category
        })
    return extracted_info, categorized_articles

def parse_products(soup):
    """Extract and categorize products from the soup object."""
    categorized_products = {
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
            "Furniture", "Appliances", "Decor", "Kitchenware", "Bedding", "Cleaning"
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
    return extracted_info, categorized_products

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

def scrape_all_pages(base_url, max_pages=5):
    """Scrape data from all pages, parse and categorize articles and products."""
    conn = connect_db()
    create_tables(conn)

    all_articles = []
    all_extracted_info = []

    for page_number in range(1, max_pages + 1):
        url = f"{base_url}?page={page_number}"
        soup = fetch_page(url)
        if soup is None:
            print(f"Failed to retrieve page {page_number}.")
            continue
        
       
        articles, categorized_articles = parse_articles(soup)
        if articles:
            for article in articles:
                insert_article(conn, article['title'], article['content'], article['category'], page_number)
            all_articles.extend(articles)
        
  
        extracted_info, categorized_products = parse_products(soup)
        if extracted_info:
            for product in extracted_info:
                insert_product(conn, product['title'], product['description'], product['additional_info'], product['category'])
            all_extracted_info.extend(extracted_info)

        time.sleep(1)
    
    display_categorized_info(all_extracted_info, categorized_products)
    print('All pages have been processed and categorized.')
    conn.close()

if __name__ == "__main__":
    base_url = "https://infotradekenya.go.ke/Products?l=en"
    scrape_all_pages(base_url, max_pages=5)
