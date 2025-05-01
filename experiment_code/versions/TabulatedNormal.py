"""
Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.

This is heavily inspired from Jeff Erickson's Subset Sum algorithm but it has a few notable changes, mainly in handing negative numbers and the changes needed to do that effectively as well as solve specifically for partition.
His algorithm can be found in Chapter 3, page 117 in his free online algorithms textbook located here: https://www.algorithms.wtf/

Made by bananathrowingmachine on May 1st, 2025.
"""
def testIterations(inputList: list[int]) -> tuple[int, bool]:
    """
    Finds a few details about the input set then send it off to partition and returns it's answer directly. Since this algorithm is not recursive, absolutely no need to make the wrapper class like for the others.

    :param inputList: The inputted list to solve the partition question on.
    :return: A tuple containing the iteration count, and the computed answer.
    """
    posSum = 0
    negSum = 0
    for num in inputList:
        if num > 0:
            posSum += num
        else:
            negSum += num
    return partition(inputList, posSum, negSum)

def partition(inputList: list[int], posSum: int, negSum: int) -> tuple[int, bool]:
    """
    Finds a few details about the input set then send it off to partition and returns it's answer directly.

    :param inputList: The inputted list to solve the partition question on.
    :param posSum: The sum of all the positive integers in the set.
    :param negSum: The sum of all the negative integers in the set.
    :return: A tuple containing the iteration count, and the computed answer.
    """
    sumRange = posSum + abs(negSum) + 1
    resultsTable = list[list[bool]] = [[None for _ in range(sumRange)] for _ in range(len(inputList))]
    resultsTable.append([False for _ in range(sumRange)])
    resultsTable[len(inputList)][0] = True
    
    for i in reversed(range(0, len(inputList))):
        for j in range(negSum, posSum + 1): 
            if j - inputList[i] > posSum or j - inputList[i] < negSum:
                resultsTable[i][j] = resultsTable[i+1][j]
            else:
                resultsTable[i][j] = resultsTable[i+1][j] or resultsTable[i+1][j-inputList[i]]

    iterations = sumRange * len(inputList) # The iterations count will always be exactly the size of the tabulation table.
    if posSum == abs(negSum):
        return (iterations)
    return (iterations, resultsTable[0, (posSum - negSum) / 2])