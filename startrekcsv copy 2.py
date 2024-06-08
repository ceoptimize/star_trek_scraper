import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.utils.dataframe import dataframe_to_rows
from PIL import Image
from io import BytesIO
import os

# Create a directory for saving images
os.makedirs('images/star_trek_indiv_screenshots', exist_ok=True)
os.makedirs('output/xls_results', exist_ok=True)

# URL of the page to scrape
url = "https://memory-alpha.fandom.com/wiki/Star_Trek:_Discovery_The_Official_Starships_Collection"

# Send a request to the webpage
response = requests.get(url)

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Helper function to extract and clean a table
def extract_and_clean_table(table):
    headers = [th.text.strip() for th in table.find_all('th')]
    headers.insert(0, "Year")  # Insert 'Year' as the first header

    rows = []
    year = ''
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = tr.find_all(['td', 'th'])  # Including 'th' for potential sub-headers
        if len(cells) == 1:  # Row with only the year
            year = cells[0].text.strip()
        else:
            row = [year]
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

    # Adjust rows to match the length of headers
    max_len = len(headers)
    adjusted_rows = []
    for row in rows:
        if len(row) < max_len:
            row.extend([''] * (max_len - len(row)))
        adjusted_rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(adjusted_rows, columns=headers)

    # Clean DataFrame to remove duplicate header row
    df_cleaned = df.iloc[1:].reset_index(drop=True)
    df_cleaned.columns = df.iloc[0]
    df_cleaned = df_cleaned.rename_axis(None, axis=1)  # Remove the axis name
    df_cleaned.columns.values[0] = "Year"  # Ensure the first column header is set to "Year"

    return df_cleaned

# Find tables and their respective sections
tables = soup.find_all('table', {'class': 'grey'})
sections = ['Issues', 'Bonus Edition Issues', 'Special Edition Issues']

# Create a workbook
wb = Workbook()
wb.remove(wb.active)  # Remove the default sheet

# Process each table and add to different sheets
for table, section in zip(tables, sections):
    df_cleaned = extract_and_clean_table(table)

    # Create a new sheet for each section
    ws = wb.create_sheet(title=section)

    # Write the cleaned DataFrame to the worksheet
    for r in dataframe_to_rows(df_cleaned, index=False, header=True):
        ws.append(r)

    # Insert images into the worksheet
    for idx, row in enumerate(df_cleaned.values, start=2):  # Start from the second row (after headers)
        for col_idx, value in enumerate(row):
            if isinstance(value, str) and value.startswith('http'):
                response = requests.get(value)
                img = Image.open(BytesIO(response.content))
                img_path = f'images/star_trek_indiv_screenshots/{section}_image_{idx}_{col_idx}.png'
                img.save(img_path)
                excel_img = ExcelImage(img_path)
                excel_img.width = 240  # Set larger width
                excel_img.height = 240  # Set larger height
                img_cell = f'{chr(65 + col_idx)}{idx}'  # Column for images
                ws.add_image(excel_img, img_cell)
                df_cleaned.at[idx - 2, 'Image'] = img_path  # Update DataFrame with image path

# Save the workbook
wb.save('output/xls_results/star_trek_discovery_ships.xlsx')
print("Data has been saved to star_trek_discovery_ships.xlsx")
