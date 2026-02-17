"""
Runs an experiment of integer count size for all versions of the algorithm.

Written by bananathrowingmachine, Feb 16, 2026.
"""
from data_processing_code.MiscDataCode import FullResultsDType, SpeedyResultsDType, DisagreeData
import concurrent.futures as ThreadPool
from multiprocessing import Manager
import numpy as np
from enum import IntEnum

def worker(taskName: str, testList: list[int], runPython: bool) -> tuple[int, bool]:
    """
    Worker function for the threads so that python can pickle everything.
    
    :param taskName: The name of the task
    :type taskName: str
    :param testList: The list to be tested
    :type testList: list[int]
    :param runPython: Boolean on running the Python versions instead of the C versions
    :type runPython: bool
    :return: The result of the experiment, with the iteration count and then if the list is partitionable
    :rtype: tuple[int, bool]
    """
    if runPython: # luckily python only imports stuff once and then just reuses the pointers
        from experiment_code.versions.python.MemoizedNormal import MemoizedNormal
        from experiment_code.versions.python.OldMemoizedCrazy import OldMemoizedCrazy
        from experiment_code.versions.python.NewMemoizedCrazy import NewMemoizedCrazy
        import experiment_code.versions.python.TabulatedCrazy as TabulatedCrazy
        import experiment_code.versions.python.TabulatedNormal as TabulatedNormal
        from experiment_code.versions.python.RecursiveNormal import RecursiveNormal
    else:
        from experiment_code.versions.c_bin._MemoizedNormal import lib as MemoizedNormal
        from experiment_code.versions.c_bin._OldMemoizedCrazy import lib as OldMemoizedCrazy
        from experiment_code.versions.c_bin._NewMemoizedCrazy import lib as NewMemoizedCrazy
        from experiment_code.versions.c_bin._TabulatedCrazy import lib as TabulatedCrazy
        from experiment_code.versions.c_bin._TabulatedNormal import lib as TabulatedNormal
        from experiment_code.versions.c_bin._RecursiveNormal import lib as RecursiveNormal
        from experiment_code.versions.c_bin._NewMemoizedCrazy import ffi
        testList = ffi.new("int[]", testList)

    registry = {"oldMemoCrazy": OldMemoizedCrazy, "memoNormal": MemoizedNormal, "tabCrazy": TabulatedCrazy, "tabNormal": TabulatedNormal, "recurseNormal": RecursiveNormal, "newMemoCrazy": NewMemoizedCrazy}

    if runPython:
        return registry[taskName].testIterations(testList) 
    result = registry[taskName].testIterations(testList, len(testList)) 
    return (int(result.iterationCount), bool(result.result))

class OutLevel(IntEnum):
    """
    An enum for the console output level of the complexity tester. Each level will output what is describe as well as what is before it.
    """
    NONE = 0
    """
    No console output.
    """
    SUITE = 1
    """
    Will output each time the next int count has started or finished testing (the class method being called or returning).
    """
    SUM = 2
    """
    Will output each time the next sum size has started or finished testing.
    """
    BATCH = 3
    """
    Will output each time the next batch of 4 algorithms has started or finished testing.
    """
    ALL = 4
    """
    Will output each time a single algorithm has finished testing.
    """

class ComplexityExperiment:
    """
    Class for running a complexity experiment. Not desinged for each class to be called seperately however some are more detachable than others but I give you 0 promises on any functionality outside of running it the expected way.
    To run it the expected way, call class method testProblemSize, and give it an integer that says how many integers should be in a randomized set given to each algorithm.
    """
    def __init__(self, size: int, outLevel: OutLevel, inputArgs):
        """
        Experiment setup. Finds the sets of size n with the smallest possible and largest possible (with signed 32 bit int limit being the largest number added) absolute sums. Then finds the size each targetIndex should be.
        Designed to be run by calling the class method testProblemSize.

        :param size: The amount of integers that should be in each set.
        :param outLevel: The amount of console output the app should produce. I don't plan on making this modifiable by user input.
        """
        self.runRecurse = size <= 25
        self.setCount = size
        self.sumSizeTarget = [None for _ in range(21)]
        self.sumSizeBound = self.findAbsSumBounds() # The maximum allowed difference between the predetermined absolute sum (self.sumSize[i]) and the actual absolute sum.
        self.intSizeBound = round(self.sumSizeBound/self.setCount)
        self.disagreeList: list[DisagreeData] = []
        self.disagreeLock = Manager().Lock()
        self.runReduced = inputArgs.reduced
        self.runPython = inputArgs.python
        self.outputLevel = outLevel
        if self.runReduced:
            self.tasks = ["oldMemoCrazy"]
        else:
            self.tasks = ["memoNormal", "tabCrazy", "tabNormal"]
            if self.runRecurse:
                self.tasks.append("recurseNormal")
        self.tasks.append("newMemoCrazy")

    @classmethod
    def testProblemSize(cls, size: int, inputArgs) -> tuple[np.ndarray, list[DisagreeData]]:
        """
        In a simple TLDR sense, will run a experiment (or example of one).

        :param size: The amount of seperate integers should be in a set sent to the algorithms. Commonly referred to as size. Stays constant throughtout a single class of the method.
        :param inputArgs: The command line arguments passed when the program started.
        :return: A numpy array where each column is [targetSum], [newMemoCrazy], [memoNormal], [tabCrazy], [tabNormal], and [recurseNormal] in that order, and named, as well as the list of all recorded disagreements between algorithms.
        """
        if inputArgs.example:
            yapLevel = OutLevel.NONE
        elif inputArgs.reduced:
            if inputArgs.python:
                yapLevel = OutLevel.SUM
            else:
                yapLevel = OutLevel.SUITE
        elif not inputArgs.python:
            yapLevel = OutLevel.BATCH
        else:
            yapLevel = OutLevel.ALL
        experiment = cls(size, yapLevel, inputArgs)
        allRegResults = np.empty(21, dtype=SpeedyResultsDType) if inputArgs.reduced else np.empty(21, dtype=FullResultsDType)
        if experiment.outputLevel >= OutLevel.SUITE: print(f"|[==>>--:>-  Started entire test suite for set integer count {size:3}. This will take awhile.  -<:--<<==]|")
        for targetIndex in range(21):
            r = experiment.generateSampleOutput(targetIndex) if inputArgs.example else experiment.runSingleSize(targetIndex)
            allRegResults[targetIndex] = (experiment.sumSizeTarget[targetIndex], r[0], r[1]) if inputArgs.reduced else (experiment.sumSizeTarget[targetIndex], r[0], r[1], r[2], r[3], r[4])
        
        if experiment.outputLevel >= OutLevel.SUITE: 
            print(f"|[==>>--:>- Finished entire test suite for set integer count {size:3}. Results have been sent. -<:--<<==]|")
            print("|[==>>--:>- ============================================================================= -<:--<<==]|")
        return allRegResults, experiment.disagreeList
    
    def generateSampleOutput(self, targetIndex: int) -> tuple[np.float64, np.float64, np.float64, np.float64, np.float64]:
        """
        Returns a set of quickly generated example data to test the data processing.

        :param targetIndex: The target index to get the example sum from.
        :return: The sum size target, used for recording the specifics somewhere.
        """
        currSize = self.sumSizeTarget[targetIndex]
        random = np.random.default_rng()
        exampleBound = self.sumSizeTarget[20] - self.sumSizeTarget[0]
        output = (abs(random.normal(currSize, exampleBound / 2)), abs(random.normal(currSize, exampleBound / 4)), abs(random.normal(currSize, exampleBound / 6)), 
                  abs(random.normal(currSize, exampleBound / 8)), abs(random.normal(currSize, exampleBound / 10)) if self.runRecurse else np.nan)
        
        if targetIndex in np.random.default_rng().integers(0, 21, size=2):
            xnor = [random.integers(0, 2) == 0, random.integers(0, 2) == 0]
            if not self.runReduced:
                xnor.extend([random.integers(0, 2) == 0, random.integers(0, 2) == 0])
                if self.runRecurse: xnor.append(random.integers(0, 2) == 0)
            self.disagreeList.append(DisagreeData(xnor, self.setCount, targetIndex, 1, self.sumSizeTarget[targetIndex], self.generateRandomSet(targetIndex)))
        return output

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
            toggleChange = not toggleChange
        self.sumSizeTarget[0] = smallBound
        self.sumSizeTarget[20] = bigBound
        percent5inc = (bigBound - smallBound)/20
        for i in range(1, 20):
            self.sumSizeTarget[i] = round(percent5inc + self.sumSizeTarget[i-1])
        return round(percent5inc/5)

    def generateRandomSet(self, targetIndex: int) -> set[int]:
        """
        Generates a set of random ints of size n and absolute sum +-1% of sumSize[targetIndex]. The absolute sum will also not be above sumSize[21] or below sumSize[0], and will always be even.
        Uses numpy gaussian distribution to generate the sets.

        :param targetIndex: The size target index of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
        :return: A randomized set with a sum that has an absolute value within 1% of the 5% increment given to it through targetIndex.
        """
        currentAbsSum = 0

        newSet = set()
        mean = round(self.sumSizeTarget[targetIndex]/self.setCount) # Target abs sum / size of set
        standardDeviation = (self.intSizeBound * 6) / 12

        random = np.random.default_rng()
        for _ in range(0, self.setCount):
            nextNum = abs(round(random.normal(mean, standardDeviation)))
            if nextNum > 32767: nextNum = nextNum - (nextNum - 32767) * 2 # Wraps numbers that are too big around, similar to absolute value for negative
            while nextNum in newSet or -nextNum in newSet:
                nextNum = abs(round(random.normal(mean, standardDeviation)))
                if nextNum > 32767: nextNum = nextNum - (nextNum - 32767) * 2 # Wraps numbers that are too big around, similar to absolute value for negatives
                standardDeviation += 1 
            currentAbsSum += nextNum
            if random.integers(0, 2) == 1: nextNum *= -1
            newSet.add(int(nextNum))
            devDiv = (14 - len(newSet) / self.setCount * 10)
            standardDeviation = (6 * (2 * self.intSizeBound - abs(abs(nextNum) - mean))) / devDiv # Self adjusting standard deviation. Based on how far the last number was from the bounds, and how many numbers are left until set is filled.
            if standardDeviation <= 0: # Rarely happens, will set the deviation to slightly lower than full with the current standard deviation.
                standardDeviation = (self.intSizeBound * 1.5) / devDiv

        if currentAbsSum > self.sumSizeBound + self.sumSizeTarget[targetIndex] or currentAbsSum < self.sumSizeTarget[targetIndex] - self.sumSizeBound: # Exceedingly rare, but failsafe just in case.
            if currentAbsSum > self.sumSizeBound + self.sumSizeTarget[targetIndex]:
                neededChange = (currentAbsSum - (self.sumSizeBound + self.sumSizeTarget[targetIndex])) * 2
            else:
                neededChange = ((self.sumSizeBound + self.sumSizeTarget[targetIndex]) - currentAbsSum) * 2
                neededChange *= -1
            loops = 0
            while currentAbsSum > self.sumSizeBound + self.sumSizeTarget[targetIndex] or currentAbsSum < self.sumSizeTarget[targetIndex] - self.sumSizeBound:
                if loops > 5: # Had extremely long loops happen once every few tests, this attempts to stop that by just recursively making a new set.
                    return self.generateRandomSet(targetIndex)
                victim = newSet.pop()
                if victim > 0 and (victim - neededChange) not in newSet: # Positive integers (not including 0).
                    newSet.add(victim - neededChange)
                    currentAbsSum -= neededChange
                elif victim < 0 and (victim + neededChange) not in newSet: # Negative integers (not including 0).
                    newSet.add(victim + neededChange)
                    currentAbsSum -= neededChange
                else:
                    newSet.add(victim)   
                loops += 1

        if sum(newSet) == 0: # The sum being equal to 0 is trivial and uninteresting, therefore try again if this happens.
            return self.generateRandomSet(targetIndex)

        while currentAbsSum % 2 == 1: # The sum being odd is trivial and uninteresting, therefore make it even if this happens.
            victim = newSet.pop()
            if victim + 1 not in newSet:
                newSet.add(victim + 1)
                currentAbsSum += 1
            else:
                newSet.add(victim)

        return newSet
    
    def runSingleSize(self, targetIndex: int) -> tuple[np.float64, np.float64, np.float64, np.float64, np.float64] | tuple[np.float64, np.float64]:
        """
        Runs multiple tests of the same condition (set size and abs sum size). Will return a tuple of the average iterations count from each test.
        Uses a python multithreading pool to run 3 (or 4 if not using regular recursion) tests at once as my computer allows this program 12 threads.

        :param targetIndex: The index for the sum size target. Ranges from 0->20 inclusive.
        :return: A tuple with each variations average results in order, depending on if full results are being calculated and if recursiveNormal is being run.
        """
        if self.outputLevel >= OutLevel.SUM: print(f">>--:>-  Started tests for integer count {self.setCount:3} and absolute sum target index {targetIndex:2}. -<:--<<")
        results = np.empty((50, 2 if self.runReduced else 5), dtype=np.int64)
        
        workerCount = 6 if self.runReduced else 3
        with ThreadPool.ProcessPoolExecutor(max_workers=workerCount) as outerPool:
            tasks = [i + 1 for i in reversed(range(50))]
            activeTests = set()
            try:
                while len(tasks) != 0 or len(activeTests) != 0:
                    while len(activeTests) < workerCount and len(tasks) != 0:
                        activeTests.add(outerPool.submit(self.runSingleTest, targetIndex, tasks.pop()))
                    completedTest = next(ThreadPool.as_completed(activeTests))
                    activeTests.remove(completedTest)
                    testResult = completedTest.result()
                    results[testResult[0]-1] = testResult[1]
            except KeyboardInterrupt:
                outerPool.shutdown(wait=False, cancel_futures=True)
                raise
        
        if self.outputLevel >= OutLevel.SUM: print(f">>--:>- Finished tests for integer count {self.setCount:3} and absolute sum target index {targetIndex:2}. -<:--<<")
        if self.runReduced:
            return (np.mean(results[:, 0]), np.mean(results[:, 1]))
        return (np.mean(results[:, 0]), np.mean(results[:, 1]), np.mean(results[:, 2]), np.mean(results[:, 3]), np.mean(results[:, 4]) if self.runRecurse else np.nan)

    def runSingleTest(self, targetIndex: int, testNum: int) -> tuple[int, tuple[np.int64, np.int64, np.int64, np.int64, np.int64]] | tuple[int, tuple[np.int64, np.int64]]:
        """
        Runs each algorithm once for the full version. Verifies all algorithms returned the same bool, and will record the parameters and which algorithm disagrees if not. Also returns the iteration count of each.
        Uses a python multithreading pool to run each version at the same time.

        :param targetIndex: The size target index of the set. Can be from 0->20 inclusive where 0 is smallest possible, 20 is largest possible, and everything else is increments of 5%.
        :param testNum: The test number (used solely for console output).
        :return: A tuple of the testNum, and a inner tuple of the results in order New Memoized Crazy, Old Memoized Crazy, Memoized Normal, Tabulated Crazy, Tabulated Normal, Recursive Normal, with -1 given if Recursive Normal is too high.
        """
        if self.outputLevel >= OutLevel.BATCH: print(f":>-  Started test take {testNum:2} for specs {self.setCount:3} and {targetIndex:2}. -<:")
        testList = list(self.generateRandomSet(targetIndex))
        officialNames = {"newMemoCrazy": "New Memoized Crazy", "oldMemoCrazy": "Old Memoized Crazy", "memoNormal": "   Memoized Normal", 
                         "tabCrazy": "   Tabulated Crazy", "tabNormal": "  Tabulated Normal", "recurseNormal": "  Recursive Normal"}
    
        with ThreadPool.ProcessPoolExecutor(max_workers=len(self.tasks)) as innerPool:
            futures = {innerPool.submit(worker, name, testList, self.runPython): name for name in self.tasks}
            results = {}
            for future in ThreadPool.as_completed(futures):
                name = futures[future]
                if self.outputLevel >= OutLevel.ALL: print(f"- Finished test for {officialNames[name]} take {testNum:2}. -")
                results[name] = future.result()

        if self.runReduced:
            xnor = [results["newMemoCrazy"][1], results["oldMemoCrazy"][1]]
        else:
            xnor = [results["newMemoCrazy"][1], results["memoNormal"][1], results["tabCrazy"][1], results["tabNormal"][1]]
            if self.runRecurse: 
                xnor.append(results["recurseNormal"][1])
        if len(set(xnor)) > 1:
            with self.disagreeLock:
                self.disagreeList.append(DisagreeData(xnor, self.setCount, targetIndex, testNum, self.sumSizeTarget[targetIndex], testList))
        
        if self.outputLevel >= OutLevel.BATCH: print(f":>- Finished test take {testNum:2} for specs {self.setCount:3} and {targetIndex:2}. -<:")
        if self.runReduced:
            return testNum, (results["newMemoCrazy"][0], results["oldMemoCrazy"][0]) 
        return testNum, (results["newMemoCrazy"][0], results["memoNormal"][0], results["tabCrazy"][0], results["tabNormal"][0], results["recurseNormal"][0] if self.runRecurse else -1) 
