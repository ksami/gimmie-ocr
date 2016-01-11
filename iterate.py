import multiprocessing
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
    processes = []
    queues = []

    filename = filenames[0]
    print filename

    best_conf = 0
    best_ratio = 0
    best_result = None

    proc_id = 0

    # Create processes with each combination of params
    for rotate_angle in xrange(PARAM_ROTATE_ANGLE_MIN, PARAM_ROTATE_ANGLE_MAX, PARAM_ROTATE_ANGLE_DELTA):
        for thresh_low in xrange(PARAM_STRETCH_THRESH_MIN_LOW, PARAM_STRETCH_THRESH_MAX_LOW, PARAM_STRETCH_THRESH_DELTA_LOW):
            for thresh_high in xrange(thresh_low, PARAM_STRETCH_THRESH_MAX_HIGH, PARAM_STRETCH_THRESH_DELTA_HIGH):
                queue = multiprocessing.Queue()
                proc = multiprocessing.Process(target=script.process, args=(str(proc_id), filename, thresh_low, thresh_high, rotate_angle, queue))
                proc_id += 1

                processes.append(proc)
                queues.append(queue)


    print 'total number of processes: ' + str(len(processes))

    # Wait for all processes to complete
    for i in xrange(0,len(processes),NUM_PROCESSES):
        print 'running processes ' + str(i) + ' to ' + str(i+NUM_PROCESSES-1)
        for j in xrange(NUM_PROCESSES):
            if i+j<len(processes):
                processes[i+j].start()
        for j in xrange(NUM_PROCESSES):
            if i+j<len(processes):
                processes[i+j].join()


    for queue in queues:
        results = queue.get()

        if len(results) == 0:
            continue

        unzipped = [list(tup) for tup in zip(*results)]

        # Median values of OCR conf and fuzzy ratio
        # conf = median(unzipped[1])
        # ratio = median(unzipped[2])
        conf = average(unzipped[1])
        ratio = average(unzipped[2])

        # Criteria for taking result as best
        # TODO: check on line by line basis
        # which is the line to compare against?
        # length of results list not constant
        if conf > best_conf or ratio > best_ratio:
            best_result = results


    for res in best_result:
        print reduce(lambda s,t: ' || '.join((str(s),str(t))), res)


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