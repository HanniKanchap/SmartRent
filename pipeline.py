import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_olx_delhi(start_page=2, end_page=40):
    listings = []

    for page_num in range(start_page, end_page + 1):
        url = f"https://www.olx.in/en-in/delhi_g4058659/apartments-flats_c1723?page={page_num}"
        print(f"🔎 Scraping page {page_num}...")

        try:
            response = requests.get(url, headers=headers, timeout=300)
            
        except requests.RequestException as e:
            print(f"❌ Error on page {page_num}: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        ads = soup.find_all("li", class_="_1DNjI")

        if not ads:
            print(f"⚠️ No ads found on page {page_num}. Possibly JS-rendered.")
            continue

        for ad in ads:
            title_tag = ad.find("span", class_="_2poNJ")
            location_tag = ad.find("span", class_="_2VQu4")
            price_tag = ad.find("span", class_="_2Ks63")
            link_tag = ad.find("a", href=True)
            info_tag = ad.find("span", class_="YBbhy")
            image_tag = ad.find("img", class_="_3vnjf") or ad.find("img", class_="_2hBzJ")

            listings.append({
                "Title": title_tag.get_text(strip=True) if title_tag else None,
                "Location": location_tag.get_text(strip=True) if location_tag else None,
                "Price": price_tag.get_text(strip=True) if price_tag else None,
                "Link": "https://www.olx.in" + link_tag["href"] if link_tag else None,
                "Image": image_tag["src"] if image_tag and image_tag.has_attr("src") else None,
                "Info": info_tag.get_text(strip=True) if info_tag else None
            })

        time.sleep(1.5) 

    return listings

# Run and export
data = scrape_olx_delhi()
df = pd.DataFrame(data)
df.to_csv("scraped_olx_data.csv", index=False)
print(f"✅ Scraped {len(df)} listings across pages {2} to {50}.")

## Cleaning data
df = df.drop_duplicates().reset_index(drop = True)

def clean_price(data):
    data =  data.replace('₹','').replace(',','')
    return int(data)

df['Price'] = df['Price'].apply(clean_price)

import re

def parse_listing(info):
    if pd.isna(info):
        return pd.Series([None, None, None])

    bhk = None
    bath = None
    area = None

    parts = info.split(' - ')
    for part in parts:
        part = part.strip().lower()

        # Extract BHK
        if 'bhk' in part:
            match = re.search(r'(\d+)\s*bhk', part)
            if match:
                bhk = int(match.group(1))

        # Extract Bathroom
        elif 'bathroom' in part:
            match = re.search(r'(\d+)\s*bathroom', part)
            if match:
                bath = int(match.group(1))

        # Extract Area
        elif 'sqft' in part or 'ft' in part:
            match = re.search(r'(\d+(\.\d+)?)\s*(sqft|ft)', part)
            if match:
                raw_area = float(match.group(1))
                unit = match.group(3)
                area = raw_area if unit == 'sqft' else raw_area * raw_area  # Convert ft² to m² if needed
                area = round(area, 2)

    return pd.Series([bhk, bath, area])

df[['BHK', 'Bathroom', 'Area']] = df['Info'].apply(parse_listing)
def get_area(data):
    data = data.split(',')
    return data[0]

df['Locality'] = df['Location'].apply(get_area)

df2 = pd.read_csv('data/cleaned_data.csv',index_col=0)

merged_df = pd.concat([df, df2], ignore_index=True)
merged_df = merged_df.drop_duplicates().reset_index(drop=True)
print(merged_df.head)
print(merged_df.shape)
merged_df.to_csv('data/cleaned_data.csv')
