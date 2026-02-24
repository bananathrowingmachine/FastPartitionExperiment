/**
 * Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.
 * Additionally uses an absolute value trick to reduce the dynamic programming array by half.
 * UNFINISHED
 *
 * Made by bananathrowingmachine on Feb 24, 2026.
 */
#include <typedefs.h>

static Output partition(Constants* constants, int index, int goal);

Output testIterations(int* inputList, int listLength) {
  Constants constants;
  constants.posSum = 0;
  for (int i = 0; i < listLength; i++) {
    int absNumber = abs(inputList[i]);
    constants.posSum += absNumber;
    inputList[i] = absNumber;
  }
  constants.inputList = inputList;
  constants.listLength = listLength;
  return partition(&constants, 0, constants.posSum / 2);
}

/**
 * Solves the partition problem with dynamic programming.
 */
static Output partition(Constants* constants, int index, int goal) {
  uint8_t* prev = calloc(goal + 1, sizeof(uint8_t));
  uint8_t* next = malloc(goal + 1);

  for (int i = constants->listLength - 1; i >= 0; i--) {
    uint8_t* temp = prev;
    prev = next;
    next = temp;
    next[0] = 1;
    for (int j = 1; j < goal + 1; j++) {
      next[j] = prev[j] || (constants->inputList[i] <= j && prev[j - constants->inputList[i]]);
    }
  }

  Output output;
  output.iterationCount = goal * constants->listLength;
  output.result = next[goal];
  return output;
}