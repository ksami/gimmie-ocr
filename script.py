# /usr/bin/python
from PIL import Image

import pytesseract
from SimpleCV import Image as SImage

img = SImage('./images/receipt.jpg')
img.show()
pil_img = Image.fromstring('RGB', img.size(), img.toString())
print(pytesseract.image_to_string(pil_img))
