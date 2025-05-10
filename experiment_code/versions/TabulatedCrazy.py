"""
Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.
This version however uses some crazy math I discovered to help speed things up (or that's at least what I'm creating the entire complexity experiment to test). 
Out of all the versions of partition, this is a lot more my own than the others, as the crazy math is my own, while the actual partitioning is mostly just Jeff Erickson's subset sum modified.

This partition algorithm is mostly just Jeff Erickson's Subset Sum algorithm, with a small driver to translate partition into subset sum with the crazy math.
His version can be found in Chapter 3, pages 116 and 117 in his free online algorithms textbook located here: https://www.algorithms.wtf/

Made by bananathrowingmachine on May 9th, 2025.
"""
def testIterations(inputList: list[int]) -> tuple[int, bool]:
    """
    Finds a few details about the input set then send it off to partition and returns it's answer directly. Since this algorithm is not recursive, absolutely no need to make the wrapper class like for the others.

    :param inputList: The inputted list to solve the partition question on.
    :return: A tuple containing the iteration count, and the computed answer.
    """
    posSum = 0
    negSum = 0
    absList = []
    for num in inputList:
        if num > 0:
            posSum += num
        else:
            negSum += num
        absList.append(abs(num))
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
    resultsTable = [[False for _ in range(sumRange)] for _ in range(len(inputList))]
    resultsTable.append([False for _ in range(sumRange)])
    resultsTable[len(inputList)][0] = True
    
    for i in reversed(range(0, len(inputList))):
        for j in range(negSum, posSum + 1): 
            if j - inputList[i] > posSum or j - inputList[i] < negSum:
                resultsTable[i][j] = resultsTable[i+1][j]
            else:
                resultsTable[i][j] = resultsTable[i+1][j] or resultsTable[i+1][j-inputList[i]]

    return (sumRange * len(inputList), resultsTable[0][int((posSum - negSum) / 2)]) # The iterations count will always be exactly the size of the tabulation table.