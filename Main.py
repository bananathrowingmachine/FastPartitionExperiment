"""
Collects and processes all the data from the complexity experiment. 

Made by bananathrowingmachine on April 29th, 2025.
"""
from experiment_code.ComplexityExperiment import ComplexityExperiment
from DataProcessor import DataProcessor, FullResultDType
from multiprocessing import Process, Queue, Event
import numpy as np
from inputimeout import TimeoutOccurred, inputimeout
from shutil import rmtree
from pathlib import Path
from queue import Empty

def collectData(queue: Queue, example: bool):
    """
    Allows data collection to happen in a seperate thread. Takes data and inputs it into the queue.

    :param queue: The data queue. Used to allow the computer to collect and process data simultaneously. Effectively the output of the method.
    :param example: Wether to generate a quick example set of data, since a real set is computationally expensive.
    """
    for n in range(1, 21):
        size = n * 5
        allResults = np.empty(1, dtype=FullResultDType)
        allResults[0]['setIntCount'] = size
        allResults[0]['recurseRun'] = (size <= 25)
        actualData = ComplexityExperiment.testProblemSize(size, genFilesDir, example)
        if actualData.shape != (21,):
            print(f"Expected shape {(21,)}, got {actualData.shape} unexpectedly. Experiment terminating.")
            break
        allResults[0]['actualData'] = actualData
        queue.put(allResults)

def processData(queue: Queue):
    """
    Allows data processing to happen in a seperate thread. Takes data inputted into the queue and heads off to processes it. Will wait idly until data arrives.

    :param queue: The data queue. Used to allow the computer to collect and process data simultaneously. Effectively the input of the method. Instantly calls the data processor when data is made available.
    """
    while keepGoing.is_set():
        try: 
            data = queue.get(timeout=0.25) # Attempts to process data every 0.25 seconds until the end of work signal of None is sent.
            DataProcessor.processData(genFilesDir, data)
        except Empty:
            continue

"""
The main method. Starts up the threads, flags, and gets everything moving. This is the file to run to start up everything else.

Do note that this program will also wipe all previously generated graphs, data tables, and recorded solution conflicts when run.
"""
queue = Queue()
scriptDir = Path(__file__).parent
genFilesDir = scriptDir / "generated files"
if genFilesDir.exists():
    rmtree(genFilesDir)
genFilesDir.mkdir()
keepGoing = Event()
keepGoing.set()
print("This program requires a lot of computation to run effectively. If the device you are running this on is not particularly good, you might run into issues.")
print("Therefore, by default this program will generate and graph a set of computationally cheap example data, however that data will be mostly randomly generated nonsense.")
print("Only generate a full legitimate set of data if your understand it will take a while, and will use all of your PC's resources.")
print(" ")
try:
    answer = inputimeout(prompt="That being said, press f to generate a full set of data, and press anything else to generate an example set. ", timeout=10)
    if answer.lower() == "f":
        try:
            fallBack = inputimeout(prompt="Full data collection will commence in 10 seconds if no further inputs are recieved. Press f again to reconfirm quickly.", timeout=10)
            if fallBack.lower() == "f":
                print("Full data collection has commenced.")
            else:
               print("Full data collection has been cancelld. Will use example data instead.") 
               answer = "e"
        except TimeoutOccurred:
            print("Full data collection has commenced.")
except TimeoutOccurred:
    print("Input timeout occured. Defaulting to example data.")
    answer = "e"
collector = Process(target=collectData, args=(queue, answer.lower() != "f"))
processor = Process(target=processData, args=(queue,))
collector.start()
processor.start()
collector.join()
keepGoing.clear() # Signals end of work.
processor.join()
