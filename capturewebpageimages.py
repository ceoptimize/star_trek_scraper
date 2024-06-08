
#This script uses Selenium to capture a full-page screenshot of a webpage.
# It scrolls through the page, taking screenshots at each position, and then saves them as separate image files.

from selenium import webdriver
from PIL import Image
from io import BytesIO
import os
import time

def capture_full_page_screenshots(url, output_folder):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(2)  # Allow time for the page to load

        # Get the total scroll height
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        current_position = 0
        screenshot_index = 0

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        while current_position < total_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1)  # Allow time for the page to render after scroll

            screenshot = driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))

            # Save each screenshot separately
            screenshot_path = os.path.join(output_folder, f"screenshot_{screenshot_index}.png")
            image.save(screenshot_path)
            screenshot_index += 1

            current_position += viewport_height

    finally:
        driver.quit()

# Example usage
url = 'https://memory-alpha.fandom.com/wiki/Star_Trek:_Discovery_The_Official_Starships_Collection'
output_folder = 'output/star_trek_scroll_screenshots'
capture_full_page_screenshots(url, output_folder)


