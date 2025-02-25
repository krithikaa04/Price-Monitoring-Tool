import requests
from bs4 import BeautifulSoup
import csv
import json
import urllib.parse
import time
import random
from datetime import datetime

# Scrape.do API token
token = "<your token>"

# User agent to mimic a browser
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
]

# Product URLs for each platform
urls = {
    "flipkart": [
        "https://www.flipkart.com/v-guard-m10-pro-wall-mounted-black-900-cmh-chimney/p/itmd483f2cac050a?pid=CHYGZCQHJGCDAGTG&marketplace=FLIPKART",
    ],
    "amazon": [
        "https://www.amazon.in/V-Guard-Suction-900-Push-Button-Powder-Coated/dp/B0C194RTGW/ref=sr_1_1?crid=3OMWM5Q683PZL&dib=eyJ2IjoiMSJ9.9yv06CC4-kLHTIRpDvw9Sshv12ZDjfIWkP3U1fFSin62_5KrI4YknuG5bXF4jozG5RHjTxIO1M15kOMYO0teXfIQNTHSaErntx10TbFQRTrBIVe7KSpgX2kerftQt1EztOkGtwR5rtFjA2YkUw4-StWtGtCRtd7ksR3ZFpXoCb9PwHoIycbiUhufQ_KJtVn6TJPR2alhWnpkvPhAXoHgF6KT2LwgbjalxpbpcCXKxTo.xiLz4GfBGfsuZQDIGS2-uWoXH-Et_ob0YUgVJ6dE9c0&dib_tag=se&keywords=V-Guard+M10+Pro+Wall+Mounted+Black+900+CMH+Chimney&nsdOptOutParam=true&qid=1740487318&s=kitchen&sprefix=v-guard+m10+pro+wall+mounted+black+900+cmh+chimney%2Ckitchen%2C408&sr=1-1",  # Example product URL
    ],
    "snapdeal": [
        "https://www.snapdeal.com/product/shopeleven-egg-boiler-1-ltr/649245196493",  # Example product URL
    ]
}

# Function to get a random user agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Function to scrape Flipkart products
def scrape_flipkart(url, use_proxy=True):
    data = {"source": "Flipkart", "url": url, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    try:
        if use_proxy:
            # Use scrape.do proxy
            target_url_encoded = urllib.parse.quote_plus(url)
            api_url = f"http://api.scrape.do?token={token}&url={target_url_encoded}"
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(api_url, headers=headers)
        else:
            # Direct request
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract Product Name - try multiple possible class names
            try:
                name_element = soup.select_one("span.B_NuCI, h1.yhB1nd, span.VU-ZEz")
                data["name"] = name_element.text.strip() if name_element else "Name Not Found"
            except Exception as e:
                data["name"] = "Name Not Found"
                data["name_error"] = str(e)

            # Extract Price - try multiple possible class names
            try:
                price_element = soup.select_one("div._30jeq3._16Jk6d, div.Nx9bqj.CxhGGd, div._30jeq3")
                data["price"] = price_element.text.strip() if price_element else "Price Not Found"
            except Exception as e:
                data["price"] = "Price Not Found"
                data["price_error"] = str(e)

            # Extract Rating - try multiple possible class names
            try:
                rating_element = soup.select_one("div._3LWZlK, div.XQDdHH, span._1lRcqv")
                data["rating"] = rating_element.text.strip() if rating_element else "Rating Not Found"
            except Exception as e:
                data["rating"] = "Rating Not Found"
                data["rating_error"] = str(e)

            # Extract specifications
            specs = {}
            try:
                spec_tables = soup.select("table._14cfVK, table._1NIlFV")
                for table in spec_tables:
                    rows = table.select("tr")
                    for row in rows:
                        cols = row.select("td")
                        if len(cols) >= 2:
                            key = cols[0].text.strip()
                            value = cols[1].text.strip()
                            specs[key] = value
                data["specifications"] = specs
            except Exception as e:
                data["specifications"] = {}
                data["specifications_error"] = str(e)

            data["html"] = html_content  # Store raw HTML
            data["status"] = "success"
        else:
            data["status"] = "failed"
            data["error"] = f"Failed to fetch data (Status code: {response.status_code})"
    except Exception as e:
        data["status"] = "failed"
        data["error"] = str(e)
    
    return data

# Function to scrape Amazon products
def scrape_amazon(url, use_proxy=True):
    data = {"source": "Amazon", "url": url, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    try:
        if use_proxy:
            # Use scrape.do proxy
            target_url_encoded = urllib.parse.quote_plus(url)
            api_url = f"http://api.scrape.do?token={token}&url={target_url_encoded}"
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(api_url, headers=headers)
        else:
            # Direct request
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract Product Name
            try:
                name_element = soup.select_one("#productTitle, #title, .product-title")
                data["name"] = name_element.text.strip() if name_element else "Name Not Found"
            except Exception as e:
                data["name"] = "Name Not Found"
                data["name_error"] = str(e)

            # Extract Price
            try:
                price_element = soup.select_one(".a-price .a-offscreen, #priceblock_ourprice, #priceblock_dealprice, .a-price-whole")
                data["price"] = price_element.text.strip() if price_element else "Price Not Found"
            except Exception as e:
                data["price"] = "Price Not Found"
                data["price_error"] = str(e)

            # Extract Rating
            try:
                rating_element = soup.select_one("#acrPopover, .a-icon-alt")
                if rating_element:
                    rating_text = rating_element.text.strip()
                    # Extract just the number from text like "4.5 out of 5 stars"
                    rating = rating_text.split(' ')[0] if 'out of' in rating_text else rating_text
                    data["rating"] = rating
                else:
                    data["rating"] = "Rating Not Found"
            except Exception as e:
                data["rating"] = "Rating Not Found"
                data["rating_error"] = str(e)

            # Extract specifications/features
            specs = {}
            try:
                # Try to get from product details section
                details_section = soup.select_one("#productDetails_techSpec_section_1, #detail-bullets, #prodDetails, #technicalSpecifications_section_1")
                if details_section:
                    rows = details_section.select("tr, .content li")
                    for row in rows:
                        if row.name == "tr":
                            cols = row.select("th, td")
                            if len(cols) >= 2:
                                key = cols[0].text.strip()
                                value = cols[1].text.strip()
                                specs[key] = value
                        elif row.name == "li":
                            parts = row.text.split(':')
                            if len(parts) >= 2:
                                key = parts[0].strip()
                                value = ':'.join(parts[1:]).strip()
                                specs[key] = value
                data["specifications"] = specs
            except Exception as e:
                data["specifications"] = {}
                data["specifications_error"] = str(e)

            data["html"] = html_content  # Store raw HTML
            data["status"] = "success"
        else:
            data["status"] = "failed"
            data["error"] = f"Failed to fetch data (Status code: {response.status_code})"
    except Exception as e:
        data["status"] = "failed"
        data["error"] = str(e)
    
    return data

# Function to scrape Snapdeal products
def scrape_snapdeal(url, use_proxy=True):
    data = {"source": "Snapdeal", "url": url, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    try:
        if use_proxy:
            # Use scrape.do proxy
            target_url_encoded = urllib.parse.quote_plus(url)
            api_url = f"http://api.scrape.do?token={token}&url={target_url_encoded}"
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(api_url, headers=headers)
        else:
            # Direct request
            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract Product Name
            try:
                name_element = soup.select_one("h1.pdp-e-i-head, .product-title")
                data["name"] = name_element.text.strip() if name_element else "Name Not Found"
            except Exception as e:
                data["name"] = "Name Not Found"
                data["name_error"] = str(e)

            # Extract Price
            try:
                price_element = soup.select_one("span.payBlkBig, .product-price")
                data["price"] = price_element.text.strip() if price_element else "Price Not Found"
            except Exception as e:
                data["price"] = "Price Not Found"
                data["price_error"] = str(e)

            # Extract Rating
            try:
                rating_element = soup.select_one(".product-rating .review-rating-average, .product-rating .avrg-rating")
                data["rating"] = rating_element.text.strip() if rating_element else "Rating Not Found"
            except Exception as e:
                data["rating"] = "Rating Not Found"
                data["rating_error"] = str(e)

            # Extract specifications
            specs = {}
            try:
                # Try to get from specification section
                spec_section = soup.select_one(".spec-section, .product-specs")
                if spec_section:
                    spec_rows = spec_section.select("li, .spec-row")
                    for row in spec_rows:
                        parts = row.text.strip().split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip()
                            value = ':'.join(parts[1:]).strip()
                            specs[key] = value
                data["specifications"] = specs
            except Exception as e:
                data["specifications"] = {}
                data["specifications_error"] = str(e)

            data["html"] = html_content  # Store raw HTML
            data["status"] = "success"
        else:
            data["status"] = "failed"
            data["error"] = f"Failed to fetch data (Status code: {response.status_code})"
    except Exception as e:
        data["status"] = "failed"
        data["error"] = str(e)
    
    return data

# Main function to run the scraper
def main():
    use_proxy = True  # Set to False if you want to make direct requests
    
    # Timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepare CSV file
    csv_filename = f"product_data_{timestamp}.csv"
    json_filename = f"product_data_{timestamp}.json"
    
    # Store all product data
    all_product_data = []
    
    # Open CSV file
    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        # Define CSV headers
        fieldnames = ["Source", "Product Name", "Price", "Rating", "URL", "Status"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Scrape Flipkart products
        print("🔍 Scraping Flipkart products...")
        for url in urls["flipkart"]:
            print(f"Processing: {url}")
            product_data = scrape_flipkart(url, use_proxy)
            all_product_data.append(product_data)
            
            # Write to CSV
            writer.writerow({
                "Source": product_data["source"],
                "Product Name": product_data["name"],
                "Price": product_data["price"],
                "Rating": product_data["rating"],
                "URL": product_data["url"],
                "Status": product_data["status"]
            })
            
            # Add delay to avoid being blocked
            time.sleep(random.uniform(2, 5))
        
        # Scrape Amazon products
        print("\n🔍 Scraping Amazon products...")
        for url in urls["amazon"]:
            print(f"Processing: {url}")
            product_data = scrape_amazon(url, use_proxy)
            all_product_data.append(product_data)
            
            # Write to CSV
            writer.writerow({
                "Source": product_data["source"],
                "Product Name": product_data["name"],
                "Price": product_data["price"],
                "Rating": product_data["rating"],
                "URL": product_data["url"],
                "Status": product_data["status"]
            })
            
            # Add delay to avoid being blocked
            time.sleep(random.uniform(3, 7))
        
        # Scrape Snapdeal products
        print("\n🔍 Scraping Snapdeal products...")
        for url in urls["snapdeal"]:
            print(f"Processing: {url}")
            product_data = scrape_snapdeal(url, use_proxy)
            all_product_data.append(product_data)
            
            # Write to CSV
            writer.writerow({
                "Source": product_data["source"],
                "Product Name": product_data["name"],
                "Price": product_data["price"],
                "Rating": product_data["rating"],
                "URL": product_data["url"],
                "Status": product_data["status"]
            })
            
            # Add delay to avoid being blocked
            time.sleep(random.uniform(2, 5))
    
    print(f"\n✅ Scraping completed!")
    print(f"➡️ CSV data saved to: {csv_filename}")
    print(f"➡️ JSON data saved to: {json_filename}")
    print(f"📊 Total products scraped: {len(all_product_data)}")
    
    # Print summary of results
    success_count = sum(1 for item in all_product_data if item["status"] == "success")
    print(f"✓ Successfully scraped: {success_count}")
    print(f"✗ Failed: {len(all_product_data) - success_count}")

if __name__ == "__main__":
    main()