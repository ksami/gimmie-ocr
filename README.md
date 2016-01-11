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
`python2 iterate.py` for iterative version to decide parameter values


## Process
1. Push colors towards black and white using colorDistance
2. Replace values < stretch_thresh_low with black, values > stretch_thresh_high with white using stretch
4. Scale image to 2x
5. Rotate image by rotate_angle degrees
6. OCR using tesseract
7. Prediction using fuzzy string matching
8. If OCR confidence > 50% and fuzzy confidence > 50%
    a. Correct output with prediction from fuzzy
    b. Else, flag line
9. Run steps 1-8 varying `stretch_thresh_low`, `stretch_thresh_high` and `rotate_angle`, if median OCR confidence > best or median fuzzy confidence > best
    a. Use current set of lines as best result
    b. Keep best result