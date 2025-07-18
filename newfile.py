import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
# ========== Scraper Functions ==========
def scrape_expireddomains_net():
    url = "https://www.expireddomains.net/expired-domains/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        domains = set()
        for td in soup.find_all("td", class_="field_domain"):
            a = td.find("a")
            if a and ".com" in a.text:
                domains.add(a.text.strip().lower())
        return domains
    except Exception as e:
        print(f"Error scraping ExpiredDomains.net: {e}")
        return set()
def scrape_moonsy():
    url = "https://moonsy.com/expired_domains/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        pre = soup.find("pre")
        if pre:
            return set(line.strip().lower() for line in pre.text.splitlines() if line.endswith(".com"))
        return set()
    except Exception as e:
        print(f"Error scraping Moonsy: {e}")
        return set()
def scrape_justdropped():
    url = "https://www.justdropped.com/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        domains = set()
        for div in soup.find_all("div", class_="col-md-3 col-xs-6"):
            a = div.find("a")
            if a and a.text.endswith(".com"):
                domains.add(a.text.strip().lower())
        return domains
    except Exception as e:
        print(f"Error scraping JustDropped: {e}")
        return set()
def scrape_snapnames():
    url = "https://www.snapnames.com/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        domains = set()
        for a in soup.find_all("a"):
            text = a.text.strip().lower()
            if text.endswith(".com"):
                domains.add(text)
        return domains
    except Exception as e:
        print(f"Error scraping SnapNames: {e}")
        return set()
def scrape_namejet():
    url = "https://www.namejet.com/featuredauctions"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        domains = set()
        for a in soup.find_all("a"):
            text = a.text.strip().lower()
            if text.endswith(".com"):
                domains.add(text)
        return domains
    except Exception as e:
        print(f"Error scraping NameJet: {e}")
        return set()
# ========== Spider Function ==========
def spider(start_url, depth=1, visited=None):
    if visited is None:
        visited = set()
    if depth == 0 or start_url in visited:
        return set()
    visited.add(start_url)
    domains = set()
    try:
        response = requests.get(start_url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.text.strip().lower()
            if text.endswith(".com"):
                domains.add(text)
            elif href.startswith("http"):
                domains.update(spider(href, depth - 1, visited))
    except Exception as e:
        print(f"Spider error at {start_url}: {e}")
    return domains
# ========== Main Function ==========
def main():
    source_sites = {
        "expireddomains.net", "moonsy.com", "justdropped.com",
        "snapnames.com", "namejet.com"
    }
    all_domains = set()
    all_domains.update(scrape_expireddomains_net())
    all_domains.update(scrape_moonsy())
    all_domains.update(scrape_justdropped())
    all_domains.update(scrape_snapnames())
    all_domains.update(scrape_namejet())
    all_domains.update(spider("https://www.expireddomains.net/expired-domains/", depth=1))
    clean_domains = {
        d for d in all_domains
        if d.endswith(".com") and not any(site in d for site in source_sites)
    }
    # Save with today's date
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"expired_domains_{today}.csv"
    # Avoid duplicates
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        existing_domains = set(existing_df['Domain'].str.lower())
    else:
        existing_domains = set()
    new_domains = clean_domains - existing_domains
    if new_domains:
        df_new = pd.DataFrame(list(new_domains), columns=["Domain"])
        if existing_domains:
            df_existing = pd.read_csv(file_path)
            df_final = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates()
        else:
            df_final = df_new
        df_final.to_csv(file_path, index=False)
        print(f"{len(new_domains)} new domains added to {file_path}")
    else:
        print("No new domains to add.")
# ========== Run ==========
if __name__ == "__main__":
    main()