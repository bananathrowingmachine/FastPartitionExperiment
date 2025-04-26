"""
Solves the partition problem using a recursive dynamic programming algorithm, however also does some crazy math.
"""
class memoizedCrazy:
    def __init__(self):
        """
        Algorithm setup. Creates the input and output, parses the incoming numbers then runs partition. Nothing in here is part of the algorithm being tested.
        """
        self.iterationCount = 0
        self.answerMap: dict[tuple[int, int], int] = {}
        self.absoluteList: list[int] = []

    @classmethod
    def testIterations(cls, inputSet: set[int]) -> tuple[int, bool]:
        """
        Creates a new instance of the problem, runs the input on it, then returns iteration count, as well as if the set can or cannot be subdivided.
        """
        solver = cls()
        answer = solver.partition(inputSet)
        return (solver.iterationCount, answer)

    def partition(self, inputSet: set[int]) -> bool:
        """
        Converts the results of subsetSum into a boolean depending on certain conditions. Converts input into a list of absolute values.
        """
        for number in inputSet:
            self.absoluteList.append(abs(number))
        if sum(inputSet) == 0 and 0 in inputSet:
            return True
        answer = self.subsetSum(0, sum(self.absoluteList)/2)
        if sum(inputSet) == 0:
            return answer > 2
        return answer > 0

    def subsetSum(self, index, goal) -> int:
        """
        Recursively solves the subset sum problem with inputs for partition. 
        """
        self.iterationCount += 1
        if goal == 0:
            return 1
        if index >= len(self.absoluteList):
            return 0
        withResult = 0
        withoutResult = 0
        if goal >= self.absoluteList[index]:
            if (index+1, goal-self.absoluteList[index]) not in self.answerMap:
                withResult = self.subsetSum(index+1, goal-self.absoluteList[index])
            else:
                withResult = self.answerMap[(index+1, goal-self.absoluteList[index])]
        if (index+1, goal) not in self.answerMap:
            withoutResult = self.subsetSum(index+1, goal)
        else:
            withoutResult = self.answerMap[(index+1, goal)]
        self.answerMap[(index, goal)] = withResult + withoutResult
        return withResult + withoutResult