try:
    import Image
except:
    from PIL import Image

import pytesseract

img = Image.open('receipt.jpg')
img.load()
print(pytesseract.image_to_string(img))
