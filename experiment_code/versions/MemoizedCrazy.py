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
        result = solver.subsetSum(0, int(sum(inputList)/2))[1 if sum(inputList) == 0 else 0]
        return solver.iterationCount, result

    def subsetSum(self, index, goal) -> tuple[bool, bool]:
        """
        Recursively solves the subset sum problem with inputs for partition. 

        :param index: The current index of the list the algorithm is considering.
        :param goal: The current goal the algorithm needs to reach to find a valid answer.
        :return: A boolean of if the set (list) can be partitioned, as well as a boolean for if at least one item has been taken.
        """
        self.iterationCount += 1

        if goal == 0:
            return True, False
        if index >= len(self.absoluteList):
            return False, False
        
        if goal >= self.absoluteList[index]: # Bounds checking, better than the others though as it can use the current goal.
            if (index + 1, goal-self.absoluteList[index]) in self.answerMap:
                take = self.answerMap[(index + 1, goal-self.absoluteList[index])][0]
            else:
                take = self.subsetSum(index + 1, goal-self.absoluteList[index])[0]
        else: take = False
        if (index + 1, goal) in self.answerMap:
            skip, notEmpty = self.answerMap[(index + 1, goal)]
        else:
            skip, notEmpty = self.subsetSum(index + 1, goal)
        
        self.answerMap[(index, goal)] = take or skip, take or notEmpty
        return take or skip, take or notEmpty