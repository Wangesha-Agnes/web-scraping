
# import requests
# from bs4 import BeautifulSoup


# response = requests.get("https://ura.go.ug/en/category/imports-exports/customs-enforcements/")


# soup = BeautifulSoup(response.text, "html.parser")

# articles = soup.find_all("article", class_="col-sm-6")
# # print('article ===>', articles)


# rules = []

# with open("Articles.txt", "w", encoding='UTF-8') as f:
#     for i, article in enumerate(articles, start=1):
#         title_tag = article.find("h4", class_="card-title")
#         if title_tag:
#             title = title_tag.get_text(strip=True)
#         body = article.find("div", class_="card-body")
#         if body:
#             content = body.get_text(strip=True).replace(title, "")
        
        
#         rules.append({
#             'title':title,
#             'content':content
#         })

      
#         f.writelines(f"Article {i}: \n Title : {title} \n  \t{content} \n")

#         print(f"Article {i}: \n Title : {title} \n  \t{content}")
#         print("\n")
# print('rules ====>', rules)





# import requests
# from bs4 import BeautifulSoup
# import time

# def fetch_page(url):
#     """Fetch and parse a single page."""
#     headers = {
#         'Cache-Control': 'no-cache',
#         'Pragma': 'no-cache',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Connection': 'keep-alive',
#     }
#     try:
#         print(f"Fetching URL: {url}")
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  
#         return response.text
#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None
# def parse_articles(html):
#     """Extract article data from the HTML content."""
#     soup = BeautifulSoup(html, "html.parser")
#     articles = []

#     content_container = soup.find("main") or soup.find("div", class_="content")
#     if content_container:
#         sections = content_container.find_all(["section", "article", "div"], recursive=True)
#         for section in sections:
#             title = section.find(["h1", "h2", "h3", "h4", "h5", "h6"])
#             if title:

#                 title_text = title.get_text(strip=True)
                
#                 paragraphs = section.find_all("p", recursive=True)
#                 content = " ".join(p.get_text(strip=True) for p in paragraphs)
#                 articles.append({
#                     'title': title_text,
#                     'content': content
#                 })
#     return articles
# def save_articles_to_file(articles, page_number):
#     """Save collected articles to a file."""
#     filename = f"Fetched_Articles_Page_{page_number}.txt"
#     with open(filename, "w", encoding='UTF-8') as f:
#         for i, article in enumerate(articles, start=1):
#             title = article['title']
#             content = article['content']
#             f.write(f"Article {i} (Page {page_number}): \n Title : {title} \n Content : \n{content}\n\n")
#             print(f"Article {i} (Page {page_number}): \n Title : {title} \n Content : \n{content}\n")
# def scrape_all_pages(base_url, max_pages=5):
#     """Scrape data from all pages."""
#     for page_number in range(1, max_pages + 1):
#         url = f"{base_url}?page={page_number}"
#         html = fetch_page(url)
#         if html is None:
#             print(f"Failed to retrieve page {page_number}.")
#             continue
#         articles = parse_articles(html)
#         if not articles:
#             print(f"No more articles found on page {page_number}.")
#             break
#         save_articles_to_file(articles, page_number)
        
#         time.sleep(1)
# if __name__ == "__main__":
#     base_url = "https://lca.logcluster.org/kenya-231-border-crossing-busia"
#     scrape_all_pages(base_url, max_pages=10) 




#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup
#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None
# def parse_articles(soup):
#     """Extract and categorize articles from the soup object."""
#     categorized_articles = {
#         "Agricultural Documents": [
#             "Certificate of Origin",
#             "Phytosanitary Certificate",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List"
#         ],
#         "Electronics": [
#             "Certificate of Conformity",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Declaration of Conformity"
#         ],
#         "Clothing": [
#             "Certificate of Origin",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Customs Declaration"
#         ],
#         "Textiles and Fabrics": [
#             "Certificate of Origin",
#             "Export License",
#             "Bill of Lading",
#             "Invoice",
#             "Packing List",
#             "Certificate of Authenticity"
#         ]
#     }
#     print("Page source preview:\n", soup.prettify()[:2000])
#     articles = soup.find_all("article", class_="col-sm-6")
#     extracted_info = []
#     for index, article in enumerate(articles):
#         print(f"Parsing article {index + 1}...")
#         title_tag = article.find("h4", class_="card-title")
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"
#         content_parts = []
#         body = article.find("div", class_="card-body")
#         if body:
#             for element in body.find_all(["p", "div", "span"], recursive=True):
#                 text = element.get_text(strip=True)
#                 if text:
#                     content_parts.append(text)
#         content = " ".join(content_parts).strip() if content_parts else "No content found"
#         category = "Other"
#         if any(keyword in title.lower() for keyword in ["agriculture", "farm", "crops"]):
#             category = "Agricultural Documents"
#         elif any(keyword in title.lower() for keyword in ["electronics", "devices"]):
#             category = "Electronics"
#         elif any(keyword in title.lower() for keyword in ["clothing", "apparel"]):
#             category = "Clothing"
#         elif any(keyword in title.lower() for keyword in ["textiles", "fabrics"]):
#             category = "Textiles and Fabrics"
#         extracted_info.append({
#             'title': title,
#             'content': content,
#             'category': category
#         })
#     return extracted_info, categorized_articles
# def display_categorized_info(extracted_info, categorized_articles):




