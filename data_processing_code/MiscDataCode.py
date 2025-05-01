"""
Stores types used across multiple files to organize data transfer, as well as manages recording disagreements without causing race conditions.

Made by bananathrowingmachine on Apr 30th, 2025
"""
from collections import namedtuple
from numpy import dtype, int64, float64
from pathlib import Path

RawResultsDType = dtype([
    ('targetSum', int64),
    ('memoCrazy', float64), 
    ('memoNormal', float64), 
    ('tabNormal', float64), 
    ('recurseNormal', float64) 
])

ResultsWrapper = namedtuple('ResultsWrapper', ['IntCount', 'RawData', 'RecurseEstimate'])

DisagreeData = namedtuple('DisagreementData', ['AlgoOutputs', 'IntCount', 'TargetIndex', 'TargetSum', 'CurrentSet'])

class DisagreeProcessor:
    def __init__(self, genFilesDir: Path):
        """
        Simple disagreement data processor object. Processes the data and stores it in a subdirectory of the one given to it during construction.

        :param genFilesDir: The directory for all generated files.
        """
        self.disagreDir = genFilesDir / "solution conflicts"
        self.disagreDir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def processBulkDisagreements(cls, genFilesDir: Path, dataInput: list[DisagreeData]):
        """
        Processes a group of disagreements, and their associated data. 

        :param genFilesDir: The directory for all generated files.
        :param dataList: The list of each disagreement are the conditions were it arised in DisagreeData named tuple format.
        """
        processor = cls(genFilesDir)
        for disagreement in dataInput:
            processor.processDisagreement(disagreement)

    def processDisagreement(self, data: DisagreeData):
        """
        Records any disagreement between the algorithms. Since the tested sets can get pretty big, all data besides the set is recorded on one txt file, and then it will point to the specific set that caused the disagreement.
        Records will list which algorithms disagreed, the current set integer count, the current target index and it's associated sum, the actual and absolute sum of the set, then where the actual set was recorded.

        :param data: All of the disagreement data, neatly packaged for use.
        """
        xnor = data.AlgoOutputs
        algoNames = ["Memoized Crazy", "Memoized Normal", "Tabulated Normal", "Recursive Normal"]
        culprits = []
        if xnor[3] != None: # It's hard to really know who's right, so in the case recursive normal is running, it's always right, and otherwise, it's the majority opinion.
            truth = xnor[3] 
        else:
            if xnor[0] == xnor[1]: truth = xnor[2]
            if xnor[1] == xnor[2]: truth = xnor[0]
            else: truth = xnor[1]
        for i in range(len(xnor)):
            if xnor[i] != truth:
                culprits.append(algoNames[i])
        with open(self.disagreDir / "disagree.txt", "a") as f:
            f.write("Test disagree file!")
        # TODO: Write to 2 documents. First document will read the last recorded conflict number in /generated files/solution conflicts/all conflicts.txt then generate a new conflict message with conflict number + 1.
        # TODO: With the conflict number of this conflict recorded, it will generate a file called /generated files/solution conflicts/problem sets/conflict # set.txt and paste the set.
