from experiment_code.complexityExperiment import complexityExperiment
from graphBuilder import graphBuilder
from multiprocessing import Process, Queue

def collectData(queue: Queue):
    """
    Allows data collection to happen in a seperate thread. Takes data and inputs it into the queue.

    :param queue: The data queue.
    """
    for n in range(1, 21):
        size = n * 5
        queue.put((size, complexityExperiment.testProblemSize, size <= 25))

def activateProcessData(queue: Queue):
    """
    Allows data processing to happen in a seperate thread. Takes data inputted into the queue to process.

    :param queue: The data queue.
    """
    while keepGoing:
        try:
            graphBuilder.processData(queue.get(timeout=0.1))
        except Queue.empty:
            continue

"""
The main method. Starts up the threads, flags, and gets everything moving.
"""
queue = Queue()
keepGoing = True
collector = Process(target=collectData, args=(queue,))
processor = Process(target=activateProcessData, args=(queue,))
collector.start()
processor.start()
collector.join()
keepGoing = False
processor.join()
