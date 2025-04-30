"""
Made by bananathrowingmachine and Earthquakeshaker2 on [insert final date here].
"""
from experiment_code.ComplexityExperiment import ResultDType
import numpy as np
from pathlib import Path

FullResultDType = np.dtype([
    ('setIntCount', np.int64),
    ('actualData', (ResultDType, 21)), 
    ('recurseRun', np.bool_),
])

class DataProcessor:
    def __init__(self, genFileDir: Path):
        """
        Simple data processor object. Processes the data and stores them in subdirectories of the one given to it during construction.

        :param genFileDir: The directory to store generated processed data in. Will create the sub directories for graphs and data tables if they do not exist.
        """
        self.genFileDir = genFileDir
        self.graphDir = self.genFileDir / "graphs"
        self.tableDir = self.genFileDir / "data tables"
        self.graphDir.mkdir(exist_ok=True)
        self.tableDir.mkdir(exist_ok=True)

    @classmethod
    def processData(cls, genFileDir: Path, data: np.ndarray):
        """
        Wraps up object construction and data processing into a convienient single method.

        :param genFileDir: The upper directory for generated files to end up in. Will create sub directories if the ones it expects do not exist.
        :param data: The data to get processed. 
        """
        processor = cls(genFileDir)
        processor.createTablesAndGraphs(data)

    def createTablesAndGraphs(self, data: np.ndarray):
        """
        Processes the data. Can reference itself for easy access to the directories on where to put graphs and data tables.

        :param data: The data to be processed.
        """
        with open(self.graphDir / "graph.txt", "w") as f:
            f.write("Test graph file!")
        with open(self.tableDir / "table.txt", "w") as f:
            f.write(str(data))