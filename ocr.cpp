#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main(int argc, char** argv)
{
    if(argc < 2){
        printf("Not enough arguments");
        return 1;
    }

    char* filename = argv[1];
    Pix *image = pixRead(filename);

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    api->Init(NULL, "eng");
    api->SetImage(image);
    api->SetVariable("tessedit_char_whitelist", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.-/");
    api->SetVariable("user_words_suffix ", "user-words");
    api->Recognize(NULL);

    tesseract::ResultIterator* ri = api->GetIterator();
    tesseract::PageIteratorLevel level = tesseract::RIL_TEXTLINE;
    if(ri != 0) {
        do {
            const char* line = ri->GetUTF8Text(level);
            float conf = ri->Confidence(level);
            if(line != 0) {
                printf("line: %s", line);
                printf("conf: %f\n", conf);
            }
            printf("------------------\n");
            delete[] line;
        } while((ri->Next(level)));
    }

    api->End();
    pixDestroy(&image);

    return 0;
}
