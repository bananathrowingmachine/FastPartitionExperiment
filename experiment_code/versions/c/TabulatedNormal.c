/**
 * Solves the partition problem using a bottom up dynamic programming algorithm, which is an algorithm that iteratively fills a list of subproblems in reverse order to then end at the answer.
 * NOT IMPLEMENTED YET THIS JUST PUTS THE ARRAYS SUM IN ITERATIONCOUNT AND RETURNS TRUE (used for C->Python testing)
 *
 * Made by bananathrowingmachine on Feb 17, 2026.
 */
#include <immintrin.h>
#include <typedefs.h>

static Output partition(Constants* constants, int index, int goal);

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
  return partition(&constants, 0, (constants.posSum + constants.negSum) / 2);
}

/**
 * Solves the partition problem with vectorized dynamic programming.
 */
static Output partition(Constants* constants, int index, int goal) {
  int sumRange = constants->posSum - constants->negSum + 1;
  // uint8_t prev[sumRange];

  Output output;
  for (int i = 0; i < constants->listLength; i++)
    output.iterationCount += abs(constants->inputList[i]);
  output.iterationCount *= 5;
  // output.result = 1;
  return output;
  /**
   * python example array before and after
   * [[None, None, None, None, None, None, None, None, None, None, None],
   * [None, None, None, None, None, None, None, None, None, None, None],
   * [None, None, None, None, None, None, None, None, None, None, None],
   * [None, None, None, None, None, None, None, None, None, None, None],
   * [None, None, None, None, None, None, None, None, None, None, None],
   * [True, False, False, False, False, False, False, False, False, False, False]]
   *
   * [[True, True, True, True, True, True, True, True, True, True, True],
   * [True, True, True, False, True, True, False, False, True, True, False],
   * [True, True, False, False, True, True, False, False, False, False, False],
   * [True, True, False, False, True, True, False, False, False, False, False],
   * [True, True, False, False, False, False, False, False, False, False, False],
   * [True, False, False, False, False, False, False, False, False, False, False]]
   */
}