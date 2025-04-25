"""
Will run a complexity experiment on the provided variations of algorithms that solve partition. Takes a problem size n, and a repeat amount r.
Will run the experiment of (n,S) r times, where there are 21 levels of S, labeled 0-20 (to match their list index), tested and appended to the output list in that order.
All sets inputted into the algorithms will be verified to have an even absolute sum. 
"""
from versions.memoizedCrazy import memoizedCrazy
from versions.memoizedNormal import memoizedNormal
from versions.tabulatedNormal import tabulatedNormal
from versions.recursiveNormal import recursiveNormal

from collections import namedtuple

class complexityExperiment:
    """
    Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each bigS should be.
    """
    def __init__(self, size: int):
        self.runRecurse = size <= 25
        self.sumSize = [int for _ in range(21)]
        self.findAbsSumBounds()

    @classmethod
    def testProblemSize(cls, size: int, repeat = 20) -> list[tuple[float, float, float, float]]:
        """
        Runs a new experiment of set size n. Will repeat the test the given amount of times, get the average, append it to the output, then increment bigS until bigS reaches 20.
        Do note that once n is larger than 25, recursion testing will stop and the final float will always be None.
        """
        experiment = cls(size)
        return experiment.runAllSizes()
    
    def findAbsSumBounds(self):
        """
        Finds the smallest and biggest set of integers, names their sizes sumSize[0] and sumSize[20] respectively, then finds the other 19 values as 5%% increments from sumSize[0] to sumSize[20].
        """
        pass

    def generateRandomSet(self, size: int, bigS: int) -> set[int]:
        pass

    def runSingleTest(self, currentConds: tuple[int, int, set[int]]) -> tuple[int, int, int, int]:
        """
        Runs each algorithm once. Verifies all algorithms returned the same bool, and will record the parameters and which algorithm disagrees if not. Also returns the iteration count of each.
        """
        testSet = currentConds[2]
        memoCrazy = memoizedCrazy.testIterations(testSet)
        memoNormal = memoizedNormal.testIterations(testSet)
        tabNormal = tabulatedNormal.testIterations(testSet)
        xnor = [memoCrazy[1], memoNormal[1], tabNormal[1]]
        if self.runRecurse:
            recurseNormal = recursiveNormal.testIterations(testSet)
            xnor.append(recurseNormal[1])

        if len(set(xnor)) > 1:
            self.recordDisagreement(xnor, currentConds)

        return (
            memoCrazy[0],
            memoNormal[0],
            tabNormal[0],
            recurseNormal[0] if self.runRecurse else None
        )   

    def runSingleSize(self) -> tuple[float, float, float, float]:
        pass

    def runAllSizes(self) -> list[tuple[float, float, float, float]]:
        outputList = [[tuple[float, float, float, float]] for _ in range(21)]

    def recordDisagreement(xnor: list[bool], currentConds: tuple[int, int, set[int]]):
        algoNames = ["Memoized Crazy", "Memoized Normal", "Tabulated Normal", "Recursive Normal"]
        culprits = []
        if len(xnor) == 4: # It's hard to really know who's right, so in the case recursive normal is running, it's always right, and otherwise, it's the majority opinion.
            truth = xnor[3] 
        else:
            if xnor[0] == xnor[1]: truth = xnor[2]
            if xnor[1] == xnor[2]: truth = xnor[0]
            else: truth = xnor[1]
        for i in range(len(xnor)):
            if xnor[i] != truth:
                culprits.append(algoNames[i])
        # TODO: Have this write to 2 sheets. One that has the culprits and the first 2 current conds and then then one that has all 3.
        

