#In this snippet, we first extract the base64 encoded image data from the data URI by splitting the string at the comma.
#  We then decode the base64 data and attempt to open it as an image using the PIL library. 
# If successful, we print out the first 20 pixels of the image. 
# If there are any errors during the decoding or opening process, we catch the exception and print an error message.
import base64
from PIL import Image
from io import BytesIO

# Base64 string (replace with your actual base64 string)
data_uri = "data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D"

# Remove the prefix
header, encoded = data_uri.split(",", 1)

# Decode the image data
image_data = base64.b64decode(encoded)

# Verify if the decoded data is valid for an image
try:
    image = Image.open(BytesIO(image_data))

    # Print out the first 20 pixels
    pixels = list(image.getdata())[:20]
    print("First 20 pixels:", pixels)

except Exception as e:
    print(f"Failed to decode image: {e}")


