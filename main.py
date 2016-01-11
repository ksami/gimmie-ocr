import script
from fuzzywuzzy import fuzz

filenames = [
    'receipt00.jpg',
    'receipt01.jpg',
    'receipt02.jpg'
]

def test():
    for name in filenames:
        print('Processing ' + name + '...')
        print('Actual || Expected || % Accuracy || isFlagged')
        
        diff = []

        # Process each image
        actual = script.process(name, isFeedback=False, toWriteFile=True)
        with open('./expected/' + name + '.txt', 'r') as f:
            expected = f.read().strip().split('\n')

        # Calculate % accuracy
        for i in xrange(len(expected)):
            aline = actual[i][0]
            flagged = actual[i][3]
            eline = expected[i].strip()
            # ignore unnecessary lines eg. address
            if(eline.startswith('!')):
                continue

            acc = fuzz.ratio(aline, eline)
            diff.append(acc)
            print ' || '.join((aline, eline, str(acc), flagged))

        # average accuracy across all lines
        total = reduce(lambda x, y: x+y, diff)
        avg = total/len(diff)

        print('Average accuracy: ' + str(avg) + '%\n')


if __name__ == '__main__':
    test()