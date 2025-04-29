from experiment_code.complexityExperiment import complexityExperiment
import graphBuilder as gb
from multiprocessing import Process, Queue
import time

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
    Allows data processing to happen in a seperate thread. Takes data inputted into the queue and heads off to processes it. Will wait idly until data arrives.

    :param queue: The data queue.
    """
    while keepGoing:
        gb.processData(queue.get())

"""
The main method. Starts up the threads, flags, and gets everything moving. This is the file to run to start up everything else.
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
