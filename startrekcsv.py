import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://memory-alpha.fandom.com/wiki/Star_Trek:_Discovery_The_Official_Starships_Collection"

# Send a request to the webpage
response = requests.get(url)

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table in the webpage
table = soup.find('table', {'class': 'grey'})

# Check if the table was found
if table:
    # Extract headers
    headers = [th.text.strip() for th in table.find_all('th')]
    
    print("Headers found:", headers)  # Debug print for headers

    # Extract rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = tr.find_all(['td', 'th'])  # Including 'th' for potential sub-headers
        row = []
        for cell in cells:
            # Handle cells that contain images
            img = cell.find('img')
            if img:
                # Extract the actual image URL
                img_url = img.get('data-src') or img.get('src')
                row.append(img_url)
            else:
                row.append(cell.text.strip())
        rows.append(row)
    
    # Debug print for a sample row
    if rows:
        print("Sample row:", rows[0])
    
    # Adjust rows to match the length of headers
    max_len = len(headers)
    adjusted_rows = []
    for row in rows:
        if len(row) < max_len:
            row.extend([''] * (max_len - len(row)))
        adjusted_rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(adjusted_rows, columns=headers)
    print(df.head())  # Debug print for DataFrame
    df.to_csv('output/csv_results/star_trek_discovery_ships.csv', index=False)
    print("Data has been saved to star_trek_discovery_ships.csv")
else:
    print("Table not found on the page.")
