"""
Builds theoretical time complexities of my recursive dp table culling method, and the crazy math DP (which is O(nM/2) compared to regular partition which is O(nM)) complexity for reference)
Results are here (this sheet is bad im gonna remake it): https://docs.google.com/spreadsheets/d/1EVpkLWv8gCQcz2yu1IRJDw23yp9A61_KYahQDJ6xTzY/edit?usp=sharing
"""
import random

def dpTableBuilder(index, goal):
    """
    Recursively builds a DP table for the DP algorithm, so that it doesn't do unnecessary problems.
    """
    if goal == 0 or goal < 0 or index == len(inputArr):
        return
    if (index, goal) not in dpDict:
        dpDict[(index, goal)] = None
        dpTableBuilder(index + 1, goal - inputArr[index])
        dpTableBuilder(index + 1, goal)
    
def newExperiement(size: int, givenInts: list[int]) -> tuple[int, int]:
    """
    Creates a test input for checking operation count of 

    :param size: The amount of random numbers to add to the testInput
    :param givenInts: Any pre determined ints to add to the testInput
    """
    global dpDict
    dpDict = {}
    global inputArr
    inputArr = []
    if len(givenInts) != 0:
        inputArr.extend(givenInts)
    for _ in range(size):
        inputArr.append(random.randint(-32768, 32767))
    absValueInput = list(map(abs, inputArr))
    if sum(absValueInput) % 2 == 1: # make sure it's even
        absValueInput[0] = absValueInput[0] + 1
    dpTableBuilder(0, sum(absValueInput)/2)
    return (len(dpDict) * 2, (size * sum(absValueInput))/2)

"""
For complexity experiments
"""
print("How many rounds do you want averaged out?")
rounds = int(input())
print("What is your desired max n?")
endProblemSize = int(input())
print("Do you have any required ints?")
stringInput = input().split(' ')
inputList = []
for value in stringInput:
    inputList.append(int(value))

for size in range(1, endProblemSize+1):
    cullingData = [] # For the theoretical operations count of my recursive culling method with the crazy halving math
    dpingData = [] # For just using dynamic programming with M/2 math
    for round in range(1, rounds+1):
        result = newExperiement(size-len(inputList), inputList)
        cullingData.append(result[0])
        dpingData.append(result[1])
    print(str(sum(cullingData)/rounds) + ", " + str(sum(dpingData)/rounds))
