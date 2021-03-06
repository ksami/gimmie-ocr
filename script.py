# /usr/bin/python
import subprocess
import shlex
import sys

from SimpleCV import Image, Color
from fuzzywuzzy import process as FProcess

HEADING_LINES_COUNT = 8
FLAG_CRITERIA_OCR = 50  # range 0-100
FLAG_CRITERIA_FUZZY = 50  # range 0-100



def process(filename, task_id=0, stretch_thresh_low=140, stretch_thresh_high=140, rotate_angle=0, toWriteFile=False):
    # Preprocessing
    print('Running task_id: ' + str(task_id))
    input_img = Image('./images/' + filename)


    img = input_img.colorDistance(Color.BLACK).stretch(stretch_thresh_low, stretch_thresh_high).scale(2).rotate(rotate_angle, fixed=False)
    img.save('./processed/'+ str(task_id) + '-' + filename)


    # OCR
    ocr_bin = shlex.split('./ocr ./processed/' + str(task_id) + '-' + filename)
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
    header_count = 0
    for ln in lines:
        # don't process empty lines
        if(len(ln) == 0):
            continue

        # line in format "confidence || line"
        ocr_line = ln.split('||')
        conf, item_and_price = ocr_line[0], ocr_line[1].split(' ')

        # header is 1st x lines eg. FAIRPRICE XTRA
        if(header_count<HEADING_LINES_COUNT):
            header_count+=1
            item = ' '.join(item_and_price).strip()
            price = ''
        else:
            # assume price is last word in line
            item, price = ' '.join(item_and_price[:-1]).strip(), item_and_price[-1].strip()

        # Use case-insensitive fuzzy string matching to correct result
        predicted, ratio = FProcess.extractOne(item.upper(), choices)
        if ratio >= FLAG_CRITERIA_FUZZY and float(conf) >= FLAG_CRITERIA_OCR:
            output_line = predicted
            flag = ''
        else:
            output_line = item
            flag = 'Flag'

        results.append(output_line + ' ' + price)
        confidences.append(float(conf))
        ratios.append(ratio)
        flags.append(flag)


    zipped = zip(results, confidences, ratios, flags)

    # Write results with flags for manual checking
    if toWriteFile:
        mapped = map(lambda tup: ' || '.join(str(tup)), zipped)
        outfile = './results/' + filename + '.txt'
        with open(outfile, 'w') as f:
            f.write('\n'.join(mapped))


    return zipped


if __name__ == '__main__':
    if len(sys.argv<1):
        print 'Not enough arguments'
        sys.exit(1)
    else:
        process(sys.argv[1])