import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# ---- User-Agent and Headers for Indian Sites ----
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# ---- Multi-Platform Scrapers ----

def scrape_amazon_in(search_query, max_results=10):
    """Scrape Amazon India for products"""
    query = quote_plus(search_query)
    url = f"https://www.amazon.in/s?k={query}"
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        
        products = []
        items = soup.select("div.s-main-slot div[data-component-type='s-search-result']")[:max_results]
        
        for item in items:
            try:
                # Try multiple selectors for title - Amazon frequently changes their structure
                title_elem = (item.select_one("h2 a span") or 
                             item.select_one("span.a-size-base-plus") or 
                             item.select_one("span.a-text-normal") or
                             item.select_one("h2 span"))
                title = title_elem.text.strip() if title_elem else "N/A"
                
                # Try multiple selectors for link
                link_elem = (item.select_one("h2 a") or 
                            item.select_one("a.a-link-normal") or
                            item.select_one("a.a-text-normal"))
                link = "https://www.amazon.in" + link_elem["href"] if link_elem and link_elem.get("href") else "N/A"
                
                # Debug: print the HTML structure to understand what's available
                if title == "N/A":
                    print(f"DEBUG - Item HTML: {item.prettify()[:500]}...")
                
                # Extract price
                price_whole = item.select_one("span.a-price-whole")
                price_fraction = item.select_one("span.a-price-fraction")
                price = 0
                if price_whole:
                    try:
                        price_str = price_whole.text.replace(",", "").replace("₹", "").strip()
                        if price_fraction:
                            price_str += "." + price_fraction.text
                        price = float(price_str)
                    except:
                        price = 0
                
                # Extract rating
                rating_span = item.select_one("span.a-icon-alt")
                rating = 0
                if rating_span:
                    try:
                        rating = float(rating_span.text.split()[0])
                    except:
                        rating = 0
                
                # Extract image
                img_elem = item.select_one("img.s-image")
                image_url = (
                    img_elem.get("src")
                    or img_elem.get("data-src")
                    or img_elem.get("srcset", "").split(" ")[0]
                    if img_elem else ""
                )
                
                print(f"Amazon - Title: {title}, Link: {link}, Price: {price}, Rating: {rating}, Image: {image_url}")  # Debug statement
                
                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": link,
                    "image": image_url,
                    "platform": "Amazon",
                    "platform_icon": "📦"
                })
            except Exception as e:
                print(f"Error extracting Amazon product: {e}")  # Debug statement
                continue
                
        return products
        
    except Exception as e:
        print(f"Amazon scraping error: {e}")
        return []

def scrape_flipkart(search_query, max_results=10):
    """Scrape Flipkart for products"""
    query = quote_plus(search_query)
    url = f"https://www.flipkart.com/search?q={query}"
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        
        products = []
        items = soup.select("div._1AtVbE")[:max_results]
        
        for item in items:
            try:
                title_elem = item.select_one("a.IRpwTa") or item.select_one("a._1fQZEK")
                title = title_elem.text.strip() if title_elem else "N/A"
                
                link_elem = item.select_one("a.IRpwTa") or item.select_one("a._1fQZEK")
                link = "https://www.flipkart.com" + link_elem["href"] if link_elem and link_elem.get("href") else "N/A"
                
                # Extract price
                price_elem = item.select_one("div._30jeq3")
                price = 0
                if price_elem:
                    try:
                        price_str = price_elem.text.replace("₹", "").replace(",", "").strip()
                        price = float(price_str)
                    except:
                        price = 0
                
                # Extract rating
                rating_elem = item.select_one("div._3LWZlK")
                rating = 0
                if rating_elem:
                    try:
                        rating = float(rating_elem.text)
                    except:
                        rating = 0
                
                # Extract image
                img_elem = item.select_one("img._396cs4") or item.select_one("img._2r_T1I")
                image_url = img_elem.get("src") if img_elem else ""
                
                print(f"Flipkart - Title: {title}, Link: {link}, Price: {price}, Rating: {rating}, Image: {image_url}")  # Debug statement
                
                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": link,
                    "image": image_url,
                    "platform": "Flipkart",
                    "platform_icon": "🛒"
                })
            except Exception as e:
                print(f"Error extracting Flipkart product: {e}")  # Debug statement
                continue
                
        return products
        
    except Exception as e:
        print(f"⚠️ Flipkart access blocked (403 error). This is a common anti-scraping measure.")
        print(f"   Try using a different network or VPN if you need Flipkart results.")
        return []

def scrape_myntra(search_query, max_results=10):
    """Scrape Myntra for fashion products"""
    query = quote_plus(search_query)
    url = f"https://www.myntra.com/{search_query.replace(' ', '-')}?rawQuery={query}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")

        products = []
        items = soup.select("li.product-base")[:max_results]

        for item in items:
            try:
                brand_elem = item.select_one("h3.product-brand")
                name_elem = item.select_one("h4.product-product")
                title = f"{brand_elem.text.strip()} {name_elem.text.strip()}" if brand_elem and name_elem else "N/A"

                link_elem = item.select_one("a[href]")
                link = "https://www.myntra.com" + link_elem["href"] if link_elem and link_elem.get("href") else "N/A"

                # Extract price
                price_elem = item.select_one("span.product-discountedPrice, span.product-price")
                price = 0
                if price_elem:
                    try:
                        price_str = price_elem.text.replace("₹", "").replace(",", "").strip()
                        price = float(price_str)
                    except:
                        price = 0

                # Extract rating (Myntra doesn't always show ratings)
                rating_elem = item.select_one("div.product-ratingsContainer")
                rating = 0
                if rating_elem:
                    try:
                        rating_text = rating_elem.text.strip()
                        rating = float(rating_text) if rating_text else 0
                    except:
                        rating = 0

                # Extract image
                img_elem = item.select_one("img.img-responsive")
                image_url = img_elem.get("src") if img_elem else ""

                print(f"Myntra - Title: {title}, Link: {link}, Price: {price}, Rating: {rating}, Image: {image_url}")  # Debug statement

                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": link,
                    "image": image_url,
                    "platform": "Myntra",
                    "platform_icon": "👕"
                })
            except Exception as e:
                print(f"Error extracting Myntra product: {e}")  # Debug statement
                continue

        return products

    except Exception as e:
        print(f"Myntra scraping error: {e}")
        return []

def scrape_all_platforms(search_query, max_results=10):
    """Scrape all available platforms"""
    all_products = []

    # Scrape Amazon
    amazon_products = scrape_amazon_in(search_query, max_results)
    all_products.extend(amazon_products)

    # Scrape Flipkart
    flipkart_products = scrape_flipkart(search_query, max_results)
    all_products.extend(flipkart_products)

    # Scrape Myntra (for fashion products)
    if any(keyword in search_query.lower() for keyword in ['clothing', 'fashion', 'shirt', 'dress', 'shoes', 'accessories']):
        myntra_products = scrape_myntra(search_query, max_results)
        all_products.extend(myntra_products)

    return all_products

# ---- Persona Recommenders ----
def premiummax(products, top_n=3):
    """PremiumMax: Prioritize ratings and quality"""
    filtered = [p for p in products if p['rating'] >= 3.5 and p['price'] > 0]
    if not filtered:
        filtered = products
    sorted_products = sorted(filtered, key=lambda x: (x['rating'], -x['price']), reverse=True)
    return sorted_products[:top_n]

def budgetbalance(products, top_n=3):
    """BudgetBalance: Prioritize value for money"""
    filtered = [p for p in products if p['price'] > 0 and p['rating'] >= 2.5]
    if not filtered:
        filtered = products
    sorted_products = sorted(filtered, key=lambda x: (x['price'], -x['rating']))
    return sorted_products[:top_n]

# ---- Enhanced Persona Debate ----
def persona_debate(products, user_pref="neutral"):
    pm_recs = premiummax(products, 3)
    bb_recs = budgetbalance(products, 3)

    print(f"\n🤖 PremiumMax (High-End Expert) found {len(pm_recs)} recommendations:")
    for i, p in enumerate(pm_recs, 1):
        print(f"   {i}. 🏆 {p['title'][:50]}... | ₹{p['price']} | ⭐{p['rating']} | {p['platform_icon']} {p['platform']}")

    print(f"\n🤖 BudgetBalance (Smart Saver) found {len(bb_recs)} recommendations:")
    for i, p in enumerate(bb_recs, 1):
        print(f"   {i}. 💰 {p['title'][:50]}... | ₹{p['price']} | ⭐{p['rating']} | {p['platform_icon']} {p['platform']}")

    # Conflict Resolution
    if user_pref == "premium":
        final = pm_recs[0] if pm_recs else (products[0] if products else None)
        print(f"\n✅ Final Decision: PremiumMax wins! Best quality product from {final['platform']}")
        return final
    elif user_pref == "budget":
        final = bb_recs[0] if bb_recs else (products[0] if products else None)
        print(f"\n✅ Final Decision: BudgetBalance wins! Best value from {final['platform']}")
        return final
    else:
        # Best value-for-money across all platforms
        filtered = [p for p in products if p['price'] > 0 and p['rating'] > 0]
        if filtered:
            best = sorted(filtered, key=lambda x: (x['rating'] / (x['price'] + 1)), reverse=True)[0]
            print(f"\n✅ Final Decision: Best value for money from {best['platform']}")
            return best
        else:
            return products[0] if products else None

# ---- Enhanced Demo Function ----
def run_enhanced_demo():
    print("🎯 AI Shopping Assistant - Multi-Platform Demo")
    print("=" * 50)
    
    search = input("🔍 What product are you looking for? ")
    pref = input("💰 Preference? (premium/budget/neutral): ").lower()
    
    if pref not in ['premium', 'budget', 'neutral']:
        pref = 'neutral'
    
    print(f"\n🌐 Searching across Amazon, Flipkart, and Myntra...")
    
    results = scrape_all_platforms(search, 5)
    
    if results:
        print(f"\n✅ Found {len(results)} products across platforms:")
        for i, product in enumerate(results, 1):
            print(f"   {i}. {product['platform_icon']} {product['platform']}: {product['title'][:40]}... - ₹{product['price']}")
        
        final_choice = persona_debate(results, pref)
        
        if final_choice:
            print(f"\n🎯 FINAL RECOMMENDATION:")
            print(f"   Product: {final_choice['title']}")
            print(f"   Price: ₹{final_choice['price']}")
            print(f"   Rating: ⭐{final_choice['rating']}")
            print(f"   Platform: {final_choice['platform_icon']} {final_choice['platform']}")
            print(f"   Link: {final_choice['url']}")
        else:
            print("❌ No suitable products found.")
    else:
        print("❌ No products found. Try a different search term.")

if __name__ == "__main__":
    run_enhanced_demo()



