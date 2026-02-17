"""
Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.

I literally just copied RecursiveNormal.py and slapped on a answer map (revolutionary stuff over here guys). Therefore the same credit to Jeff Erickson from RecursiveNormal.py applies.
His algorithm can be found in Chapter 2, page 77 and Chapter 3, page 116 in his free online algorithms textbook located here: http://algorithms.wtf/

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
        self.inputList = inputList
        self.answerMap: dict[tuple[int, int], bool] = {}
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
        result = solver.subsetSum(0, int(sum(inputList)/2))
        return len(solver.answerMap), result # Since the answer map is added to each recursive call, it's length is an iteration count.
    
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
        
        if goal - self.inputList[index] < self.posSum and goal - self.inputList[index] > self.negSum: # Bounds checking
            if (index + 1, goal-self.inputList[index]) in self.answerMap:
                take = self.answerMap[(index + 1, goal-self.inputList[index])]
            else:
                take = self.subsetSum(index + 1, goal-self.inputList[index])
            if take == True: # This causes OR short circuiting behavior. 
                self.answerMap[(index, goal)] = True
                return True
            
        if (index + 1, goal) in self.answerMap:
            skip = self.answerMap[(index + 1, goal)]
        else:
            skip = self.subsetSum(index + 1, goal)

        self.answerMap[(index, goal)] = skip
        return skip