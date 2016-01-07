import script
from fuzzywuzzy import fuzz

filenames = [
    'receipt00.jpg',
    'receipt01.jpg',
    'receipt02.jpg'
]

for name in filenames:
    print('Processing ' + name + '...')
    print('Actual || Expected || % Accuracy')
    
    diff = []

    # Process each image
    actual = script.process(name)
    with open('./expected/' + name + '.txt', 'r') as f:
        expected = f.read().strip().split('\n')

    # Calculate % accuracy
    for i in xrange(len(expected)):
        aline = actual[i]
        eline = expected[i].strip()
        # ignore unnecessary lines eg. address
        if(eline.startswith('!')):
            continue

        acc = fuzz.ratio(aline, eline)
        diff.append(acc)
        print ' || '.join((aline, eline, str(acc)))

    # average accuracy across all lines
    total = reduce(lambda x, y: x+y, diff)
    avg = total/len(diff)

    print('Average accuracy: ' + str(avg) + '%\n')
