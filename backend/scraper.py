import requests
from bs4 import BeautifulSoup
import re
from app import app
from models import db, Product

def clean_price(price_str):
    if not price_str:
        return 0.0
    # Remove non-numeric characters except period
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def scrape_jumia(query):
    url = f"https://www.jumia.com.ng/catalog/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        # Jumia selector: article.prd
        cards = soup.select('article.prd')
        
        for card in cards[:5]: # Top 5 results
            title_tag = card.select_one('h3.name')
            price_tag = card.select_one('div.prc')
            
            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                price = clean_price(price_tag.get_text(strip=True))
                
                products.append({
                    'name': title,
                    'price': price,
                    'source': 'Jumia',
                    'category': 'solar_panel' if 'panel' in query.lower() else 'battery'
                })
        return products
    except Exception as e:
        print(f"Error scraping Jumia: {e}")
        return []

def scrape_konga(query):
    url = f"https://www.konga.com/search?search={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        # Konga selector: article[class*="ListingCard_listingCardContainer"]
        cards = soup.select('article[class*="ListingCard_listingCardContainer"]')
        
        for card in cards[:5]: # Top 5 results
            title_tag = card.select_one('h3[class*="ListingCard_productTitle"]')
            price_tag = card.select_one('div[class*="shared_priceBoxWrapper"]')
            
            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                price = clean_price(price_tag.get_text(strip=True))
                
                products.append({
                    'name': title,
                    'price': price,
                    'source': 'Konga',
                    'category': 'solar_panel' if 'panel' in query.lower() else 'battery'
                })
        return products
    except Exception as e:
        print(f"Error scraping Konga: {e}")
        return []

def run_scraper():
    queries = ['Jinko Solar Panel 550W', 'Felicity Lithium Battery']
    results = []
    
    for query in queries:
        print(f"Scraping for {query}...")
        results.extend(scrape_jumia(query))
        results.extend(scrape_konga(query))
    
    with app.app_context():
        print(f"Found {len(results)} items. Updating database...")
        for item in results:
            # Check if product exists (simple check by name for now)
            # In a real app we might want more robust matching
            existing = Product.query.filter_by(name=item['name']).first()
            
            if existing:
                existing.price = item['price']
                existing.stock = 1 # Assume available if scraped
            else:
                new_product = Product(
                    name=item['name'],
                    category=item['category'],
                    specs={'source': item['source']},
                    price=item['price'],
                    stock=1
                )
                db.session.add(new_product)
        
        db.session.commit()
    
    return results

if __name__ == '__main__':
    run_scraper()
