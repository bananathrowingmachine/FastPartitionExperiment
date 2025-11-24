"""
Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.
This version however uses a as many hueristics as possible that still keep the result completely accurate that I could find.
Out of all the versions of partition, this is the most original, as all the hueristics are my idea, while the general partition/subset sum algorithm itself is written by Jeff Erickson and then translated for this experiment.

This partition algorithm is mostly just Jeff Erickson's Subset Sum algorithm with a reverse memoization order, some extra hueristics, then the crazy math translation into a solution to partition.
His version can be found in Chapter 3, pages 116 and 117 in his free online algorithms textbook located here: http://algorithms.wtf/

Made by bananathrowingmachine on Nov 23rd, 2025.
"""
class NewMemoizedCrazy:
    """
    This is a class solely to make iterationCount effectively pass by reference. Storing the answer map and input list is just an extra bonus.
    """
    def __init__(self, inputList: list[int]):
        """
        Creates a "pass by reference" integer and then also stores the absolute list and answer map for ease of use.

        :param inputList: The inputted list, which will mapped to a list of absolute values in the input.
        """
        self.inputList = inputList
        self.absoluteList = list(map(abs, inputList))
        self.answerMap: dict[tuple[int, int], bool] = {}
        self.extraIterations = 0

    @classmethod
    def testIterations(cls, inputList: list[int]) -> tuple[int, bool]:
        """
        Tests the iteration count of a very slightly modified subset sum that uses top down dynamic programming with a bit of extra input and output code to produce an answer to partition for the same input.

        :param inputList: The inputted list, which will mapped to a list of absolute values in the input internally.
        :return: A tuple containing the iteration count, and the computed answer.
        """
        solver = cls(inputList)
        result = solver.subsetSum(0, int(sum(inputList)/2))
        return len(solver.answerMap) + solver.extraIterations, result # Since the answer map is added to each recursive call, it's length is an iteration count.

    def subsetSum(self, index, goal) -> bool:
        """
        Recursively solves the subset sum problem with inputs for partition. 

        :param index: The current index of the list the algorithm is considering.
        :param goal: The current goal the algorithm needs to reach to find a valid answer.
        :return: A boolean of if the set (list) can be partitioned.
        """
        if goal == 0:
            return True
        self.extraIterations += len(self.absoluteList[index:])
        if sum(self.inputList[index:]) % 2 == 1:
            return False
        self.extraIterations += len(self.absoluteList[index:])
        if sum(self.inputList[index:]) == 0:
            return True
        self.extraIterations += len(self.absoluteList[index:]) * 2
        if max(self.absoluteList[index:]) > sum(self.absoluteList[index:])/2:
            return False
        if index >= len(self.absoluteList):
            return False
        
        if goal >= self.absoluteList[index]: # Bounds checking, better than the others though as it can use the current goal.
            if (index + 1, goal-self.absoluteList[index]) in self.answerMap:
                take = self.answerMap[(index + 1, goal-self.absoluteList[index])]
            else:
                take = self.subsetSum(index + 1, goal-self.absoluteList[index])
            if take == True: # This causes OR short circuiting behavior. 
                self.answerMap[(index, goal)] = True
                return True

        if (index + 1, goal) in self.answerMap:
            skip = self.answerMap[(index + 1, goal)]
        else:
            skip = self.subsetSum(index + 1, goal)
        
        self.answerMap[(index, goal)] = skip
        return skip