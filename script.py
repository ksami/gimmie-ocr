# /usr/bin/python
from datetime import datetime
# from PIL import Image

# import pytesseract
from SimpleCV import Image as SImage
from fuzzywuzzy import process as FProcess
import subprocess
import shlex

# Preprocessing
input_img = SImage('./images/receipt.jpg')
img = input_img.blur(2).binarize(128).invert().scale(2)
img.save('./processed/receipt.jpg')


# OCR
ocr_bin = shlex.split('./ocr ./processed/receipt.jpg')
process = subprocess.Popen(ocr_bin, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = process.communicate()

# pil_img = Image.fromstring('RGB', img.size(), img.toString())
# output = pytesseract.image_to_string(pil_img, lang='eng', config='./receipt --user-words=./eng.user-words')

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
results = 'Actual | Predicted | OCR Conf\n'
for line in lines:
    if(line.startswith('line: ')):
        ln = line[6:]
        predicted, ratio = FProcess.extractOne(ln, choices)
        if ratio==0:
            results += ln + ' | '
        else:
            results += ln + ' | (' + predicted + ', ' + str(ratio) + ') | '
    elif(line.startswith('conf: ')):
        ln = line[6:]
        results += ln + '\n'


filename = './results/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.txt'
with open(filename, 'w') as f:
    f.write(results)
