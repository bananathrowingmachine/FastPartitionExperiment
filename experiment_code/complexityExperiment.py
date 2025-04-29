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
from functools import partial
from typing import Tuple, Optional
import numpy as np

resultDType = np.dtype([
    ('memoCrazy', np.float64),
    ('memoNormal', np.float64),
    ('tabNormal', np.float64),
    ('recurseNormal', np.float64) 
])

class complexityExperiment:
    """
    Class for running a complexity experiment with an inputted size and optional repeat count. Designed to be run by the classMethod testProblemSize(size, repeat)
    """
    def __init__(self, size: int):
        """
        Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each bigS should be.
        Designed to be run by calling the class method testProblemSize.
        """
        self.runRecurse = size <= 25
        self.setCount = size
        self.sumSizeTarget = [int for _ in range(21)]
        self.sumSizeBound = self.findAbsSumBounds() # The maximum allowed difference between the predetermined absolute sum (self.sumSize[i]) and the actual absolute sum.
        self.intSizeBound = round(self.sumSizeBound/self.setCount)

    @classmethod
    def testProblemSize(cls, size: int, repeat = 20) -> np.ndarray:
        """
        Runs a new experiment of set size n. Will repeat the test the given amount of times, get the average, append it to the output, then increment bigS until bigS reaches 20.
        Do note that once n is larger than 25, recursion testing will stop and the final float will always be None.

        :param size: The size of sets to be tested.
        :param repeat: The amount of times a single size and bigS should be repeated. Defaults to 20 times.
        :return: A list of the target sum and each algorithm's iteration count for that target sum. Goes from 0% max sum (output[0]) to 100% max sum (ouput[20]), with 5% increments in between.
        """
        experiment = cls(size)
        return experiment.runAllSizes(repeat)
    
    def findAbsSumBounds(self) -> int:
        """
        Finds the smallest and largest possible set for the size given at object construction, in terms of sum of the absolute values inside of the set. Called by the constructor.
        Then fills in the rest of the sumSize as 5% increments from the smallest to the largest.

        :return: 1% of the distance between sumSizeTarget[0] and sumSizeTarget[20]. Used for the set builder error.
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

    def generateRandomSet(self, targetIndex: int, recurseLevel = 0) -> set[int]:
        """
        Generates a set of random ints of size n and absolute sum +-1% of sumSize[targetIndex]. The absolute sum will also not be above sumSize[21] or below sumSize[0], and will always be even.
        Uses numpy gaussian distribution to generate the sets.

        :param targetIndex: The size target interger of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
        :param recurseLevel: Used internally to prevent infinite recursion. Defaults to 0, unless you are ABSOLUTELY SURE (you aren't) you want to set it to something else, keep it at the default.
        :return: A randomized set with a sum that has an absolute value within 1% of the 5% increment given to it through targetIndex.
        """
        currentAbsSum = 0

        if recurseLevel > 5: # Infinite recursion failsafe. Generates a predetermined set similar to how the lower and upper bounds of set sums were calculated.
            newList = []
            nextNum = round(self.sumSizeTarget[targetIndex]/self.setCount)
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
        mean = round(self.sumSizeTarget[targetIndex]/self.setCount) # Target abs sum / size of set
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
        while currentAbsSum > self.sumSizeBound + self.sumSizeTarget[targetIndex] or currentAbsSum < self.sumSizeTarget[targetIndex] - self.sumSizeBound: # Exceedingly rare (happens 0-2 times in 420 sets built which is one full experiment), but failsafe just in case.
            if loops > 5: # Had extremely long loops happen once every few tests, this attempts to stop that by just recursively making a new set, with a recursion level fail safe for the SUPER EXTREMELY rare.
                return self.generateRandomSet(targetIndex, recurseLevel + 1)
            if currentAbsSum > self.sumSizeBound + self.sumSizeTarget[targetIndex]:
                neededChange = (currentAbsSum - (self.sumSizeBound + self.sumSizeTarget[targetIndex])) * 2
            else:
                neededChange = ((self.sumSizeBound + self.sumSizeTarget[targetIndex]) - currentAbsSum) * 2
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
                return self.generateRandomSet(targetIndex, recurseLevel + 1)
            victim = None
            while victim == None or victim + 1 in newSet:
                victim = int(random.choice(list(newSet)))
            newSet.remove(victim)
            newSet.add(victim + 1)
            loops += 1

        return newSet

    def runSingleTest(self, targetIndex: int) -> Tuple[int, int, int, Optional[int]]:
        """
        Runs each algorithm once. Verifies all algorithms returned the same bool, and will record the parameters and which algorithm disagrees if not. Also returns the iteration count of each.
        Uses a python multithreading pool to run each version at the same time.

        :param current: The current conditions. Will generate the current set internally and add it on.
        :return: A tuple with each variations results in order <memoized crazy, memoized normal, tabulated normal, recursive normal>. Will return None for recursive normal if the amount of ints in the set it too high (> 25).
        """
        testSet = self.generateRandomSet(self.sumSizeTarget[targetIndex])

        # If problem size is small enough for basic recursion, run it, if not, make it's results var a tuple of None, None
        with Pool(processes=4 if self.runRecurse else 3) as pool:
            memoCrazy = pool.apply_async(memoizedCrazy.testIterations, (testSet,)).get()
            memoNormal = pool.apply_async(memoizedNormal.testIterations, (testSet,)).get()
            tabNormal = pool.apply_async(tabulatedNormal.testIterations, (testSet,)).get()
            recurseNormal = pool.apply_async(recursiveNormal.testIterations, (testSet,)).get() if self.runRecurse else (None, None)

        xnor = [memoCrazy[1], memoNormal[1], tabNormal[1]]
        if self.runRecurse: xnor.append(recurseNormal[1])
        if len(set(xnor)) > 1:
            self.recordDisagreement(xnor, targetIndex, testSet)
        return (memoCrazy[0], memoNormal[0], tabNormal[0], recurseNormal[0])   

    def runSingleSize(self, targetIndex: int, rounds: int) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        """
        Runs multiple tests of the same condition (set size and abs sum size). Will return a tuple of the average iterations count from each test.
        Uses a python multithreading pool to run 3 (or 4 if not using regular recursion) tests at once as my computer allows this program 12 threads.

        :param rounds: Will run a single test size this amount of times. Will return an average of the results in the form of a tuple of floats.
        :param targetIndex: The index for the sum size target. Ranges from 0->20 inclusive.
        :return: A tuple with each variations average results in order <memoized crazy, memoized normal, tabulated normal, recursive normal>. Will return np.nan for recursive normal if integer count is above 25.
        """
        results = np.empty((rounds, 4), dtype=np.int64)
        with Pool(processes=3 if self.runRecurse else 4) as pool:
            worker = partial(self.runSingleTest, targetIndex)
            for i, result in enumerate(pool.imap_unordered(worker, range(rounds))):
                results[i] = result
        avg4 = np.mean(results[:, 3]) if self.runRecurse else np.nan
        return (np.mean(results[:, 0]), np.mean(results[:, 1]), np.mean(results[:, 2]), avg4)

    def runAllSizes(self, rounds: int) -> np.ndarray:
        """
        Runs each size index for the current integer count. Returns a 4 * 21 numpy array, having started at size 0 and moved up to size 21.

        :param rounds: How many rounds to give runSingleSize. 
        :return: A 4 * 21 numpy array of results where [0] is memoCrazy, [1] is memoNormal, [2] is tabNormal, and [3] is recurseNormal. [3] will be np.nan above integer count 25.
        """
        allResults = np.empty(21, dtype=resultDType)
        for targetIndex in range(21):
            r = self.runSingleSize(targetIndex, rounds)
            allResults[targetIndex] = (r[0], r[1], r[2], r[3])
        return allResults

    def recordDisagreement(xnor: list[bool], targetIndex: int, testedSet: set[int]):
        """
        h
        """
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
        

