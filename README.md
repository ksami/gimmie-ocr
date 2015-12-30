## Requirements
- Python 2.7
- tesseract 3.04
- pytesseract 0.1.6
- SimpleCV 1.3.0
- fuzzywuzzy 0.8.0

## Build
`g++ -o ocr ocr.cpp -ltesseract -llept`

## Run
`./ocr images/receipt.jpg`