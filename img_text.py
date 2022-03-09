# get frames from video
# use google lib
# save the string to a file

# single lines
# black & white
# 5sec video

# pip install pytesseract

import pdb
from PIL import Image
import pytesseract

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
image_path = r"C:\\Users\\ritik\\PycharmProjects\\braille_project\\Braille-Translator\\test.jpg"

# Opening the image & storing it in an image object
img = Image.open(image_path)
pdb.set_trace()
# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text[:-1])