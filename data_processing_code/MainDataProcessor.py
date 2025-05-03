"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on [insert final date here].
"""
from data_processing_code.MiscDataCode import ResultsWrapper
import numpy as np
import pandas as pd
from pathlib import Path

class MainDataProcessor:
    """
    Data processor class. In reality just a easy way to make the subdirectories for generated data and store the values easily.
    """
    def __init__(self, genFilesDir: Path):
        """
        Simple regular data processor object. Processes the data and stores it in subdirectories of the one given to it during construction.

        :param genFilesDir: The directory to store generated processed data in. Will create the sub directories for graphs and data tables if they do not exist.
        """
        graphsDir = genFilesDir / "graphs"
        graphsDir.mkdir(parents=True, exist_ok=True)
        self.singleAlgGraphsDir = graphsDir / "single algorithm graphs"
        self.otherGraphsDir = graphsDir / "other graphs"
        self.singleAlgGraphsDir.mkdir(parents=True, exist_ok=True)
        self.otherGraphsDir.mkdir(parents=True, exist_ok=True)

        tablesDir = genFilesDir / "data tables"
        tablesDir.mkdir(parents=True, exist_ok=True)
        self.singleAlgTablesDir = tablesDir / "single algorithm tables"
        self.otherTablesDir = tablesDir / "other tables"
        self.percentTablesDir = tablesDir / "percentage tables"
        self.singleAlgTablesDir.mkdir(parents=True, exist_ok=True)
        self.otherTablesDir.mkdir(parents=True, exist_ok=True)
        self.percentTablesDir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def processData(cls, genFilesDir: Path, results: ResultsWrapper):
        """
        Processes the data. Uses a DataProcessor object to easily create and reference all graph and table directories.

        :param genFilesDir: The upper directory for generated files to end up in. Will create sub directories if the ones it expects do not exist.
        :param data: The data to get processed. 
        """
        dirs = cls(genFilesDir)

        # Results comes in the form "ResultsWrapper", which is a named tuple. It contains 3 fields and I hope to show you how to use them.
        # Each field is named "IntCount", "RawData", and "RecurseEstimate". 
        # You can access a field as shown below.
        rawData = results.RawData   
        # "RawData" is the 2D np.ndarray of size 21, with 5 elements, all of them accessible by row and by name, which is shown below. This has all of the data.

        # "IntCount" gives the amount of integers in the set tested. This will be each column in a data table or graph.
        with open(dirs.singleAlgTablesDir / f"testedSetSize{results.IntCount}.txt", "w") as f:

            f.write("Sum Target Index, Absolute Sum Target, Memoized Crazy, Memoized Normal, Tabulated Normal, Recursive Normal\n")

            # Additionally, the logic for recursive normal is rather easy by using results.RecurseEstimate. It will either be a number or None, and will always be the opposite of the results for Recursive Normal.
            # Why is that? Well first, results.RecurseEstimate is None is very simply logic that tells you if Recursive Normal was run. Take a look below for a example.
            # Second, while Recursive Normal is quite slow, it's by far the most predictable, so once it gets too high, results.RecurseEstimate will become a estimated value that you can sub in for np.nan results, as shown a bit further down.
            # Therefore we can put the data in tables and graphs for Recursive Normal just like every other algorithm variation, using the estimation, we'll just want to mark what values are estimations.

            if results.RecurseEstimate is None:
                f.write("Small enough for recursive normal.\n")
            else:
                f.write("Too big for recursive normal, used a prediction instead.\n")
            
            for i in range(21):

                # Each row of the rawData can be extracted like this.
                row = rawData[i]

                # Mix of name-based and index-based access for the official data:
                # 'memoCrazy' is index 1, and 'tabNormal' is index 3. Using both interchangably is completely fine.

                f.write(f"{i}, {row['targetSum']}, {row[1]}, {row['memoNormal']}, {row[3]}, {row['recurseNormal'] if results.RecurseEstimate is None else results.RecurseEstimate}\n")

        # Simply run Main.py and DON'T PRESS F, and then this file will generate some example data tables that are basic .txt files just to give you an example of what the data output after 1 collection looks like. 
        # Each generated .txt file is one round of data collection. You can find them (relative to the Main.py file) in "generated tables/data tables", which is a file directory.
        # If those file directories don't exist, the program will make them for you. Simply run it and it will create them if needed, as well as wipe all old data currently there.