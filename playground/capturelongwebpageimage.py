#Thoughts

#This script uses Selenium to capture a full-page screenshot of a webpage. 
# It scrolls through the page, taking screenshots at each position, and then stitches them together 
# to create a single image of the entire page. 
# This can be useful for capturing content that extends beyond the initial viewport. 
# The resulting image can be saved to a file for further analysis or processing.

#This was not good for intake by GPT-4o. When asked questions about the image, it did not provide accurate answers.


from selenium import webdriver
from PIL import Image
from io import BytesIO
import time

def capture_full_page_screenshot(url, output_path):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(2)  # Allow time for the page to load

        # Get the total scroll height
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        current_position = 0
        images = []

        while current_position < total_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1)  # Allow time for the page to render after scroll

            screenshot = driver.get_screenshot_as_png()
            images.append(Image.open(BytesIO(screenshot)))
            
            current_position += viewport_height

        # Stitch images together
        width = images[0].width
        height = sum(image.height for image in images)

        stitched_image = Image.new('RGB', (width, height))

        current_height = 0
        for image in images:
            stitched_image.paste(image, (0, current_height))
            current_height += image.height

        stitched_image.save(output_path)

    finally:
        driver.quit()


capture_full_page_screenshot("https://memory-alpha.fandom.com/wiki/Star_Trek:_Discovery_The_Official_Starships_Collection", "webpage_screenshot.png")

