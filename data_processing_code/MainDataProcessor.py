"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on May 9th, 2025.
"""
from data_processing_code.MiscDataCode import ResultsWrapper
import numpy as np
import pandas as pd
from pathlib import Path
from tabulate import tabulate

class MainDataProcessor:
    """
    Data processor class, that stores, saves, and handles all the data tables and graphs. Best if created once and appendData is called repeatedly.
    """
    def __init__(self, genFilesDir: Path):
        """
        Simple regular data processor object. Processes the data and stores it in subdirectories of the one given to it during construction.

        :param genFilesDir: The directory to store generated processed data in. Will create the sub directories for graphs and data tables if they do not exist.
        """
        graphsDir = genFilesDir / "graphs"
        self.singleAlgGraphsDir = graphsDir / "single_algorithm_graphs"
        self.otherGraphsDir = graphsDir / "other_graphs"

        tablesDir = genFilesDir / "data_tables"
        self.singleAlgTablesDir = tablesDir / "single_algorithm_tables"
        self.otherTablesDir = tablesDir / "other_tables"

        for directory in [graphsDir, self.singleAlgGraphsDir, self.otherGraphsDir, tablesDir, self.singleAlgTablesDir, self.otherTablesDir]:
            directory.mkdir(parents=True, exist_ok=True)

        self.xValues = [f'x_{i}' for i in range(5, 101, 5)]
        self.yValues = [f'y_{i}' for i in range(21)]
        self.zNames = ['targetSum', 'memoCrazy', 'memoNormal', 'tabCrazy', 'tabNormal', 'recurseNormal']

        self.dataTables: dict[str, pd.DataFrame] = {
            zName: pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64)
            for zName in self.zNames
        }
        self.dataTables['targetSum'] = pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.int64)

    def appendData(self, results: ResultsWrapper) -> None:
        """
        Appends a new chunk of data to the appropriate x rows for each algorithm.

        :param data: The data to get processed, wrapped up with the x index and estimated exponential time value.
        """
        xIndex = results.IntCount
        rawData = results.RawData   

        for zName in self.zNames:
            yData = np.array([row[zName] for row in rawData])
            self.dataTables[zName].loc[xIndex] = yData

        with pd.ExcelWriter(self.singleAlgTablesDir / "results.xlsx", engine='openpyxl') as writer:
            for zName, df in self.dataTables.items():
                df.to_excel(writer, sheet_name=zName)
        