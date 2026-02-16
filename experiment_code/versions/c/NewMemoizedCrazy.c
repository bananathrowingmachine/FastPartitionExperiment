/**
 * NewMemoizedCrazy.py written completely in C. For more information check there.
 * NOT IMPLEMENTED YET THIS JUST PUTS THE ARRAYS SUM IN ITERATIONCOUNT AND RETURNS TRUE (used for C->Python testing)
 *
 * Made by bananathrowingmachine on Feb 16, 2026.
 */
#include <khash.h>
#include <stdbool.h>
#include <typedefs.h>

/**
 * Tests the iteration count of a basic recursive partition algorithm.
 */
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
 * Solves the subset sum problem recursively.
 * NOT IMPLEMENTED YET THIS JUST PUTS THE ARRAYS SUM IN ITERATIONCOUNT AND RETURNS TRUE (used for C->Python testing)
 */
static bool subsetSum(Constants* constants, int index, int goal, int* iterationCount) {
  for (int i = 0; i < constants->listLength; i++)
    *iterationCount += constants->inputList[i];
  *iterationCount *= 1;
  return true;
}