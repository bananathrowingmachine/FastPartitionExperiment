"""
Will run a complexity experiment on the provided variations of algorithms that solve partition. Takes a problem size n, and a repeat amount r.
Will run the experiment of (n,S) r times, where there are 21 levels of S, labeled 0-20 (to match their list index), tested and appended to the output list in that order.
All sets inputted into the algorithms will be verified to have an even absolute sum. 
"""
from versions.memoizedCrazy import memoizedCrazy
from versions.memoizedNormal import memoizedNormal
from versions.tabulatedNormal import tabulatedNormal
from versions.recursiveNormal import recursiveNormal

from multiprocessing import Pool
from typing import NamedTuple
import numpy as np
from typing import Optional

class complexityExperiment:
    """
    Class for running a complexity experiment with an inputted size and optional repeat count. Designed to be run by the classMethod testProblemSize(size, repeat)
    """
    class OutputTuple(NamedTuple):
        """
        Named output tuple for the results.
        """
        sumTarget: int
        memoCrazy: float
        memoNormal: float
        tabNormal: float
        recurseNormal: float

    class CurrentConditions(NamedTuple):
        """
        For storing the current experiment conditions.
        """
        setSize: int
        absSumSize: int
        iterationCount: int
        currentSet: set[int]

    """
    Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each bigS should be.
    Designed to be run by calling the class method testProblemSize.
    """
    def __init__(self, size: int):
        self.runRecurse = size <= 25
        self.setCount = size
        self.sumSizeTarget = [int for _ in range(21)]
        self.sumSizeBound = self.findAbsSumBounds() # The maximum allowed difference between the predetermined absolute sum (self.sumSize[i]) and the actual absolute sum.
        self.intSizeBound = round(self.sumSizeBound/self.setCount)
        # TODO change gaussian approach to find the standard deviation necessary to retain x percent of numbers within the intSizeBounds

    @classmethod
    def testProblemSize(cls, size: int, repeat = 20) -> list[OutputTuple]:
        """
        Runs a new experiment of set size n. Will repeat the test the given amount of times, get the average, append it to the output, then increment bigS until bigS reaches 20.
        Do note that once n is larger than 25, recursion testing will stop and the final float will always be None.
        """
        experiment = cls(size)
        return experiment.runAllSizes(repeat)
    
    @classmethod
    def testSetBuilder(cls, size: int) -> list[set[int]]:
        """
        Used specifically to test my random set builder function. Has no other use.
        """
        test = cls(size)
        for i in range(0, 21):
            print(test.generateRandomSet(i))
    
    def findAbsSumBounds(self) -> int:
        """
        Finds the smallest and largest possible set for the size given at object construction, in terms of sum of the absolute values inside of the set. Called by the constructor.
        Then fills in the rest of the sumSize as 5% increments from the smallest to the largest.
        """
        smallest = 0
        biggest = 32767 # I arbitrarily chose the signed 16 bit int limit, I know python goes larger.
        smallBound = 0
        bigBound = 0
        toggleChange = True # Due to the 0, the time when I increment smallest and decrement biggest are opposite, so this toggles which one happens.
        for _ in range(self.setCount): # Since I'm building the max and min absolute sum of a set, instead of dealing with negatives and absolute values, I just add every positive twice.
            smallBound += smallest
            bigBound += biggest 
            if toggleChange: smallest += 1
            else: biggest -= 1
            toggleChange != toggleChange
        self.sumSizeTarget[0] = smallBound
        self.sumSizeTarget[20] = bigBound
        percent5inc = (bigBound - smallBound)/20
        for i in range(1, 20):
            self.sumSizeTarget[i] = round(percent5inc + self.sumSizeTarget[i-1])
        return round(percent5inc/5)

    def generateRandomSet(self, bigS: int) -> set[int]:
        """
        Generates a set of random ints of size n and absolute sum +-1% of sumSize[bigS]. The absolute sum will also not be above sumSize[21] or below sumSize[0], and will always be even.
        Uses numpy gaussian distribution to generate the sets.
        """
        newSet = set()
        gaussianCenter = round(self.sumSizeTarget[bigS]/self.setCount) # Target abs sum / size of set
        currentAbsSum = 0

        standardDeviation = self.intSizeBound/6 

        random = np.random.default_rng()
        while len(newSet) != self.setCount:
            nextNum = None
            while nextNum == None or (nextNum in newSet and nextNum * -1 in newSet):
                nextNum = abs(round(random.normal(gaussianCenter, standardDeviation)))
                if nextNum > 32767:
                    nextNum = nextNum - (nextNum - 32767)*2 # Wraps numbers that are too big around, similar to absolute value for negatives
            currentAbsSum += nextNum
            if nextNum in newSet or nextNum * -1 in newSet:
                nextNum = nextNum * -1 if nextNum in newSet else nextNum
            elif random.integers(0, 2) == 1: nextNum *= -1
            newSet.add(nextNum)
        
        sumDeviation = abs(currentAbsSum - self.sumSizeTarget[bigS]) # Checks to make sure the set's absolute value is within the error bounds
        if sumDeviation > self.sumSizeBound:
            pass

        if currentAbsSum % 2 == 1: # Make sure it has a absolute sum that is even
            victim = None
            while victim == None or victim + 1 in newSet:
                victim = random.choice(list(newSet))
            newSet.remove(victim)
            newSet.add(victim + 1)

        return newSet

    def runSingleTest(self, current: CurrentConditions) -> tuple[int, int, int, int]:
        """
        Runs each algorithm once. Verifies all algorithms returned the same bool, and will record the parameters and which algorithm disagrees if not. Also returns the iteration count of each.
        Uses a python multithreading pool to run each version at the same time.
        """
        testSet = current[3] 

        # If problem size is small enough for basic recursion, run it, if not, make it's results var a tuple of None, None
        with Pool(processes=4 if self.runRecurse else 3) as pool:
            memoCrazyThread = pool.apply_async(memoizedCrazy.testIterations, (testSet,))
            memoNormalThread = pool.apply_async(memoizedNormal.testIterations, (testSet,))
            tabNormalThread = pool.apply_async(tabulatedNormal.testIterations, (testSet,))
            if self.runRecurse: recurseNormalThread = pool.apply_async(recursiveNormal.testIterations, (testSet,))
        memoCrazy = memoCrazyThread.get()
        memoNormal = memoNormalThread.get()
        tabNormal = tabNormalThread.get()
        recurseNormal = recurseNormalThread.get() if self.runRecurse else (None, None)

        xnor = [memoCrazy[1], memoNormal[1], tabNormal[1], recurseNormal[1]]
        if len(set(xnor)) > 1:
            self.recordDisagreement(xnor, current)

        return (
            memoCrazy[0],
            memoNormal[0],
            tabNormal[0],
            recurseNormal[0]
        )   

    def runSingleSize(self) -> tuple[float, float, float, float]:
        """
        Runs multiple tests of the same condition (set size and abs sum size). Will return a tuple of the average iterations count from each test.
        Uses a python multithreading pool to run 3 (or 4 if not using regular recursion) tests at once as my computer allows this program 12 threads.
        """
        pass

    def runAllSizes(self) -> list[OutputTuple]:
        outputList = [[self.OutputTuple] for _ in range(21)]
        return outputList

    def recordDisagreement(xnor: list[bool], current: CurrentConditions):
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
        # TODO: Have this write to 2 docs. One that has the culprits and the first 3 current conds (set size, abs sum size, iteration count), and one that points to the actual set inputted in another document.
        

