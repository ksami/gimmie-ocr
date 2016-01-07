# /usr/bin/python
from datetime import datetime
# from PIL import Image

# import pytesseract
from SimpleCV import Image as SImage
from fuzzywuzzy import process as FProcess
import subprocess
import shlex

HEADING_LINES_COUNT = 8
FLAG_CRITERIA_OCR = 50  # range 0-100
FLAG_CRITERIA_FUZZY = 50  # range 0-100

def process(filename):
    # Preprocessing
    input_img = SImage('./images/' + filename)
    img = input_img.binarize().invert().bilateralFilter().scale(2)
    img.save('./processed/' + filename)


    # OCR
    ocr_bin = shlex.split('./ocr ./processed/' + filename)
    process = subprocess.Popen(ocr_bin, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()


    # Parse output
    with open('eng.user-words', 'r') as f:
        choices = f.read().strip().split('\n')

    lines = out.split('\n')
    results = []
    confidences = []
    ratios = []
    flags = []
    ignore_count = 0
    for ln in lines:
        # don't process empty lines
        if(len(ln) == 0):
            continue

        # ignore 1st x lines of heading eg. FAIRPRICE XTRA
        if(ignore_count<HEADING_LINES_COUNT):
            ignore_count+=1
            continue

        # line in format "confidence || line"
        ocr_line = ln.split('||')
        conf, item_and_price = ocr_line[0], ocr_line[1].split(' ')

        # assume price is last word in line
        item, price = ' '.join(item_and_price[:-1]).strip(), item_and_price[-1].strip()

        # Use fuzzy string matching to correct result
        predicted, ratio = FProcess.extractOne(item, choices)
        if ratio >= FLAG_CRITERIA_FUZZY and float(conf) >= FLAG_CRITERIA_OCR:
            output_line = predicted
            flag = ''
        else:
            output_line = item
            flag = 'Flag'

        results.append(output_line + ' ' + price)
        confidences.append(conf)
        ratios.append(str(ratio))
        flags.append(flag)


    # Write results with flags for manual checking
    zipped = zip(results, confidences, ratios, flags)
    mapped = map(lambda tup: ' || '.join(tup), zipped)

    outfile = './results/' + filename + '.txt'
    with open(outfile, 'w') as f:
        f.write('\n'.join(mapped))


    # Return just the results list
    return results