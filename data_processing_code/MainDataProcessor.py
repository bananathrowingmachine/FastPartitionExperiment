"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on May 22nd, 2025.
"""
from data_processing_code.MiscDataCode import ResultsWrapper, DataProcessingInfo
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

        self.xValues = [i for i in range(5, 101, 5)]
        self.yValues = [i for i in range(21)]
        
        self.algorithmData: dict[str, DataProcessingInfo] = {}

        self.algorithmData['memoCrazy'] = DataProcessingInfo('Memoized Crazy', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.algorithmData['memoNormal'] = DataProcessingInfo('Memoized Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.algorithmData['tabCrazy'] = DataProcessingInfo('Tabulated Crazy', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.algorithmData['tabNormal'] = DataProcessingInfo('Tabulated Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.algorithmData['recurseNormal'] = DataProcessingInfo('Recursive Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        self.algorithmData['targetSum'] = DataProcessingInfo('Absolute Target Sum', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.int64), 0, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

    def appendData(self, results: ResultsWrapper) -> None:
        """
        Appends a new chunk of data to the appropriate x rows for each algorithm.
        Regenerates the data tables and graphs each time in case the program is stopped before it completes. Therefore the latest x value of processes data will always be visible while waiting for the entire set of data to complete.

        :param data: The data to get processed, wrapped up with the x index and estimated exponential time value.
        """
        xIndex = results.IntCount
        rawData = results.RawData   

        writer = pd.ExcelWriter(self.tablesDir / "Results.xlsx", engine="xlsxwriter") 
        
        for algoName in self.algorithmData.keys():
            currFrame = self.algorithmData[algoName].DataFrame
            currRealName = self.algorithmData[algoName].OfficialName

            if algoName == 'recurseNormal' and results.RecurseEstimate is not None:
                yData = np.array([results.RecurseEstimate for _ in range(21)])
            else:
                yData = np.array([row[algoName] for row in rawData])
            currFrame.loc[xIndex] = yData

            sheetName = currRealName
            currFrame.T.to_excel(writer, sheet_name=sheetName)
            worksheet = writer.sheets[sheetName]
                    
            for colIndex, column in enumerate(currFrame.columns):
                maxLength = max((len(f"{x:.15g}") for x in currFrame[column]), default=0)
                maxLength = max(maxLength, len(str(column)))
                newWidth = min(maxLength, 20) + 2
                worksheet.set_column(colIndex, colIndex, newWidth)
                
            if algoName != 'targetSum':
                self.algorithmData[algoName].CurrentMax = max(self.algorithmData[algoName].CurrentMax, np.max(rawData[algoName]))
                x, y = np.meshgrid([i for i in range(5, 101, 5)], self.yValues)
                dz = self.algorithmData[algoName].DataFrame.to_numpy(dtype=float).ravel()

                fig = plt.figure()
                ax = fig.add_subplot(111, projection = '3d')
                ax.bar3d(x.ravel(), y.ravel(), np.zeros_like(x.ravel()), 5.0, 5.0, dz, color = self.algorithmData[algoName].BarColor, edgecolor = self.algorithmData[algoName].EdgeColor)

                ax.set_xlabel('Set Integer Count')
                ax.set_ylabel('Absolute Sum Target Index')
                ax.set_zlabel('Average Iteration Count')
                ax.set_title(f'{self.algorithmData[algoName].OfficialName} Graph')

                # Since my friend who's helping with graphing wants to use the pyplot.show() function while I'm fine with just seeing the images and don't have the necessary app installed anyways,
                # this will only cause it to run on his windows device and only on the last data append.
                if sys.platform == 'win32' and results.IntCount == 100: plt.show()
                plt.savefig(self.graphsDir / f'{self.algorithmData[algoName].OfficialName} Graph.png')  
                plt.close()  
        
        writer.close()