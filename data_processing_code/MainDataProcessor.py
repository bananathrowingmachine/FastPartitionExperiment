"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on May 19th, 2025.
"""
from data_processing_code.MiscDataCode import ResultsWrapper
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

        self.tablesDir = genFilesDir / "data_tables"

        for directory in [graphsDir, self.singleAlgGraphsDir, self.otherGraphsDir, self.tablesDir]:
            directory.mkdir(parents=True, exist_ok=True)

        self.xValues = [f'{i}' for i in range(5, 101, 5)]
        self.yValues = [f'{i}' for i in range(21)]
        self.zNames: dict[str, str] = {'memoCrazy': 'Memoized Crazy', 'memoNormal': 'Memoized Normal', 'tabCrazy': 'Tabulated Crazy', 'tabNormal': 'Tabulated Normal', 'recurseNormal': 'Recursive Normal', 'targetSum': 'Absolute Sum Target'}

        self.dataTables: dict[str, pd.DataFrame] = {zNameShort: pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64) for zNameShort in self.zNames.keys()}
        self.dataTables['targetSum'] = pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.int64)

    def appendData(self, results: ResultsWrapper) -> None:
        """
        Appends a new chunk of data to the appropriate x rows for each algorithm.

        :param data: The data to get processed, wrapped up with the x index and estimated exponential time value.
        """
        xIndex = f'{results.IntCount}'
        rawData = results.RawData   

        for zNameShort in self.zNames.keys():
            if zNameShort == 'recurseNormal' and results.RecurseEstimate is not None:
                yData = np.array([results.RecurseEstimate for _ in range(21)])
            else:
                yData = np.array([row[zNameShort] for row in rawData])
            self.dataTables[zNameShort].loc[xIndex] = yData

        with pd.ExcelWriter(self.tablesDir / "results.xlsx", engine="xlsxwriter") as writer:
            for zNameShort, dataFrame in self.dataTables.items():
                sheetName = self.zNames[zNameShort]
                dataFrame.T.to_excel(writer, sheet_name=sheetName)
                worksheet = writer.sheets[sheetName]
                        
                for colIndex, column in enumerate(dataFrame.columns):
                    maxLength = max((len(f"{x:.15g}") for x in dataFrame[column]), default=0)
                    maxLength = max(maxLength, len(str(column)))
                    newWidth = min(maxLength, 20) + 2
                    worksheet.set_column(colIndex, colIndex, newWidth)
                
        # Sample data
        x = np.array([1, 2, 3, 4])
        y = np.array([1, 2, 3])
        x, y = np.meshgrid(x, y)
        x = x.ravel()
        y = y.ravel()
        z = np.zeros_like(x)

        # Height of the bars
        dx = dy = 0.4
        dz = np.random.randint(1, 10, size=len(x))

        # Create 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot bars
        ax.bar3d(x, y, z, dx, dy, dz, color='skyblue', edgecolor='black')

        # Labels
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.set_title('3D Bar Graph Example')

        plt.show()


                