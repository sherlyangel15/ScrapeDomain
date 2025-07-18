# expired_domain_hunter.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import nltk
from nltk.corpus import wordnet as wn
import re
import random
import os

nltk.download('wordnet')

# Configuration
DOMAIN_LIMIT = 100
DELAY = 1
OUTPUT_CSV = "final_expired_domains.csv"
EXPIRED_DOMAIN_SOURCES = [
    "https://www.expireddomains.net/backorder-expired-domains/",
    "https://www.justdropped.com/",
    "https://moonsy.com/expired_domains/"
]

# -----------------------------------
# 1. Extract Domains from Multiple Sources
# -----------------------------------
def extract_domains_from_multiple_sources(sources):
    print("🔍 Scraping domains from sources...")
    all_domains = set()
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in sources:
        print(f"🌐 Extracting from: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all("a", href=True)
            for link in links:
                text = link.get_text().strip().lower()
                if text.endswith(".com") and len(text) <= 25:
                    all_domains.add(text)
        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
        time.sleep(1)

    return list(all_domains)[:DOMAIN_LIMIT]

# -----------------------------------
# 2. Dummy Expiry Check (replaces WHOIS)
# -----------------------------------
def verify_expiry_dummy(domain):
    return random.choice([True, False])  # Simulate 50% expired

# -----------------------------------
# 3. Brandability Score
# -----------------------------------
def score_brandability(domain):
    name = domain.replace('.com', '').lower()
    score = 0
    if len(name) <= 10: score += 2
    if re.fullmatch(r"[a-z0-9\-]+", name): score += 2
    words = re.findall(r"[a-z]+", name)
    for word in words:
        if wn.synsets(word): score += 3
    if not any(char.isdigit() for char in name): score += 1
    return score

# -----------------------------------
# 4. Mock SEO Metrics (Replace with Real API)
# -----------------------------------
def get_mock_seo_data(domain):
    return {
        "domain_rating": random.randint(10, 90),
        "backlinks": random.randint(100, 5000),
        "traffic": random.randint(0, 10000),
        "valuation": f"${random.randint(100, 5000)}"
    }

# -----------------------------------
# 5. Main Logic
# -----------------------------------
def main():
    all_domains = extract_domains_from_multiple_sources(EXPIRED_DOMAIN_SOURCES)
    print(f"🔎 Total scraped domains: {len(all_domains)}")

    expired_domains = []
    for domain in all_domains:
        print(f"🧪 Checking dummy expiry for: {domain}")
        if verify_expiry_dummy(domain):
            expired_domains.append(domain)
        time.sleep(DELAY)

    print(f"✅ Verified expired domains: {len(expired_domains)}")

    data = []
    for domain in expired_domains:
        brand_score = score_brandability(domain)
        seo = get_mock_seo_data(domain)
        status = "GOOD" if brand_score >= 6 and seo['domain_rating'] >= 30 else "POOR"
        data.append({
            "domain": domain,
            "brand_score": brand_score,
            **seo,
            "status": status
        })

    df = pd.DataFrame(data)

    if os.path.exists(OUTPUT_CSV):
        df_existing = pd.read_csv(OUTPUT_CSV)
        df_combined = pd.concat([df_existing, df]).drop_duplicates(subset="domain")
        df_combined.to_csv(OUTPUT_CSV, index=False)
    else:
        df.to_csv(OUTPUT_CSV, index=False)

    print(f"📁 Updated and saved to {OUTPUT_CSV}")

# -----------------------------------
# Run
# -----------------------------------
if __name__ == "_main_":
    main()

#want to verify?
import os
if os.path.exists(OUTPUT_CSV):
    print(f"✅ File successfully created: {OUTPUT_CSV}")
else:
    print("❌ File not found.")