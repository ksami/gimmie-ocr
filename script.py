# /usr/bin/python
from datetime import datetime
# from PIL import Image

# import pytesseract
from SimpleCV import Image as SImage
from fuzzywuzzy import process as FProcess
import subprocess
import shlex

def process(filename):
    # Preprocessing
    input_img = SImage('./images/' + filename)
    img = input_img.blur(2).binarize(128).invert().scale(2)
    img.save('./processed/' + filename)


    # OCR
    ocr_bin = shlex.split('./ocr ./processed/' + filename)
    process = subprocess.Popen(ocr_bin, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()

    # pil_img = Image.fromstring('RGB', img.size(), img.toString())
    # output = pytesseract.image_to_string(pil_img, lang='eng', config='./receipt --user-words=./eng.user-words')

    # Parse output
    with open('eng.user-words', 'r') as f:
        choices = f.read().split('\n')


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


    outfile = './results/' + filename + '.txt'
    with open(outfile, 'w') as f:
        f.write(results)
