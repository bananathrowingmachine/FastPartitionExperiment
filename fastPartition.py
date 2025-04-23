"""
This is an astronomically fast partition algorithm. Partition is defined on page 405 of the pdf linked below.
A lot of credit goes to Jeff Erickson, author of https://jeffe.cs.illinois.edu/teaching/algorithms/book/Algorithms-JeffE.pdf, a free online textbook for my university algorithms class.

Made by bananathrowingmachine, [insert date here].
"""

def dpTableBuilder(index: int, goal: int) -> dict[(int, int), int]:
    """
    Recursively builds the dynamic programming table for superFastSubsetSum. Returns the table as a dictionary of <inputs as a tuple> for the key and <result> as the value.
    """
    if goal == 0 or goal < 0 or index == len(absInputArray):
        return
    if (index, goal) not in dpTableDict:
        dpTableDict[(index, goal)] = None
        dpTableBuilder(index + 1, goal - absInputArray[index])
        dpTableBuilder(index + 1, goal)

def superFastSubsetSum(inputSet: set[int]) -> int:
    """
    This function was heavily inspired by Jeff Erickson's fastSubsetSum(), pg 116. I essentially use his recurrence for the table builder.
    """
    global absInputArray
    absInputArray = list(map(abs(), inputSet))
    global dpTableDict
    dpTableDict = {}
    dpTableBuilder(0, sum(absInputArray)/2)
    return 0

def outerShell(inputSet: set[int]) -> bool:
    """
    Converts the results of superFastSubsetSum into a boolean and is the official output of the algorithm, which changes depending on different inputs.
    """
    totalSolutions = superFastSubsetSum(inputSet)
    return False