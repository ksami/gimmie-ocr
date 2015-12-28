# /usr/bin/python
from datetime import datetime
from PIL import Image

import pytesseract
from SimpleCV import Image as SImage
from fuzzywuzzy import process as FProcess

# Preprocessing
input_img = SImage('./images/receipt.jpg')
img = input_img.blur(2).binarize(128).invert()
img.show()


# OCR
pil_img = Image.fromstring('RGB', img.size(), img.toString())
output = pytesseract.image_to_string(pil_img, lang='eng', config='./receipt --user-words=./eng.user-words')

# Parse output
choices = [
    'FAIRPRICE XTRA',
    'NEX HYPERMART',
    'SINGAPORE',
    'REG',
    'GST',
    'SENGCHOON EGG 55 G',
    'GD S/V ENR WHT 600G',
    'N-FRS SOYAMK ALMD1L',
    'FP SPINACH 250G',
    'FP PF SATAY-BEEF500',
    'DELMONTE BANANAS-BAG',
    'NSOY FR S/MILK A',
    'NORMAL PRICE',
    'LINK CARD',
    'SUBTOTAL',
    'TOTAL',
    'VISA'
]

lines = output.split('\n')
results = 'Actual | Predicted\n'
for line in lines:
    (predicted, ratio) = FProcess.extractOne(line, choices)
    if ratio==0:
        results += line + ' | \n'
    else:
        results += line + ' | (' + predicted + ', ' + str(ratio) + ')\n'


filename = './results/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.txt'
with open(filename, 'w') as f:
    f.write(results)