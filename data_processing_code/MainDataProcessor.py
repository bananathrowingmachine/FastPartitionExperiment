"""
Processes all of the data into data tables and graphs. 

Made by bananathrowingmachine and Earthquakeshaker2 on Nov 27rd, 2025.
"""
from data_processing_code.MiscDataCode import ResultsWrapper, DataProcessingInfo
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys

class MainDataProcessor:
    """
    Data processor class, that stores, saves, and handles all the data tables and graphs. Best if created once and appendData is called repeatedly.
    """
    def __init__(self, genFilesDir: Path, runSpeedy: bool):
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

        self.algorithmData['targetSum'] = DataProcessingInfo('Absolute Target Sum', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.int64), None, None)
        self.algorithmData['newMemoCrazy'] = DataProcessingInfo('New Memoized Crazy', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (0.00, 0.40, 0.20), (0.00, 0.10, 0.05))
        if runSpeedy:
            self.algorithmData['oldMemoCrazy'] = DataProcessingInfo('Old Memoized Crazy', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (0.20, 1.00, 0.20), (0.05, 0.25, 0.05))
        else:
            self.algorithmData['memoNormal'] = DataProcessingInfo('Memoized Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (0.00, 0.12, 0.70), (0.00, 0.02, 0.10))
            self.algorithmData['tabCrazy'] = DataProcessingInfo('Tabulated Crazy', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (1.00, 1.00, 0.00), (0.10, 0.10, 0.00))
            self.algorithmData['tabNormal'] = DataProcessingInfo('Tabulated Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (0.70, 0.00, 0.00), (0.10, 0.00, 0.00))
            self.algorithmData['recurseNormal'] = DataProcessingInfo('Recursive Normal', pd.DataFrame(columns=self.yValues, index=self.xValues, dtype=np.float64), (0.60, 0.00, 0.50), (0.10, 0.00, 0.08))

    def appendData(self, results: ResultsWrapper) -> None:
        """
        Appends a new chunk of data to the appropriate x rows for each algorithm in it's data frame.

        :param data: The data to get processed, wrapped up with the x index and estimated exponential time value.
        """
        xIndex = results.IntCount
        rawData = results.RawData   
        
        for algoName in self.algorithmData.keys():
            if algoName == 'recurseNormal' and results.RecurseEstimate is not None:
                yData = np.array([results.RecurseEstimate for _ in range(21)])
            else:
                yData = np.array([row[algoName] for row in rawData])
            self.algorithmData[algoName].DataFrame.loc[xIndex] = yData

    def outputTableData(self) -> None:
        """
        Generates the data tables for the generated data. Formally returns nothing, but will save a file to the directory given during object construction.
        """
        writer = pd.ExcelWriter(self.tablesDir / "Results.xlsx", engine="xlsxwriter") 

        for algoName in self.algorithmData.keys():
            currFrame = self.algorithmData[algoName].DataFrame
            currRealName = self.algorithmData[algoName].OfficialName

            sheetName = currRealName
            currFrame.T.to_excel(writer, sheet_name=sheetName)
            worksheet = writer.sheets[sheetName]
                    
            for colIndex, column in enumerate(currFrame.columns):
                maxLength = max((len(f"{x:.15g}") for x in currFrame[column]), default=0)
                maxLength = max(maxLength, len(str(column)))
                newWidth = min(maxLength, 20) + 2
                worksheet.set_column(colIndex, colIndex, newWidth)

        writer.close()

    def outputImageData(self) -> None:
        """
        Generates all of the images and files for the generated data. Formally returns nothing, but will save multiple files to the directory given during object construction.
        """
        for algoName in self.algorithmData.keys():
            currFrame = self.algorithmData[algoName].DataFrame
            currRealName = self.algorithmData[algoName].OfficialName

            self.outputTableData()
                
            if algoName != 'targetSum':

                # To show off the numbers increasing better, this code swaps the x and y axis, and then reverses the new x axis.
                x, y = np.meshgrid(self.xValues, self.yValues)
                dz = currFrame.T.to_numpy(dtype=float).ravel()
                fig = plt.figure()
                ax = fig.add_subplot(111, projection = '3d')

                if algoName == 'recurseNormal': # Does all the special handling needed for the exponential time Recursive Normal algorithm.
                    mask = x.ravel() > 25  

                    xPre = x.ravel()[~mask]
                    yPre = y.ravel()[~mask]
                    dzPre = dz[~mask]
                    xPost = x.ravel()[mask]
                    yPost = y.ravel()[mask]
                    dzPost = dz[mask]

                    dzPreLog = np.log2(dzPre)
                    dzPostLog = np.log2(dzPost)

                    ax.bar3d(yPre, xPre, 1e-10 * np.ones_like(xPre), 0.95, 4.95, dzPreLog, color=self.algorithmData[algoName].BarColor, edgecolor=self.algorithmData[algoName].EdgeColor)  
                    ax.bar3d(yPost, xPost, 1e-10 * np.ones_like(xPost), 0.95, 4.95, dzPostLog, color=self.algorithmData[algoName].BarColor, edgecolor=(0.40, 0.33, 0.00)) 
                  
                    scale = 10
                    major_vals = [10, 100]
                    major_locs = np.log2(major_vals) * scale
                    major_labels = [r"$10^1$", r"$10^2$"]

                    ax.set_zticks(major_locs)
                    ax.set_zticklabels(major_labels)

                else:
                    ax.bar3d(y.ravel(), x.ravel(), np.ones_like(x.ravel()), 0.95, 4.95, dz, color = self.algorithmData[algoName].BarColor, edgecolor = self.algorithmData[algoName].EdgeColor)  
                    ax.zaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
                    ax.zaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.2e}"))
                    ax.set_zlabel('Average Iteration Count', labelpad=28)
                    ax.tick_params(axis='z', which='major', pad=14) 

                ax.set_xlabel('Absolute Sum Target Index')  
                ax.invert_xaxis()  
                ax.set_ylabel('Set Integer Count')       
                ax.set_title(f'{currRealName} Graph')

                # Shows the interactive plot window for my friend helping me, who is on windows.
                if sys.platform == 'win32': plt.show()
                plt.savefig(self.graphsDir / f'{currRealName} Graph.png')  
                plt.close()