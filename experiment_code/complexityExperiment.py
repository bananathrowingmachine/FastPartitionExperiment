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
        absSumTarget: int
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

    @classmethod
    def testProblemSize(cls, size: int, repeat = 20) -> list[OutputTuple]:
        """
        Runs a new experiment of set size n. Will repeat the test the given amount of times, get the average, append it to the output, then increment bigS until bigS reaches 20.
        Do note that once n is larger than 25, recursion testing will stop and the final float will always be None.
        """
        experiment = cls(size)
        return experiment.runAllSizes(repeat)
    
    @classmethod
    def testSetBuilder(cls, size: int) -> float | int:
        """
        Used specifically to test my random set builder function. Has no other use.
        """
        test = cls(size)
        avgSumDev = 0
        totalFails = 0
        for i in range(0, 21):
            sumDev = test.generateRandomSet(i)
            print("Sum deviation of {:.5f}% from expected sum.".format(sumDev))
            if sumDev > 1:
                print("Which is too high!")
                totalFails += 1
            avgSumDev += sumDev
        return sumDev, totalFails
    
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

    def generateRandomSet(self, bigS: int, recurseLevel = 0) -> float:
        """
        Generates a set of random ints of size n and absolute sum +-1% of sumSize[bigS]. The absolute sum will also not be above sumSize[21] or below sumSize[0], and will always be even.
        Uses numpy gaussian distribution to generate the sets.

        :param bigS: The size target interger of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
        :param recurseLevel: Used internally to prevent infinite recursion. Defaults to 0, unless you are ABSOLUTELY SURE (you aren't) you want to set it to something else, keep it at the default.
        """
        currentAbsSum = 0

        if recurseLevel > 5: # Infinite recursion failsafe. Generates a predetermined set similar to how the lower and upper bounds of set sums were calculated.
            newList = []
            nextNum = round(self.sumSizeTarget[bigS]/self.setCount)
            newList.append(nextNum)
            nextNum *= -1
            newList.append(nextNum)
            currentAbsSum = nextNum * -2
            next4 = [nextNum * -1 + 1, nextNum - 1, nextNum * -1 - 1, nextNum + 1]
            next4copy = list(next4)
            while len(newList) != self.setCount: # Impossible for this to be infinite.
                if len(next4copy) != 0:
                    nextNum = next4copy.pop(0)
                    currentAbsSum += abs(nextNum)
                    newList.append(nextNum)
                else:
                    next4copy = [next4[0] + 1, next4[1] - 1, next4[2] - 1, next4[3] + 1]
                    next4 = list(next4copy)
            if currentAbsSum % 2 == 1:
                if newList[-1] + 1 in newList: # Both options cannot be in the list
                    newList[-1] -= 1
                else:
                    newList[-1] += 1
            return set(newList)

        newSet = set()
        mean = round(self.sumSizeTarget[bigS]/self.setCount) # Target abs sum / size of set
        standardDeviation = (self.intSizeBound * 6) / 12

        random = np.random.default_rng()
        for _ in range(0, self.setCount):
            nextNum = None
            loops = 0
            while nextNum == None or (nextNum in newSet and nextNum * -1 in newSet):
                if loops > 20: # Infinite loop failsafe.
                    nextNum = mean
                    while nextNum in newSet and nextNum * -1 in newSet: # Impossible for this to be infinite.
                        nextNum += 1
                else:
                    nextNum = abs(round(random.normal(mean, standardDeviation)))
                    if nextNum > 32767:
                        nextNum = nextNum - (nextNum - 32767)*2 # Wraps numbers that are too big around, similar to absolute value for negatives
                    loops += 1
            currentAbsSum += nextNum
            if nextNum in newSet or nextNum * -1 in newSet:
                nextNum = nextNum * -1 if nextNum in newSet else nextNum
            elif random.integers(0, 2) == 1: nextNum *= -1
            newSet.add(int(nextNum))
            devDiv = (14 - len(newSet) / self.setCount * 10)
            standardDeviation = (6 * (2 * self.intSizeBound - abs(abs(nextNum) - mean))) / devDiv # Self adjusting standard deviation. Based on how far the last number was from the bounds, and how many numbers are left until set is filled.
            if standardDeviation <= 0: # Rarely happens, will set the deviation to slightly lower than full with the current standard deviation.
                standardDeviation = (self.intSizeBound * 1.5) / devDiv

        loops = 0
        while currentAbsSum > self.sumSizeBound + self.sumSizeTarget[bigS] or currentAbsSum < self.sumSizeTarget[bigS] - self.sumSizeBound: # Exceedingly rare (happens 0-2 times in 420 sets built which is one full experiment), but failsafe just in case.
            if loops > 5: # Had extremely long loops happen once every few tests, this attempts to stop that by just recursively making a new set, with a recursion level fail safe for the SUPER EXTREMELY rare.
                return self.generateRandomSet(bigS, recurseLevel + 1)
            if currentAbsSum > self.sumSizeBound + self.sumSizeTarget[bigS]:
                neededChange = (currentAbsSum - (self.sumSizeBound + self.sumSizeTarget[bigS])) * 2
            else:
                neededChange = ((self.sumSizeBound + self.sumSizeTarget[bigS]) - currentAbsSum) * 2
                neededChange *= -1
            victim = int(random.choice(list(newSet)))
            if victim > 0 and (victim - neededChange) not in newSet: # Positive integers (not including 0).
                newSet.remove(victim)
                newSet.add(victim - neededChange)
                currentAbsSum -= neededChange
            elif victim < 0 and (victim + neededChange) not in newSet: # Negative integers (not including 0).
                newSet.remove(victim)
                newSet.add(victim + neededChange)
                currentAbsSum -= neededChange      
            loops += 1

        loops = 0
        if currentAbsSum % 2 == 1: # Make sure it has a absolute sum that is even
            if loops > 5: # Since I implemented the failsafe above, I put it here too.
                return self.generateRandomSet(bigS, recurseLevel + 1)
            victim = None
            while victim == None or victim + 1 in newSet:
                victim = int(random.choice(list(newSet)))
            newSet.remove(victim)
            newSet.add(victim + 1)
            loops += 1

        return abs((currentAbsSum / (self.sumSizeTarget[20] - self.sumSizeTarget[0]) * 100) - bigS * 5)

    def runSingleTest(self, current: CurrentConditions) -> tuple[int, int, int, int]:
        """
        Runs each algorithm once. Verifies all algorithms returned the same bool, and will record the parameters and which algorithm disagrees if not. Also returns the iteration count of each.
        Uses a python multithreading pool to run each version at the same time.
        """
        testSet = self.generateRandomSet(current.absSumTarget)
        current.currentSet = testSet

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

        return (memoCrazy[0], memoNormal[0], tabNormal[0], recurseNormal[0])   

    def runSingleSize(self, rounds: int) -> tuple[float, float, float, float]:
        """
        Runs multiple tests of the same condition (set size and abs sum size). Will return a tuple of the average iterations count from each test.
        Uses a python multithreading pool to run 3 (or 4 if not using regular recursion) tests at once as my computer allows this program 12 threads.
        """
        pass

    def runAllSizes(self, rounds: int) -> list[OutputTuple]:
        random = np.random.default_rng()
        outputList = [[self.OutputTuple] for _ in range(21)]
        for i in range(0,21):
            nextTuple = self.OutputTuple
            nextTuple.sumTarget = random.integers(0, 100)
            nextTuple.memoCrazy = random.random() * 10
            nextTuple.memoNormal = random.random() * 100
            nextTuple.tabNormal = random.random() * 1000
            nextTuple.recurseNormal = random.random() * 10000
            outputList[i] = nextTuple
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
        # TODO: Write to 2 documents. First document will read the last recorded conflict number in /generated files/solution conflicts/all conflicts.txt then generate a new conflict message with conflict number + 1.
        # TODO: With the conflict number of this conflict recorded, it will generate a file called /generated files/solution conflicts/problem sets/conflict # set.txt and paste the set.
        

