def subsetSum(index, goal) -> int:
    global iterationCount
    iterationCount += 1
    if goal == 0:
        return 1
    if index >= len(absoluteList):
        return 0
    withResult = 0
    withoutResult = 0
    global answerMap
    if goal >= absoluteList[index]: # Only bother with withResult if it can fit
        if (index+1, goal-absoluteList[index]) not in answerMap:
            withResult = subsetSum(index+1, goal-absoluteList[index])
        else:
            withResult = answerMap[(index+1, goal-absoluteList[index])]
    if (index+1, goal) not in answerMap:
        withoutResult = subsetSum(index+1, goal)
    else:
        withoutResult = answerMap[(index+1, goal)]
    answerMap[(index, goal)] = withResult + withoutResult
    return withResult + withoutResult

def outerShell() -> bool:
    """
    Converts the results of superFastSubsetSum into a boolean and is the official output of the algorithm, which changes depending on different inputs.
    """
    for number in inputSet:
        absoluteList.append(abs(number))
    if sum(absoluteList) == 0 and 0 in inputSet:
        return True
    answer = subsetSum(0, sum(absoluteList)/2)
    if sum(inputSet) == 0:
        return answer > 2
    return answer > 0

iterationCount = 0
answerMap: dict[tuple[int, int], int] = {}
absoluteList: list[tuple[int, int]] = []
inputSet = {}
inputStrings = input().splitlines()
for strNum in inputStrings:
    inputSet.update(int(strNum))

outerShell() # actually test the program

print(iterationCount)