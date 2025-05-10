"""
Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.

I literally just copied RecursiveNormal.py and slapped on a answer map (revolutionary stuff over here guys). Therefore the same credit to Jeff Erickson from RecursiveNormal.py applies.
His algorithm can be found in Chapter 2, page 77 and Chapter 3, page 116 in his free online algorithms textbook located here: https://www.algorithms.wtf/

Made by bananathrowingmachine on May 9th, 2025.
"""
class MemoizedNormal:
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
        self.answerMap: dict[tuple[int, int], tuple[bool, bool]] = {}
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
        Tests the iteration count of a partition algorithm that uses top down dynamic programming to allow it solve given inputs quicker.

        :param inputList: The inputted list to solve the partition question on.
        :return: A tuple containing the iteration count, and the computed answer.
        """
        solver = cls(inputList)
        result = solver.subsetSum(0, int(sum(inputList)/2))[1 if sum(inputList) == 0 else 0]
        return solver.iterationCount, result
    
    def subsetSum(self, index, goal) -> tuple[bool, bool]:
        """
        Solves the partition problem recursively.

        :param index: The current index of the list the algorithm is considering.
        :param goal: The current goal the algorithm needs to reach to find a valid answer.
        :return: A boolean of if the set (list) can be partitioned, as well as a boolean for if at least one item has been taken.
        """
        self.iterationCount += 1

        if goal == 0:
            return True, False
        if index >= len(self.inputList):
            return False, False
        
        if goal - self.inputList[index] > self.posSum or goal - self.inputList[index] < self.negSum: # Bounds checking
            if (index + 1, goal-self.inputList[index]) in self.answerMap:
                take = self.answerMap[(index + 1, goal-self.inputList[index])][0]
            else:
                take = self.subsetSum(index + 1, goal-self.inputList[index])[0]
        else: take = False
        if (index + 1, goal) in self.answerMap:
            skip, notEmpty = self.answerMap[(index + 1, goal)]
        else:
            skip, notEmpty = self.subsetSum(index + 1, goal)

        self.answerMap[(index, goal)] = (take or skip, take or notEmpty)
        return take or skip, take or notEmpty