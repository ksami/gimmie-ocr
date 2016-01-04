import script
import difflib

filenames = [
    'receipt00.jpg',
    'receipt01.jpg',
    'receipt02.jpg'
]

print('Accuracy percentages\n')

for name in filenames:
    print('Processing ' + name + '...')
    
    diff = []

    actual = script.process(name).split('\n')
    with open('./expected/' + name + '.txt', 'r') as f:
        expected = f.read().split('\n')

    for i in xrange(len(expected)):
        aline = actual[i]
        eline = expected[i]
        # ignore unnecessary lines
        if(eline.startswith('!')):
            continue

        seq = difflib.SequenceMatcher(None, eline, aline)
        diff.append(seq.ratio()*100)

    total = reduce(lambda x, y: x+y, diff)
    avg = total/len(diff)

    print(name + ': ' + str(avg) + '\n')
