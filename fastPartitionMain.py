"""
CHANGE APPROACH!

This is an astronomically fast partition algorithm. Partition is the problem of determining if a set of integers can be split into 2 subsets with equal sum and no intersection.
A lot of credit goes to Jeff Erickson, author of https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf, a free online textbook for my university algorithms class.
His version of fastSubsetSum (pg 116, 117) is the backbone of this algorithm, I mostly modified how it runs. 

This is hopefully understandable, but I use a lot of unique python features (like the fact that dictionaries are ordered)
In /variations, I will eventually provide this algorithm but made in c++ just to help others understand how to make it work.
Finally, after the other variations are done I will attempt to make a version that does the same general idea of making sure 2 recursive calls don't solve the same subproblem, but without the loop over everything to finish off. Language TBD

Made by bananathrowingmachine, [insert date here].
"""
class dpObject:
    """
    A culled dynamic programming table object for solving partition. Takes the input, builds the culled dynamic programming table and the linked order list, then seamlessly combines them using sneaky class methods and an pop iterator.
    My version of partition uses unintuative math to allow any set to be get a definite answer by running a subsetSum algorithm with only positives, looking for abs(sum(input))/2.
    """
    def __init__(self, absInputArray: list[int]):
        """
        Builds a culled dynamic programming table object. Takes the designated input and builds the table dictionary and the order list.
        Realistic implementations would probably just have a dictionary and order list.
        """
        self.__dpTableDict__: dict[tuple[int, int], int] = {}
        self.__dpSubProblemStack__: list[tuple[int, int]] = [] # While in reality it's a list as Python has no "real" stack, this is used like a stack, think of it as one.
        self.__userInput__ = absInputArray
        self.__dpTableBuilder__(0, int(sum(self.__userInput__)/2)) # To accurately build, give the builder the set of inputs that correspond to the answer.

    def __iter__(self):
        """
        Initializes the iterator for moving through the problems.
        """
        return self

    def __next__(self):
        """
        Pops the sub problem stack until it is empty.

        :return: The tuple of (index, pair) stored at the top of the stack.
        """
        if not self.__dpSubProblemStack__:
            raise StopIteration
        self.iterator = self.__dpSubProblemStack__.pop()
        return self.iterator

    def __dpTableBuilder__(self, index: int, goal: int):
        """
        Recursively builds the dynamic programming table for the dpObject. Should only be used in the constructor.

        :param index: The current index we're at in the input.
        :param goal: The current goal (the inputted goal minus any values already picked)
        """
        if goal == 0 or index == len(self.__userInput__): # If the problem has a recursive base case answer, skip, these can be computed in O(1) by the DP algorithm.
            return
        if (index, goal) not in self.__dpTableDict__: 
            # If the problem has not already been recorded.
            self.__dpTableDict__[(index, goal)] = None 
            if goal > self.__userInput__[index]: # Only "take" if the value at index is smaller than goal.
                self.__dpTableBuilder__(index + 1, goal - self.__userInput__[index]) # The "take" option.
            self.__dpTableBuilder__(index + 1, goal) # The "leave" option.
        else:
            # If a problem checks that this is already here
            del self.__dpTableDict__[(index, goal)]
            self.__dpTableDict__[(index, goal)] = None 
    
    def getAnswer(self, index, goal) -> int:
        """
        Finds the currently recorded answer for the index, goal pair. If none exists, it's a base case, so it calculates it.

        :param index: The index value of the table entry.
        :param goal: The goal value of the table entry.
        :return: The int recorded as the answer. None if pair doesn't exist.
        """
        if (index, goal) in self.__dpTableDict__:
            return self.__dpTableDict__[(index, goal)]
        if goal == 0:
            return 1
        return 0
    
    def setAnswer(self, index, goal, answer):
        """
        Sets the currently recorded answer for the index, goal pair to the given answer.

        :param index: The index value of the table entry.
        :param goal: The goal value of the table entry.
        :param answer: The new answer of the table entry.
        """
        if (index, goal) in self.__dpTableDict__:
            self.__dpTableDict__[(index, goal)] = answer

    def elementAt(self, index) -> int:
        """
        Finds the element in the user input and index.

        :param index: The index to grab a value from.
        :return: The value stored at that location in the input.
        """
        return self.__userInput__[index]
    
    def getFinalAnswer(self) -> int:
        """
        Returns the final answer. Should only be called once the iterator stops.

        :return: The final answer.
        """
        return self.__dpTableDict__[(0, sum(self.__userInput__)/2)]

def superFastSubsetSum(inputSet: set[int]) -> int:
    """
    This actually solves the problem. It does so using the iterator I made for dpObject which iterates over the stack in a natural order, computing each subproblem it finds.
    How it does this, is with the index, goal pair given to it by the iterator, it will try the take/leave options relative to it (index+1, goal-input[i]) and (index+1, goal).
    If the dpTable does not have an entry, which means that the entry is a base case, formulate the base case (an easy boolean formula) and then add them up. Return final number back to the table.
    """
    dpTable = dpObject(list(map(abs, inputSet)))
    for subProb in dpTable:
        index = subProb[0]
        goal = subProb[1]
        resultWith = dpTable.getAnswer(index + 1, goal - dpTable.elementAt(index))
        resultWithout = dpTable.getAnswer(index + 1, goal)
        dpTable.setAnswer(index, goal, resultWith + resultWithout)
    return dpTable.getFinalAnswer()

def outerShell(inputSet: set[int]) -> bool:
    """
    Converts the results of superFastSubsetSum into a boolean and is the official output of the algorithm, which changes depending on different inputs.
    """
    totalSolutions = superFastSubsetSum(inputSet)
    print(totalSolutions)
    return False

outerShell({1, 2, 7, -3, -5, -2})