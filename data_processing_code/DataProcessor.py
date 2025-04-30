"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on [insert final date here].
"""
from data_processing_code.MiscDataCode import ResultsWrapper
import numpy as np
from pathlib import Path

class DataProcessor:
    def __init__(self, genFileDir: Path):
        """
        Simple data processor object. Processes the data and stores them in subdirectories of the one given to it during construction.

        :param genFileDir: The directory to store generated processed data in. Will create the sub directories for graphs and data tables if they do not exist.
        """
        self.genFileDir = genFileDir
        self.graphDir = self.genFileDir / "graphs"
        self.tableDir = self.genFileDir / "data tables"
        self.graphDir.mkdir(parents=True, exist_ok=True)
        self.tableDir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def processData(cls, genFileDir: Path, results: ResultsWrapper):
        """
        Wraps up object construction and data processing into a convienient single method.

        :param genFileDir: The upper directory for generated files to end up in. Will create sub directories if the ones it expects do not exist.
        :param data: The data to get processed. 
        """
        processor = cls(genFileDir)
        processor.createTablesAndGraphs(results)

    def createTablesAndGraphs(self, results: ResultsWrapper):
        """
        Processes the data. Can reference itself for easy access to the directories on where to put graphs and data tables.

        :param data: The data to be processed.
        """
        with open(self.graphDir / "graph.txt", "w") as f:
            # To make life easy for you, all of the directory stuff is handeld by my code. Inside this method just write self.graphDir / "graphName" to access any graph, or make a new one.
            # As demonstrated below, the same works for self.tableDir, for all the data tables. 
            f.write("File written to (hopefully) the correct directory.")

        # Results comes in the form "ResultsWrapper", which is a named tuple. It contains 3 fields and I hope to show you how to use them.
        # Each field is named "IntCount", "RawData", and "RanRecurse". 
        # You can access a field as shown below.
        rawData = results.RawData   
        # "RawData" is the 2D np.ndarray of size 21, with 5 elements, all of them accessible by row and by name, which is shown below. This has all of the data.

        # "IntCount" gives the amount of integers in the set tested. This will be each column in a data table or graph.
        with open(self.tableDir / f"testedSetSize{results.IntCount}.txt", "w") as f:
            
            # "RanRecurse" records data if Recursive Normal was run. The statement results.RanRecurse will always be True when Recursive Normal was run, and always be False when it is not.
            if results.RanRecurse:

                f.write("Sum Target Index, Absolute Sum Target, Memoized Crazy, Memoized Normal, Tabulated Normal, Recursive Normal\n")
                for i in range(21):

                    # Each row of the rawData can be extracted like this.
                    row = rawData[i]

                    # Mix of name-based and index-based access for the official data:
                    # 'memoCrazy' is index 1, tabNormal' is index 3, and 'recurseNormal' is index 5.

                    f.write(
                        f"{i}, {row['targetSum']}, {row[1]}, {row['memoNormal']}, {row[3]}, {row['recurseNormal']}\n")          

            # This else statement records data if results.RanRecurse is false, or in other words when recurse is not run. Additionally Recursive Normal being off will fill in it's columns with np.nan, which is fine to slap on a chart too.
            else:
                f.write("Sum Target Index, Absolute Sum Target, Memoized Crazy, Memoized Normal, Tabulated Normal\n")
                for i in range(21):
                    row = rawData[i]

                    # Another mix of name-based and index-based access for the official data:
                    # 'targetSum' is index 0 and 'memoNormal' is index 2.

                    f.write(f"{i}, {row[0]}, {row['memoCrazy']}, {row[2]}, {row['tabNormal']}\n")

            # Simply run Main.py and DON'T PRESS F, and then this file will generate some example data tables that are basic .txt files just to give you an example of what the data output after 1 collection looks like. 
            # Each generated .txt file is one round of data collection. You can find them (relative to the Main.py file) in "generated tables/data tables", which is a file directory.
            # If those file directories don't exist, the program will make them for you. Simply run it and it will create them if needed, as well as wipe all old data currently there.

            # If you have any questions let me know!