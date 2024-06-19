import requests
from bs4 import BeautifulSoup
import pandas as pd

def is_valid_year(text):
    try:
        year = int(text)
        return 1900 <= year <= 2024
    except ValueError:
        return False

def scrape_starships_collection(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    current_year = None
    current_category = None

    # Iterate over the elements to capture years, categories, and tables
    for element in soup.find_all(['h2', 'h3', 'span', 'tr', 'th']):
        if element.name == 'h2':
            text = element.get_text(strip=True)
            if is_valid_year(text):
                current_year = text
        elif element.name == 'h3' or (element.name == 'span' and 'mw-headline' in element.attrs.get('class', [])):
            current_category = element.get_text(strip=True)
        elif element.name == 'th' and 'id' in element.attrs:
            text = element.get_text(strip=True)
            if is_valid_year(text):
                current_year = text
        elif element.name == 'tr':
            cols = element.find_all('td')
            if len(cols) >= 3:
                # This row contains data
                number = cols[0].get_text(strip=True)
                title_tag = cols[2].find('a')
                title = title_tag.get_text(strip=True) if title_tag else ''
                
                data.append({
                    'Number': number,
                    'Year': current_year,
                    'Category': current_category,
                    'Title': title
                })
            else:
                print(f"Warning: Skipping row with unexpected structure: {element}")

    return data

def save_to_excel(data_dict, filename):
    with pd.ExcelWriter(filename) as writer:
        for sheet_name, data in data_dict.items():
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Data successfully saved to {filename}")

# URLs of the webpages
urls = {
    'Starships_Collection': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_The_Official_Starships_Collection#2014',
    'Discovery_Starships_Collection': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_Discovery_The_Official_Starships_Collection',
    'Universe_Starships_Collection': 'https://memory-alpha.fandom.com/wiki/Star_Trek_Universe:_The_Official_Starships_Collection'
}

# Scrape the data for each URL
data_dict = {}
for name, url in urls.items():
    data_dict[name] = scrape_starships_collection(url)

# Save to Excel with multiple sheets
save_to_excel(data_dict, 'xls_results/starships_collection.xlsx')
