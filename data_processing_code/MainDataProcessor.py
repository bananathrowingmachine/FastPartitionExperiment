"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on May 22th, 2025.
"""
from data_processing_code.MiscDataCode import ResultsWrapper
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

class MainDataProcessor:
    """
    Data processor class, that stores, saves, and handles all the data tables and graphs. Best if created once and appendData is called repeatedly.
    """
    def __init__(self, genFilesDir: Path):
        """
        Simple regular data processor object. Processes the data and stores it in subdirectories of the one given to it during construction.

        :param genFilesDir: The directory to store generated processed data in. Will create the sub directories for graphs and data tables if they do not exist.
        """
        self.graphsDir = genFilesDir / "graphs"
        self.tablesDir = genFilesDir / "data_tables"

        for directory in [self.graphsDir, self.tablesDir]:
            directory.mkdir(parents=True, exist_ok=True)

        self.xValues = [f'{i}' for i in range(5, 101, 5)]
        self.yValues = [f'{i}' for i in range(21)]
        self.zNames: dict[str, str] = {'memoCrazy': 'Memoized Crazy', 'memoNormal': 'Memoized Normal', 'tabCrazy': 'Tabulated Crazy', 'tabNormal': 'Tabulated Normal', 'recurseNormal': 'Recursive Normal', 'targetSum': 'Absolute Sum Target'}

        self.dataTables: dict[str, pd.DataFrame] = {zNameShort: pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64) for zNameShort in self.zNames.keys()}
        self.dataTables['targetSum'] = pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.int64)

    def appendData(self, results: ResultsWrapper) -> None:
        """
        Appends a new chunk of data to the appropriate x rows for each algorithm.
        Regenerates the data tables and graphs each time in case the program is stopped before it completes.

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
        for zNameShort in self.zNames.keys():
            if zNameShort != 'targetSum':
                x = results.IntCount
                y = np.arange(0, 21)
                x, y = np.meshgrid(x, y)
                x = x.ravel()
                y = y.ravel()
                z = rawData[zNameShort] if zNameShort != 'recurseNormal' or results.RecurseEstimate == None else [results.RecurseEstimate for _ in range(21)]

                # Height of the bars
                dx = dy = 10
                dz = np.random.randint(1, 10, size=len(x))

                # Create 3D plot
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                # Plot bars
                ax.bar3d(x, y, z, dx, dy, dz, color='skyblue', edgecolor='black')

                # Labels
                ax.set_xlabel('Set Integer Count')
                ax.set_ylabel('Absolute Sum Target Index')
                ax.set_zlabel('Average Iteration Count')
                ax.set_title(f'{self.zNames[zNameShort]} Graph')

                if sys.platform == 'win32': plt.show()

                plt.savefig(self.graphsDir / f'{self.zNames[zNameShort]} Graph.png')  
                plt.close()  


                