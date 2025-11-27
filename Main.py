"""
Main orchestrator for all the moving parts. Is also where the main function is located and is therefore what needs to run to run the entire program.
This program on a deeper level will delete the output subdirectories if they exist, recreate them (to clean out all old data), gets the necessary user input, then will run the data collector and processor, and move the data between the two.
Both the data collector and the data processor run on independent threads, and the complexity experiment will actually run multiple parallel threads as well.

Details on the data collector:
Due to how the complexity tester was designed, this file also maintains how many integers should be in the sets tested, starting from 5, and in increments of 5 going up to 100, and sends that to the complexity tester.
Additionally, it will send the complexity tester directory information for the small bit of output it produces, and if it should generate a quick example output or a full computationally expensive output.
After the complexity tester has produced results, this program will take them, wrap them up with a few other useful bits of information, then send it to the data processor for processing.
The entire process was designed to try and keep all computer science stuff away from the data processing as possible.

Details on the data processor:
The data processor will check for packaged data every 0.25 seconds, until the signal by the orchestrator that computation has stopped is sent. 
It will then send the packaged data completely unmodified to the data processing code, along with the same directory information given to the data collector.
Once in the data processing code, the processor will unpack the data, processes it, and then once done will return back to the orchestrator, waiting for another chunk of data.
Was designed to have as little code as possible to help my non comp sci major friend who does know how to graph in python.

Made by bananathrowingmachine on Nov 27th, 2025.
"""
from experiment_code.ComplexityExperiment import ComplexityExperiment
from data_processing_code.MainDataProcessor import MainDataProcessor
from data_processing_code.MiscDataCode import ResultsWrapper, DisagreeData
from data_processing_code.DisagreeProcessor import DisagreeProcessor

from multiprocessing import Process, Queue, Event
from inputimeout import TimeoutOccurred, inputimeout
from shutil import rmtree
from pathlib import Path
from queue import Empty
import sys

disagreeCount = 1

def collectData(queue: Queue, example: bool, speedy: bool):
    """
    Allows data collection to happen in a seperate thread. Takes data and inputs it into the queue.

    :param queue: The data queue. Used to allow the computer to collect and process data simultaneously. Effectively the output of the method.
    :param example: Wether to generate a quick example set of data, since a real set is computationally expensive.
    """
    noDisagrees = True
    for n in range(1, 21):
        size = n * 5
        try:
            fullResults = ComplexityExperiment.testProblemSize(size, example, speedy)
        except:
            print("Test process crashed. Terminating.")
            raise
        results = fullResults[0]
        queue.put(ResultsWrapper(size, None if size <= 25 else 2 ** size, results))
        disagreeList = fullResults[1]
        if len(disagreeList) != 0:
            noDisagrees = False
            queue.put(disagreeList)
    if noDisagrees:
        queue.put(None)

def processData(queue: Queue, keepGoing, genFilesDir: Path, speedy: bool):
    """
    Allows data processing to happen in a seperate thread. Takes data inputted into the queue and heads off to processes it. Will wait idly until data arrives.

    :param queue: The data queue. Used to allow the computer to collect and process data simultaneously. Effectively the input of the method. Instantly calls the data processor when data is made available.
    """
    if speedy:
        DataProcessor = MainDataProcessor(genFilesDir, (True, True, True, False, False, False, False))
    else:
        DataProcessor = MainDataProcessor(genFilesDir)
    while keepGoing.is_set() or not queue.empty():
        try: 
            data = queue.get(timeout=0.25)
            if data is None:
                DisagreeProcessor.noDisagreements(genFilesDir)
            elif isinstance(data, ResultsWrapper):
                DataProcessor.appendData(data)
            elif isinstance(data, list) and all(isinstance(item, DisagreeData) for item in data):
                global disagreeCount
                DisagreeProcessor.processBulkDisagreements(genFilesDir, data, disagreeCount)
                disagreeCount += len(data)
        except Empty:
            continue
        except KeyboardInterrupt:
            DataProcessor.outputTableData()
            break
    DataProcessor.outputImageData()

"""
The main method. Starts up the threads, flags, and gets everything moving. This is the file to run to start up everything else.

Do note that this program will also wipe all previously generated graphs, data tables, and recorded solution conflicts when run.
"""
def main():
    queue = Queue()
    genFilesDir = Path(__file__).resolve().parent / "generated_files"
    if genFilesDir.exists():
        rmtree(genFilesDir)
        if sys.platform == 'win32': time.sleep(1)
    genFilesDir.mkdir(parents=True, exist_ok=True)
    if sys.platform == 'win32': os.chmod(genFilesDir, 0o777)
    keepGoing = Event()
    keepGoing.set()
    print("This program takes a long time to complete. To help with that below are a few options that can sped up execution but don't give the full results.")
    speedy = False
    try:
        answer = inputimeout("Active the speedy but incomplete version (will only run the 2 fastest algorithms)? [Y/N] \n", 10)
        if answer.lower() == "y":
            speedy = True
            print("A sped up set of data will be provided.")
        else:
            print("The complete set of data will be provided.") 
    except TimeoutOccurred:
        print("Input timeout occured. Defaulting to complete data.")
    example = False
    try:
        answer = inputimeout("Activate the example data generator (will generate mostly random numbers in place of actual results)? [Y/N] \n", 10)
        if answer.lower() == "y":
            example = True
            print("A set of example data will be provided.") 
        else:
            print("A regular set of data will be provided.")
    except TimeoutOccurred:
        print("Input timeout occured. Defaulting to regular data.")
    try:
        collector = Process(target=collectData, args=(queue, example, speedy))
        processor = Process(target=processData, args=(queue, keepGoing, genFilesDir, speedy))
    except KeyboardInterrupt:
        keepGoing.clear()
        raise
    else:
        collector.start()
        processor.start()
        collector.join()
        keepGoing.clear() # Signals end of work to the data processor.
        print("Data collection has finished. Finishing up processing.")
        processor.join()
        print("All processing has been completed. Closing.")
        sys.exit(0)

if __name__ == '__main__':
    """
    Prepares all the extra stuff needed to run this on windows.
    """
    if sys.platform == 'win32':
        from multiprocessing import freeze_support
        freeze_support()
        import os
        import time
    main()
