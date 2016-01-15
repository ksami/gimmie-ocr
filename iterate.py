from multiprocessing import Pool
import script
from fuzzywuzzy import fuzz

# PARAM_STRETCH_THRESH_LOW = 140  # range 0-255
# PARAM_STRETCH_THRESH_HIGH = 140  # range 0-255, should be above LOW
PARAM_STRETCH_THRESH_DELTA_LOW = 20
PARAM_STRETCH_THRESH_DELTA_HIGH = 20
PARAM_STRETCH_THRESH_MIN_LOW = 100
# PARAM_STRETCH_THRESH_MIN_HIGH = PARAM_STRETCH_THRESH_MIN_LOW + PARAM_STRETCH_THRESH_DELTA_HIGH  # should be higher than current low
PARAM_STRETCH_THRESH_MAX_HIGH = 180
PARAM_STRETCH_THRESH_MAX_LOW = PARAM_STRETCH_THRESH_MAX_HIGH - PARAM_STRETCH_THRESH_DELTA_LOW

# PARAM_ROTATE_ANGLE = 0  # range -360-360
PARAM_ROTATE_ANGLE_DELTA = 5
PARAM_ROTATE_ANGLE_MIN = -10
PARAM_ROTATE_ANGLE_MAX = 10

NUM_PROCESSES = 4  # if too high, will run out of memory

filenames = [
    'receipt00.jpg',
    'receipt01.jpg',
    'receipt02.jpg'
]



def main():
    pool = Pool(processes=NUM_PROCESSES)
    params = []

    filename = filenames[0]
    print 'Filename is: ' + filename

    task_id = 0

    # Create tuples with each combination of params
    for rotate_angle in xrange(PARAM_ROTATE_ANGLE_MIN, PARAM_ROTATE_ANGLE_MAX, PARAM_ROTATE_ANGLE_DELTA):
        for thresh_low in xrange(PARAM_STRETCH_THRESH_MIN_LOW, PARAM_STRETCH_THRESH_MAX_LOW, PARAM_STRETCH_THRESH_DELTA_LOW):
            for thresh_high in xrange(thresh_low, PARAM_STRETCH_THRESH_MAX_HIGH, PARAM_STRETCH_THRESH_DELTA_HIGH):
                params.append((filename, task_id, thresh_low, thresh_high, rotate_angle))
                task_id += 1


    # Run processes
    print 'Total number of tasks: ' + str(task_id)

    results = pool.map(unpackTupleIntoFunc, params)

    print 'Tasks have finished running, output is:\n\n'


    # Process results 
    best_conf = 0
    best_ratio = 0
    best_result = None

    for result in results:

        if len(result) == 0:
            continue

        unzipped = [list(tup) for tup in zip(*result)]

        # Median or average values of OCR conf and fuzzy ratio
        # conf = median(unzipped[1])
        # ratio = median(unzipped[2])
        conf = average(unzipped[1])
        ratio = average(unzipped[2])

        # Criteria for taking result as best
        # TODO: check on line by line basis
        # which is the line to compare against?
        # length of results list not constant
        # use fuzzy to find?
        if conf > best_conf or ratio > best_ratio:
            best_result = result


    for res in best_result:
        print reduce(lambda s,t: ' || '.join((str(s),str(t))), res)


    pool.close()
    pool.join()


# Unpack tuple in params before applying to script.process
def unpackTupleIntoFunc(args):
    return script.process(*args)


def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0


def average(lst):
    return sum(lst)/len(lst)

if __name__ == '__main__':
    main()