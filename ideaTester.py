"""
Results are here: https://docs.google.com/spreadsheets/d/1EVpkLWv8gCQcz2yu1IRJDw23yp9A61_KYahQDJ6xTzY/edit?usp=sharing
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
    
def newExperiement(size: int) -> tuple[int, int]:
    """
    Create a random set of size, then return it's time complexities for recursive culling and the DP approach
    """
    global dpDict
    dpDict = {}
    global inputArr
    inputArr = []
    for _ in range(size): # new random set
        inputArr.append(random.randint(0, 255))
    if sum(inputArr) % 2 == 1: # make sure it's even
        inputArr[0] = inputArr[0] + 1
    dpTableBuilder(0, int(sum(inputArr)/2))
    return (len(dpDict) * 2, size * sum(inputArr))

for size in range(1, 51):
    cullingData = []
    dpingData = []
    for round in range(1, 21):
        result = newExperiement(size)
        cullingData.append(result[0])
        dpingData.append(result[1])
    print(str(sum(cullingData)/20) + ", " + str(sum(dpingData)/20))
