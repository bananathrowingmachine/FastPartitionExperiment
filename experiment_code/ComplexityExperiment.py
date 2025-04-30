"""
Runs an experiment of integer count size for all versions of the algorithm.

Written by bananathrowingmachine, Apr 29th, 2025.
"""
from experiment_code.versions.MemoizedCrazy import MemoizedCrazy
from experiment_code.versions.MemoizedNormal import MemoizedNormal
from experiment_code.versions.TabulatedNormal import TabulatedNormal
from experiment_code.versions.RecursiveNormal import RecursiveNormal
from data_processing_code.MiscDataCode import RawResultsDType, DisagreeData

from multiprocessing import Pool, Lock
from functools import partial
from typing import Tuple, Optional
import numpy as np

class ComplexityExperiment:
    """
    Class for running a complexity experiment. Not desinged for each class to be called seperately however some are more detachable than others but I give you 0 promises on any functionality outside of running it the expected way.
    To run it the expected way, call class method testProblemSize, and give it an integer that says how many integers should be in a randomized set given to each algorithm.
    """
    def __init__(self, size: int):
        """
        Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each targetIndex should be.
        Designed to be run by calling the class method testProblemSize.

        :param size: The amount of integers that should be in each set.
        """
        self.runRecurse = size <= 25
        self.setCount = size
        self.sumSizeTarget = [int for _ in range(21)]
        self.sumSizeBound = self.findAbsSumBounds() # The maximum allowed difference between the predetermined absolute sum (self.sumSize[i]) and the actual absolute sum.
        self.intSizeBound = round(self.sumSizeBound/self.setCount)
        self.disagreeList = [DisagreeData]
        self.disagreeLock = Lock()

    @classmethod
    def testProblemSize(cls, size: int, runExample = False, rounds = 20) -> Tuple[np.ndarray, list[DisagreeData]]:
        """
        In a simple TLDR sense, will run a experiment (or example of one)

        :param size: The amount of seperate integers should be in a set sent to the algorithms. Commonly referred to as size. Stays constant throughtout a single class of the method.
        :param example: Return an example set of data without blowing up your pc. Defaults to false.
        :param rounds: The amount of times a test should be repeated. Defaults to 20 times.
        :return: A numpy array where each column is [targetSum], [memoCrazy], [memoNormal], [tabNormal], and [recurseNormal] in that order, and named, as well as the list of all recorded disagreements between algorithms.
        """
        experiment = cls(size)
        allRegResults = np.empty(21, dtype=RawResultsDType)
        for targetIndex in range(21):
            recurse = size <= 25
            currSize = experiment.getSumSizeTarget(targetIndex)
            if runExample: # Gives a quick set of example data to verify graphing functions are working. The actual "data" comes from a random gaussian distribution.
                random = np.random.default_rng()
                exampleBound = experiment.getSumSizeTarget(20) - experiment.getSumSizeTarget(0)
                r = (random.normal(currSize, exampleBound / 2), random.normal(currSize, exampleBound / 4), random.normal(currSize, exampleBound / 8), random.normal(currSize, exampleBound / 16) if recurse else np.nan)
                allRegResults[targetIndex] = (currSize, r[0], r[1], r[2], r[3]) 
                if random.uniform(0, 52) == 0: # Generates examples of recorded disagreements. Should happen approx 8 times per example data generated. Complete nonsense like the rest of the example data.
                    truth = random.uniform(0, 2) == 0
                    xnor = [truth for _ in range(0, 3 if recurse else 2)]
                    victim = random.uniform(0, 4 if recurse else 3)
                    xnor[victim] != xnor[victim]
                    experiment.recordDisagreement(xnor, targetIndex, experiment.generateRandomSet(targetIndex))
            else:
                r = experiment.runSingleSize(targetIndex, rounds)
                allRegResults[targetIndex] = (currSize, r[0], r[1], r[2], r[3])
        return (allRegResults, experiment.getDisagreeData())
    
    def getSumSizeTarget(self, targetIndex: int) -> int:
        """
        Gets the sum size target for external (my class method's example data) use.

        :param targetIndex: The target index to get the example sum from.
        :return: The sum size target, used for recording the specifics somewhere.
        """
        return self.sumSizeTarget[targetIndex]
    
    def getDisagreeData(self) -> list[DisagreeData]:
        """
        Returns the list of recorded disagreements and their data.

        :return: A list of DisagreeData tuple.
        """
        return self.disagreeList

    def findAbsSumBounds(self) -> int:
        """
        Finds the smallest and largest possible set for the size given at object construction, in terms of sum of the absolute values inside of the set. Called by the constructor (so therefore you shouldn't call it).
        Then fills in the rest of the sumSize as 5% increments from the smallest to the largest, and it's index in the array is known throught the class as "targetIndex".

        :return: 1% of the distance between sumSizeTarget[0] and sumSizeTarget[20]. Used for the set builder error, so that absolute sums don't leave a 1% range from the target absolute sum.
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

        :param targetIndex: The size target index of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
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

        :param targetIndex: The size target index of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
        :return: A tuple with each variations results in order <memoized crazy, memoized normal, tabulated normal, recursive normal>. Will return None for recursive normal if the amount of ints in the set it too high (> 25).
        """
        testSet = self.generateRandomSet(self.sumSizeTarget[targetIndex])

        # If problem size is small enough for basic recursion, run it, if not, make it's results var a tuple of None, None
        with Pool(processes=4 if self.runRecurse else 3) as pool:
            memoCrazy = pool.apply_async(MemoizedCrazy.testIterations, (testSet,)).get()
            memoNormal = pool.apply_async(MemoizedNormal.testIterations, (testSet,)).get()
            tabNormal = pool.apply_async(TabulatedNormal.testIterations, (testSet,)).get()
            recurseNormal = pool.apply_async(RecursiveNormal.testIterations, (testSet,)).get() if self.runRecurse else (None, None)

        xnor = [memoCrazy[1], memoNormal[1], tabNormal[1]]
        if self.runRecurse: xnor.append(recurseNormal[1])
        if len(set(xnor)) > 1: # Record all disagreements between algorithms.
            self.recordDisagreement(xnor, targetIndex, testSet)
        return (memoCrazy[0], memoNormal[0], tabNormal[0], recurseNormal[0])   

    def runSingleSize(self, targetIndex: int, rounds = 20) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        """
        Runs multiple tests of the same condition (set size and abs sum size). Will return a tuple of the average iterations count from each test.
        Uses a python multithreading pool to run 3 (or 4 if not using regular recursion) tests at once as my computer allows this program 12 threads.

        :param targetIndex: The index for the sum size target. Ranges from 0->20 inclusive.
        :param rounds: The amount of times a given size and target sum should be repeated. Defaults to 20 times.
        :return: A tuple with each variations average results in order <memoized crazy, memoized normal, tabulated normal, recursive normal>. Will return np.nan for recursive normal if integer count is above 25.
        """
        results = np.empty((rounds, 4), dtype=np.int64)
        with Pool(processes=3 if self.runRecurse else 4) as pool:
            worker = partial(self.runSingleTest, targetIndex)
            for i, result in enumerate(pool.imap_unordered(worker, range(rounds))):
                results[i] = result
        avg4 = np.mean(results[:, 3]) if self.runRecurse else np.nan
        return (np.mean(results[:, 0]), np.mean(results[:, 1]), np.mean(results[:, 2]), avg4)

    def recordDisagreement(self, xnor: list[bool], targetIndex: int, testedSet: set[int]):
        """
        Packages up all the necessary data for when a disagreement occured, and appends it to the objects disagreements list to be returns with the main data.

        :param xnor: The list essentially used as a xnor gate to determine if all the algorithms returned the same boolean.
        :param targetIndex: The target index being tested.
        :param testedSet: The set that caused the disagreement.
        """
        data = DisagreeData(xnor, self.setCount, targetIndex, self.sumSizeTarget[targetIndex], testedSet)
        self.disagreeLock.acquire()
        self.disagreeList.append(data)
        self.disagreeLock.release()
            

