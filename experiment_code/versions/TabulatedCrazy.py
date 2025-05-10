"""
Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.
This version however uses some crazy math I discovered to help speed things up (or that's at least what I'm creating the entire complexity experiment to test). 
Out of all the versions of partition, this is a lot more my own than the others, as the crazy math is my own, while the general partition/subset sum algorithm itself is written by Jeff Erickson and then translated for this experiment.

This partition algorithm is mostly just Jeff Erickson's Subset Sum algorithm, with a small driver to translate partition into subset sum with the crazy math.
His version can be found in Chapter 3, pages 116 and 117 in his free online algorithms textbook located here: http://algorithms.wtf/

Made by bananathrowingmachine on May 9th, 2025.
"""
def testIterations(inputList: list[int]) -> tuple[int, bool]:
    """
    Finds a few details about the input set then send it off to partition and returns it's answer directly. Since this algorithm is not recursive, absolutely no need to make the wrapper class like for the others.

    :param inputList: The inputted list to solve the partition question on.
    :return: A tuple containing the iteration count, and the computed answer.
    """
    absList = map(abs, inputList)
    return partition(absList)

def partition(inputList: list[int]) -> tuple[int, bool]:
    """
    Finds a few details about the input set then send it off to partition and returns it's answer directly.

    :param inputList: The inputted list to solve the partition question on.
    :return: A tuple containing the iteration count, and the computed answer.
    """
    goal = int(sum(inputList) / 2)
    resultsTable = [[None for _ in range(goal)] for _ in range(len(inputList))]
    resultsTable.append([False for _ in range(goal)])
    resultsTable[len(inputList)][0] = True
    
    for i in reversed(range(0, len(inputList))):
        for j in range(0, inputList[i] - 1):
            resultsTable[i][j] = resultsTable[i+1][j]
        for j in range(inputList[i] - 1, goal):
            resultsTable[i][j] = resultsTable[i+1][j] or resultsTable[i+1][j-inputList[i]]
    
    return (goal * len(inputList), resultsTable[0][goal]) # The iterations count will always be exactly the size of the tabulation table that is not predetermined (aka not a edge case bound).