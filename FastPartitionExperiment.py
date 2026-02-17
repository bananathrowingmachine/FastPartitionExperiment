"""
Main orchestrator for all the moving parts. Is also where the main function is located and is therefore what needs to run to run the entire program.
This program on a deeper level will delete the output subdirectories if they exist, recreate them (to clean out all old data), gets the necessary user input, then will run the data collector and processor, and move data around.
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

Made by bananathrowingmachine on Feb 17, 2026.
"""
from experiment_code.ComplexityExperiment import ComplexityExperiment
from data_processing_code.MainDataProcessor import MainDataProcessor
from data_processing_code.MiscDataCode import ResultsWrapper, DisagreeData, AlgoNames
from data_processing_code.DisagreeProcessor import DisagreeProcessor

from multiprocessing import Process, Queue, Event
from shutil import rmtree
from pathlib import Path
from queue import Empty
import argparse
import sys
import os
import glob
from cffi import FFI

disagreeCount = 1

def collectData(queue: Queue, args):
    """
    Allows data collection to happen in a seperate thread. Takes data and inputs it into the queue.

    :param queue: The data queue. Used to allow the computer to collect and process data simultaneously. Effectively the output of the method.
    :param args: The command line arguments passed when the program started.
    """
    sheets = None
    if args.example:
        import pandas as pd
        import urllib.error
        try:
            if args.reduced:
                excelFile = pd.ExcelFile('https://github.com/bananathrowingmachine/FastPartitionExperimentDocs/blob/main/Previous%20Results/Speedy%20Runs/Nov%2023%2C%202025%20r1/data_tables/Results.xlsx?raw=true')
                sheets = [pd.read_excel(excelFile, sheet_name='New Memoized Crazy'), pd.read_excel(excelFile, sheet_name='Old Memoized Crazy')]
            else:
                excelFile = pd.ExcelFile('https://github.com/bananathrowingmachine/FastPartitionExperimentDocs/blob/main/Previous%20Results/Full%20Runs/May%2026%2C%202025/data_tables/Results.xlsx?raw=true')
                sheets = [pd.read_excel(excelFile, sheet_name='Memoized Crazy'), pd.read_excel(excelFile, sheet_name='Memoized Normal'), pd.read_excel(excelFile, sheet_name='Tabulated Crazy'), 
                          pd.read_excel(excelFile, sheet_name='Tabulated Normal'), pd.read_excel(excelFile, sheet_name='Recursive Normal')]
            
        except (urllib.error.URLError, ConnectionError):
            print('()~~}|[==>>--:>-    Could not download data. Resorting to generating random data.    -<:--<<==]|{~~()')
    else:
        print("|[==>>--:>- ============================================================================= -<:--<<==]|")
    noDisagrees = True
    for n in range(1, 21):
        size = n * 5
        try:
            fullResults = ComplexityExperiment.testProblemSize(size, args, sheets)
        except:
            print("()~~}|[==>>--:>-                  Test process crashed. Terminating.                 -<:--<<==]|{~~()")
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
        DataProcessor = MainDataProcessor(genFilesDir, (AlgoNames.TargetSum, AlgoNames.NewMemoizedCrazy, AlgoNames.OldMemoizedCrazy))
    else:
        DataProcessor = MainDataProcessor(genFilesDir, (AlgoNames.TargetSum, AlgoNames.NewMemoizedCrazy, AlgoNames.MemoizedNormal, AlgoNames.TabulatedCrazy, AlgoNames.TabulatedNormal, AlgoNames.RecursiveNormal))
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

def main():
    """
    The main method. Starts up the threads, flags, and gets everything moving. This is the file to run to start up everything else.

    Do note that this program will also wipe all previously generated graphs, data tables, and recorded solution conflicts when run.
    """
    parser = argparse.ArgumentParser(description="Driver/main for my partition algorithm complexity experiment.", add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit. No files or folders will be created or deleted.')
    parser.add_argument('-c', '--clean', action='store_true', help="Clean then C binaries then exits. If used with --python, all __pycache__ will be cleaned as well.")
    parser.add_argument('-e', '--example', action='store_true', help="Output old/outdated example data downloaded from GitHub if online, or randomly generated data if offline. Will not attempt to compile C binaries.")
    parser.add_argument('-r', '--reduced', action='store_true', help="Run the reduced test suite. If used with --example will output example data of the reduced test suite.")
    parser.add_argument('-p', '--python', action='store_true', help="Run the Python versions of the algorithms instead of the C versions. Will not attempt to compile C binaries.")
    args = parser.parse_args()
    if sys.platform == 'win32':
        from multiprocessing import freeze_support
        freeze_support()
    cParentDir = Path(__file__).resolve().parent / "experiment_code" / "versions"
    if args.clean:
        rmtree(cParentDir / "c_bin", ignore_errors=True)
        if args.python:
            for path in Path('.').rglob('__pycache__'):
                rmtree(path)
        sys.exit(0)
    if not (args.python or args.example):
        buildCLibrary(cParentDir)
    genFilesDir = Path(__file__).resolve().parent / "generated_files"
    rmtree(genFilesDir, ignore_errors=True)
    genFilesDir.mkdir(parents=True, exist_ok=True)
    queue = Queue()
    keepGoing = Event()
    keepGoing.set()
    try:
        collector = Process(target=collectData, args=(queue, args))
        processor = Process(target=processData, args=(queue, keepGoing, genFilesDir, args.reduced))
    except KeyboardInterrupt:
        keepGoing.clear()
        raise
    else:
        collector.start()
        processor.start()
        collector.join()
        keepGoing.clear() # Signals end of work to the data processor.
        print("()~~}|[==>>--:>-        Data collection has finished. Finishing up processing.       -<:--<<==]|{~~()")
        processor.join()
        print("()~~}|[==>>--:>-              All processing has been completed. Exiting.            -<:--<<==]|{~~()")
        sys.exit(0)

def buildCLibrary(parentDir: Path):
    """
    Builds the C library.
    
    :param targetDir: The folder for the C binaries.
    """
    targetDir = parentDir / "c_bin"
    sourceDir = parentDir / "c"
    filesToClean = []
    for name in ["MemoizedNormal", "NewMemoizedCrazy", "OldMemoizedCrazy", "RecursiveNormal", "TabulatedCrazy", "TabulatedNormal"]:
        binary = next(targetDir.glob(f"_{name}.*.{'pyd' if os.name == 'nt' else 'so'}"), None)
        srcFile = sourceDir / f"{name}.c"
        if binary is None or srcFile.stat().st_mtime > binary.stat().st_mtime:
            ffibuilder = FFI()
            ffibuilder.cdef(""" 
                typedef unsigned char uint8_t;
                            
                typedef struct {
                    int iterationCount;
                    uint8_t result;
                } Output;

                Output testIterations(int* inputList, int listLength);
            """)

            ffibuilder.set_source(
                f"_{name}",
                f"""
                #include "{name}.c"
                """, 
                include_dirs=[str(sourceDir)]            
            )
            ffibuilder.compile(tmpdir=targetDir)
            filesToClean += glob.glob(os.path.join(targetDir, f"_{name}.[co]"))
            filesToClean += glob.glob(os.path.join(targetDir, f"_{name}.obj"))

    for f in filesToClean:
        try: os.remove(f)
        except OSError: pass

if __name__ == '__main__':
    main()
