## Requirements
- Python 2.7
- tesseract 3.04
- SimpleCV 1.3

#### Python packages
- fuzzywuzzy 0.8.0
- python-Levenshtein 0.12.0

## Build
`g++ -o ocr ocr.cpp -ltesseract -llept`

## Run
`python2 main.py`


## Process
1. Push colors towards black and white using colorDistance
2. Replace values < THRESH_LOW with black, values > THRESH_HIGH with white using stretch
4. Scale image to 2x
5. OCR using tesseract
6. Prediction using fuzzy string matching
7. If OCR confidence > 50% and fuzzy confidence > 50%
    a. Correct output with prediction from fuzzy
    b. Else, flag line
