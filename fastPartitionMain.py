"""
This is an astronomically fast partition algorithm. Partition is the problem of determining if a set of integers can be split into 2 subsets with equal sum and no intersection.
A lot of credit goes to Jeff Erickson, author of https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf, a free online textbook for my university algorithms class.

This version is designed to be the most understandable, especially for other languages, as python does some funny stuff sometimes.
Do note 1 funny python thing though which is tuples, a set of immutable, ordered, values. Used for returning multiple things from functions, but also as the keys for the dictionary.
In /variations, I will eventually provide this algorithm but made explicity for python, and version in c++.
Another variation to look out for will attempt to record what subproblems are being worked on, and get instances that need the answers to those problems to wait for the only solving it to complete. Language TBD

Made by bananathrowingmachine, [insert date here].
"""
class dpObject:
    """
    A culled dynamic programming table object for solving partition. Takes the input, builds the culled dynamic programming table and the linked order list, then seamlessly combines them with an iterator.
    My version of partition uses unintuative math to allow any set to be get a definite answer by running a subsetSum algorithm with only positives, looking for abs(sum(input))/2.
    """
    def __init__(self, absInputArray: list[int]):
        """
        Builds a culled dynamic programming table object. Takes the designated input and builds the table dictionary and the order list.
        Realistic implementations would probably just have a dictionary and order list.
        """
        self.__dpTableDict__ = dict[tuple(int, int), int]
        self.__dpSubProblemStack__ = list[tuple(int, int)] # While in reality it's a list as Python has no "real" stack, this is used like a stack, think of it as one.
        self.__userInput__ = absInputArray
        self.__dpTableBuilder__(0, sum(self.__userInput__)/2) # To accurately build, give the builder the set of inputs that correspond to the answer.

    def __dpTableBuilder__(self, index: int, goal: int):
        """
        Recursively builds the dynamic programming table for the dpObject. Should only be used in the constructor.

        :param index: The current index we're at in the input.
        :param goal: The current goal (the inputted goal minus any values already picked)
        """
        if goal == 0 or goal < 0 or index == len(self.__userInput__): # If the problem has a recursive base case answer, skip, these can be computed in O(1) by the DP algorithm.
            return
        if (index, goal) not in self.__dpTableDict__: # If the problem has not already been recorded. If it has, do nothing.
            self.__dpTableDict__[(index, goal)] = None 
            self.__dpSubProblemStack__.append((index, goal)) # Since we are building this recursively, the first problems recorded will be the last ones that need to be done.
            self.__dpTableBuilder__(self, index + 1, goal - self.__userInput__[index]) # The "take" option.
            self.__dpTableBuilder__(self, index + 1, goal) # The "leave" option.

    def getSize(self, total = False) -> int:
        """
        Gets the size of the culled dynamic programming table. 

        :param total: If you want the total size (size of the dict), instead of the current size (size of the stack). Defaults to False.
        :return: Size int.
        """
        if total:
            return len(self.__dpTableDict__)
        return len(self.__dpSubProblemStack__)
    
    def getAnswer(self, index, goal) -> int:
        """
        Finds the currently recorded answer for the index, goal pair.

        :param index: The index value of the table entry.
        :param goal: The goal value of the table entry.
        :return: The int recorded as the answer. None if pair doesn't exist.
        """
        if (index, goal) in self.__dpTableDict__:
            return self.__dpTableDict__[(index, goal)]
        return None
    
    def peek(self) -> tuple[int, int, int]:
        """
        Finds the (index, pair) key at the top of the stack, and it's value in the table dictionary.

        :return: The tuple of (index, pair, score) stored at the top of the stack.
        """
        if len(self.__dpSubProblemStack__) == 0:
            return None
        dictKey = self.__dpSubProblemStack__[-1] # [-1] just means the last element in the list.
        return (dictKey[0], dictKey[1], self.__dpTableDict__[(dictKey)])
    
    def pop(self) -> tuple[int, int, int]:
        """
        Removes the (index, pair) key at the top of the stack. Does not remove the associated value in the table dictionary.

        :return: The tuple of (index, pair, score) stored at the top of the stack.
        """
        if len(self.__dpSubProblemStack__) == 0:
            return None
        dictKey = self.__dpSubProblemStack__.pop() # [-1] just means the last element in the list.
        return (dictKey[0], dictKey[1], self.__dpTableDict__[(dictKey)])
    
    def setAnswer(self, index, goal, answer):
        """
        Sets the currently recorded answer for the index, goal pair to the given answer.

        :param index: The index value of the table entry.
        :param goal: The goal value of the table entry.
        :param answer: The new answer of the table entry.
        """
        if (index, goal) in self.__dpTableDict__:
            self.__dpTableDict__[(index, goal)] = answer

def superFastSubsetSum(inputSet: set[int]) -> int:
    """
    This function was heavily inspired by Jeff Erickson's fastSubsetSum(), pg 116. I essentially use his recurrence for the table builder.
    """
    dpTable = dpObject(list(map(abs(), inputSet)))
    return 0

def outerShell(inputSet: set[int]) -> bool:
    """
    Converts the results of superFastSubsetSum into a boolean and is the official output of the algorithm, which changes depending on different inputs.
    """
    totalSolutions = superFastSubsetSum(inputSet)
    return False