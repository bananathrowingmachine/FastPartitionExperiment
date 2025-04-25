"""
Will run a complexity experiment on the provided variations of algorithms that solve partition. Takes a problem size n, and a repeat amount r.
Will run the experiment of (n,S) r times, where there are 21 levels of S, labeled 0-20 (to match their list index), tested and appended to the output list in that order.
All sets inputted into the algorithms will be verified to have an even absolute sum. 
"""
from versions.memoizedCrazy import memoizedCrazy
from versions.memoizedNormal import memoizedNormal
from versions.recursiveNormal import recursiveNormal
from versions.tabulatedNormal import tabulatedNormal

from collections import namedtuple

class complexityExperiment:
    """
    Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each bigS should be.
    """
    def __init__(self, size: int):
        self.runRecurse = size <= 25
        self.sumIndex = 0
        self.sumSize = [int for _ in range(21)]
        self.findAbsSumBounds()

    @classmethod
    def testProblemSize(cls, size: int, repeat = 20) -> list[tuple[float, float, float, float]]:
        """
        Runs a new experiment of set size n. Will repeat the test the given amount of times, get the average, append it to the output, then increment bigS until bigS reaches 20.
        """
        experiment = cls(size)
        outputList = [[tuple[float, float, float, float]] for _ in range(21)]
        resultsTuple = namedtuple('Results Tuple', ['memoCrazy', 'memoNormal', 'tabNormal', 'recurseNormal'])
        return outputList
    
    def findAbsSumBounds():
        """
        Finds the smallest and biggest set of integers, names their sizes sumSize[0] and sumSize[20] respectively, then finds the other 19 values incrementally.
        The goal is that sumSize[0] is the set of ints of size n with the smallest absolute sum possible, and sumSize[20] is the biggest.
        The other 19 values should represent 5% increments from sumSize[0] to sumSize[20], so sumSize[5] should have a sum close to 25% of sumSize[20] if sumSize[0] was actually 0.
        """
        pass