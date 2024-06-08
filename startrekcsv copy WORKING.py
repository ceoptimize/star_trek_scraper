#Takes a table from a webpage and saves it to an Excel file with images
#The script first extracts the table from the webpage using BeautifulSoup and then processes the data to create a DataFrame.
#It then saves the DataFrame to an Excel file, adding images from the webpage to the corresponding cells in the Excel sheet.
#The images are downloaded and saved locally before being inserted into the Excel sheet.
#The final Excel file contains the table data along with the images from the webpage.
#The script also creates directories to store the images and the Excel file.
#The script is useful for extracting structured data from webpages and combining it with images for further analysis or presentation.
#The script demonstrates the use of web scraping, data processing, and Excel manipulation in Python.
#The script can be modified to work with different webpages and tables by adjusting the scraping logic and data processing steps.
#Here we are scraping a table from a Star Trek webpage and saving it to an Excel file with images of starships and it is 
#only looking at the first table on the page.

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

# Find the table in the webpage
table = soup.find('table', {'class': 'grey'})

# Check if the table was found
if table:
    # Extract headers
    headers = [th.text.strip() for th in table.find_all('th')]
    headers.insert(0, "Year")  # Insert 'Year' as the first header
    print("Headers found:", headers)  # Debug print for headers

    # Extract rows
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

    # Clean DataFrame to remove duplicate header row
    #What is happening here?
    #The code is removing the first row of the DataFrame, which is the duplicate header row, and resetting the index to start from 0.

    #I want to drop the first row of the DataFrame and reset the index to start from 0.
    #The sample row should not be included in the final DataFrame.

    df_cleaned = df.iloc[1:].reset_index(drop=True)
    df_cleaned.columns = df.iloc[0]
    df_cleaned = df_cleaned.rename_axis(None, axis=1)  # Remove the axis name




    print(df_cleaned.head())  # Debug print for cleaned DataFrame

    # Ensure the first column header is set to "Year"
    df_cleaned.columns.values[0] = "Year"

    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Write the cleaned DataFrame to the worksheet
    for r in dataframe_to_rows(df_cleaned, index=False, header=True):
        ws.append(r)

    # Insert images into the worksheet
    for idx, row in enumerate(df_cleaned.values, start=2):  # Start from the second row (after headers)
        for col_idx, value in enumerate(row):
            if isinstance(value, str) and value.startswith('http'):
                response = requests.get(value)
                img = Image.open(BytesIO(response.content))
                img_path = f'images/star_trek_indiv_screenshots/image_{idx}_{col_idx}.png'
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
else:
    print("Table not found on the page.")
