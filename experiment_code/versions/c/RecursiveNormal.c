/**
 * Solves the partition problem by inputting half the inputs sum into a Subset Sum recursive algorithm that can handle negative numbers. Extremely slow.
 *
 * This is literally just Jeff Erickson's Subset Sum recursive formula with a single condition change from goal below 0 to goal out of bounds
 * His algorithm can be found in Chapter 2, page 77 and Chapter 3, page 116 in his free online algorithms textbook located here: http://algorithms.wtf/
 *
 * Made by bananathrowingmachine on Feb 17, 2026.
 */
#include <typedefs.h>

static uint8_t subsetSum(Constants* constants, int index, int goal, int* iterationCount);

Output testIterations(int* inputList, int listLength) {
  Constants constants;
  constants.inputList = inputList;
  constants.listLength = listLength;
  for (int i = 0; i < listLength; i++) {
    if (inputList[i] > 0)
      constants.posSum += inputList[i];
    else
      constants.negSum += inputList[i];
  }
  Output output;
  output.iterationCount = 0;
  output.result = subsetSum(&constants, 0, (constants.posSum + constants.negSum) / 2, &output.iterationCount);
  return output;
}

/**
 * Simple, recursive, subset sum algorithm in C. It tries to get the goal to 0 by either subtracting on skipping the next element in the input array.
 *
 * @param constants Pointer to the constants throughtout execution such as the input list.
 * @param index The current index.
 * @param goal The current goal.
 * @param iterationCount Pointer to the algorithm iteration count.
 */
static uint8_t subsetSum(Constants* constants, int index, int goal, int* iterationCount) {
  if (goal == 0)
    return 1;
  if (index >= constants->listLength)
    return 0;
  *(iterationCount)++;
  int nextGoal = goal - constants->inputList[index];
  index++;
  if (nextGoal > constants->posSum || nextGoal < constants->negSum)
    return subsetSum(constants, index, goal, iterationCount);
  return subsetSum(constants, index, goal, iterationCount) || subsetSum(constants, index, nextGoal, iterationCount);
}