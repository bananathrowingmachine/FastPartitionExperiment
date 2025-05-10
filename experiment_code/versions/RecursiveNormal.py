"""
Solves the partition problem by inputting half the inputs sum into a Subset Sum recursive algorithm that can handle negative numbers. Extremely slow.

This is literally just Jeff Erickson's Subset Sum recursive formula with a single condition change from goal below 0 to goal out of bounds 
His algorithm can be found in Chapter 2, page 77 and Chapter 3, page 116 in his free online algorithms textbook located here: https://www.algorithms.wtf/

Made by bananathrowingmachine on May 9th, 2025.
"""
class RecursiveNormal:
    """
    This is a class solely to make interationCount effectively pass by reference. Storing everything else is just added on because why not if I'm already making the class.
    """
    def __init__(self, inputList: list[int]):
        """
        Creates a "pass by reference" integer and then also stores the input list, answer map, sum of all positives in the input and sum of all negatives in the input is just a easy bonus.

        :param inputList: The inputted list, which is simply stored for easy reference by the algorithm later.
        """
        self.iterationCount = 0
        self.inputList = inputList
        posSum = 0
        negSum = 0
        for num in self.inputList:
            if num > 0:
                posSum += num
            else:
                negSum += num
        self.posSum = posSum
        self.negSum = negSum

    @classmethod
    def testIterations(cls, inputList: list[int]) -> tuple[int, bool]:
        """
        Tests the iteration count of a basic recursive partition algorithm.

        :param inputList: The inputted list to solve the partition question on.
        :return: A tuple containing the iteration count, and the computed answer.
        """
        solver = cls(inputList)
        result = solver.subsetSum(0, int(sum(inputList)/2))
        return solver.iterationCount, result

    def subsetSum(self, index, goal) -> bool:
        """
        Solves the partition problem recursively.

        :param index: The current index of the list the algorithm is considering.
        :param goal: The current goal the algorithm needs to reach to find a valid answer.
        :return: A boolean of if the set (list) can be partitioned.
        """
        if goal == 0:
            return True
        if index >= len(self.inputList):
            return False
        self.iterationCount += 1 # Due to the bounds checking this won't exactly be 2^n and in reality be a little smaller, however since it'll still take ages estimations will be used passed n > 25.
        if goal - self.inputList[index] > self.posSum or goal - self.inputList[index] < self.negSum: # Bounds checking
            return self.subsetSum(index + 1, goal)
        take = self.subsetSum(index + 1, goal - self.inputList[index])
        skip = self.subsetSum(index + 1, goal)
        return take or skip
