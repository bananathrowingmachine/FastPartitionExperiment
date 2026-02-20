/**
 * Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.
 *
 * Made by bananathrowingmachine on Feb 19, 2026.
 */
#include <typedefs.h>

static Output partition(Constants* constants, int index, int goal);

/**
 * Tests the iteration count of a basic recursive partition algorithm.
 */
Output testIterations(int* inputList, int listLength) {
  Constants constants;
  constants.inputList = inputList;
  constants.listLength = listLength;
  constants.posSum = 0;
  constants.negSum = 0;
  for (int i = 0; i < listLength; i++) {
    if (inputList[i] > 0)
      constants.posSum += inputList[i];
    else
      constants.negSum += inputList[i];
  }
  return partition(&constants, 0, (constants.posSum + constants.negSum) / 2);
}

/**
 * Solves the partition problem with dynamic programming.
 */
static Output partition(Constants* constants, int index, int goal) {
  int absNegSum = -constants->negSum;
  int sumRange = constants->posSum + absNegSum + 1;
  uint8_t* prev = calloc(sumRange, sizeof(uint8_t));
  uint8_t* next = malloc(sumRange);
  prev[absNegSum] = 1;

  for (int i = constants->listLength - 1; i >= 0; i--) {
    uint8_t* temp = prev;
    prev = next;
    next = temp;
    for (int j = constants->negSum; j <= constants->posSum; j++) {
      int nextGoal = j - constants->inputList[i];
      if (nextGoal > constants->posSum || nextGoal < constants->negSum)
        next[j + absNegSum] = prev[j + absNegSum];
      else
        next[j + absNegSum] = prev[j + absNegSum] || prev[nextGoal + absNegSum];
    }
  }

  Output output;
  output.iterationCount = sumRange * constants->listLength;
  output.result = next[(constants->posSum - absNegSum) / 2 + absNegSum];
  return output;
}