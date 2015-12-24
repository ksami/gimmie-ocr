# /usr/bin/python
from PIL import Image

import pytesseract
from SimpleCV import Image as SImage


# Preprocessing
input_img = SImage('./images/receipt.jpg')
img = input_img.blur(2).binarize(128).invert()
img.show()


# OCR
pil_img = Image.fromstring('RGB', img.size(), img.toString())
print(pytesseract.image_to_string(pil_img, lang='eng', config='./receipt --user-words=./eng.user-words'))
