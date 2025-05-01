"""
Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.
However this version also does some crazy math to speed things up (or at least that's what I'm testing and making this entire project for) so it's a bit more odd.
Out of all the versions of partition, this is the one that is the most my own, the others are practically straight copies. 

This partition algorithm is mostly just Jeff Erickson's Subset Sum algorithm with a reverse memoization order, like 2 extra things, then the crazy math translation into a solution to partition.
His version can be found in Chapter 3, pages 116 and 117 in his free online algorithms textbook located here: https://www.algorithms.wtf/

Made by bananathrowingmachine on May 1st, 2025.
"""
class MemoizedCrazy:
    """
    This is a class solely to make interationCount effectively pass by reference. Storing the answer map and input list is just an extra bonus.
    """
    def __init__(self, inputList: list[int]):
        """
        Creates a "pass by reference" integer and then also stores the absolute list and answer map for ease of use.

        :param inputList: The inputted list, which will mapped to a list of absolute values in the input.
        """
        self.iterationCount = 0
        self.absoluteList = list(map(abs, inputList))
        self.answerMap: dict[tuple[int, int], int] = {}

    @classmethod
    def testIterations(cls, inputList: list[int]) -> tuple[int, bool]:
        """
        Tests the iteration count of a very slightly modified subset sum that uses top down dynamic programming with a bit of extra input and output code to produce an answer to partition for the same input.

        :param inputList: The inputted list, which will mapped to a list of absolute values in the input internally.
        :return: A tuple containing the iteration count, and the computed answer.
        """
        solver = cls(inputList)
        answer = solver.subsetSum(0, int(sum(solver.absoluteList)/2))
        if sum(inputList) == 0:
            return (solver.iterationCount,  answer > 2)
        return (solver.iterationCount, answer > 0)

    def subsetSum(self, index, goal) -> int:
        """
        Recursively solves the subset sum problem with inputs for partition. 

        :param index: The current index of the list the algorithm is considering.
        :param goal: The current goal the algorithm needs to reach to find a valid answer.
        :return: A int of how many different solutions have been found to successfully partitioning the set (list).
        """
        self.iterationCount += 1

        if goal == 0:
            return 1
        if index >= len(self.absoluteList):
            return 0
        
        if goal >= self.absoluteList[index]:
            if (index + 1, goal-self.absoluteList[index]) not in self.answerMap:
                withResult = self.subsetSum(index + 1, goal-self.absoluteList[index])
            else:
                withResult = self.answerMap[(index + 1, goal-self.absoluteList[index])]
        else: withResult = 0
        if (index + 1, goal) not in self.answerMap:
            withoutResult = self.subsetSum(index + 1, goal)
        else:
            withoutResult = self.answerMap[(index + 1, goal)]
        
        self.answerMap[(index, goal)] = withResult + withoutResult
        return withResult + withoutResult