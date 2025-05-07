"""
Stores types used across multiple files to organize data transfer, as well as manages recording disagreements without causing race conditions.

Made by bananathrowingmachine on May 2nd, 2025
"""
from collections import namedtuple
from dataclasses import dataclass, field
import numpy as np
from pathlib import Path
from docx import Document

# Float64 max values = finfo(resolution=1e-15, min=-1.7976931348623157e+308, max=1.7976931348623157e+308, dtype=float64)
RawResultsDType = np.dtype([
    ('targetSum', np.uint64),
    ('memoCrazy', np.float64), 
    ('memoNormal', np.float64), 
    ('tabNormal', np.float64), 
    ('recurseNormal', np.float64) 
])

ResultsWrapper = namedtuple('ResultsWrapper', ['IntCount', 'RawData', 'RecurseEstimate'])

@dataclass(frozen=True)
class ResultsWrapper:
    IntCount: int
    RecurseEstimate: int
    RawData: np.ndarray = field(default_factory=lambda: np.empty(21, dtype=RawResultsDType))

@dataclass(frozen=True)
class DisagreeData:
    AlgoOutputs: list[bool]
    IntCount: int
    TargetIndex: int
    TestNum: int
    TargetSum: int
    CurrentList: list[int]

class DisagreeProcessor:
    def __init__(self, genFilesDir: Path):
        """
        Simple disagreement data processor object. Processes the data and stores it in a subdirectory of the one given to it during construction.

        :param genFilesDir: The directory for all generated files.
        """
        self.disagreeDir = genFilesDir / "solution conflicts"
        self.disagreeDir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def processBulkDisagreements(cls, genFilesDir: Path, dataInput: list[DisagreeData], idNum: int):
        """
        Processes a group of disagreements, and their associated data. 

        :param genFilesDir: The directory for all generated files.
        :param dataList: The list of each disagreement are the conditions were it arised in DisagreeData named tuple format.
        :param idNum: The disagreement number. Starts at the number given and will increment by one for each given disagreement.
        """
        processor = cls(genFilesDir)
        for disagreement in dataInput:
            processor.processDisagreement(disagreement, idNum)
            idNum += 1

    @classmethod
    def noDisagreements(cls, genFilesDir: Path):
        """
        Handles cases where there were no recorded disagreements.

        :param genFilesDir: The directory for the generated file.
        """
        directory = cls(genFilesDir)
        mainDoc = Document()
        mainDoc.add_heading("Complete Algorithms Disgareement Record")
        mainDoc.add_paragraph("There were no recorded disagreements throughout running the entire experiment. Therefore, there is nothing else here to see.")
        mainDoc.save(directory / "DisagreementRecord.docx")

    def processDisagreement(self, data: DisagreeData, idNum: int):
        """
        Records any disagreement between the algorithms. Since the tested sets can get pretty big, all data besides the set is recorded on one txt file, and then it will point to the specific set that caused the disagreement.
        Records will list which algorithms disagreed, the current set integer count, the current target index and it's associated sum, the current test number, and the actual set was tested.

        :param data: All of the disagreement data, neatly packaged for use.
        :param idNum: The disagreement number.
        """
        xnor = data.AlgoOutputs
        algoNames = ["Memoized Crazy", "Memoized Normal", "Tabulated Normal"]
        culprits = []
        if len(xnor) > 3: # It's hard to really know who's right, so in the case recursive normal is running, it's always right, and otherwise, it's the majority opinion.
            truth = xnor[3] 
        else:
            if xnor[0] == xnor[1]: truth = xnor[0]
            if xnor[1] == xnor[2]: truth = xnor[1]
            else: truth = xnor[2]
        for i in range(len(xnor)):
            if xnor[i] != truth:
                culprits.append(algoNames[i])
        try:
            document = Document(self.disagreeDir / "DisagreementRecord.docx")
        except FileNotFoundError:
            document = Document()
            document.add_heading("Complete Algorithms Disgareement Record")
            document.add_heading("This document has all recorded instances where the different partition algorithms disagreed on the answer for a given set. It is procedurally generated as the experiment runs.", 3)

        header = document.add_paragraph(f"    ")
        header.add_run(f"Disagreement number {idNum}:").bold = True
        
        paragraph = document.add_paragraph()
        if len(culprits) == 1:
            paragraph.add_run(f"The algorithm {culprits[0]} claimed that the answer was {not truth} when every other algorithm running claimed that it was {truth}.")
        elif len(culprits) == 2:
            paragraph.add_run(f"The algorithms {culprits[0]} and {culprits[1]} claimed that the answer was {not truth} while Recursive Normal which is assumed to always be correct claimed that it was {truth}.")
        else:
            paragraph.add_run(f"Every other algorithm claimed that the answer was {not truth} while Recursive Normal which is assumed to always be correct claimed that it was {truth}.")
        paragraph.add_run().add_break()
        paragraph.add_run(f"The specific enviornment being tested when this disagreement occured is shown below:").add_break()

        if data.TestNum > 3: numSuffix = "th"
        elif data.TestNum == 3: numSuffix = "rd"
        elif data.TestNum == 2: numSuffix = "nd"
        else: numSuffix = "st"
        paragraph.add_run(f"This was the {data.TestNum}{numSuffix} repeat test for this specific set of independent variables.").add_break()
        paragraph.add_run(f"The amount of integers per set was {data.IntCount}.").add_break()
        paragraph.add_run(f"The current target index was {data.TargetIndex} which corresponds to a target sum of {data.TargetSum}.").add_break()
        paragraph.add_run(f"The specific set that was tested has a sum of {sum(data.CurrentList)}. It is shown below:").add_break()
        paragraph.add_run(f"{data.CurrentList}")
    
        document.save(self.disagreeDir / "DisagreementRecord.docx")
        
