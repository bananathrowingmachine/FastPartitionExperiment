/**
 * Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.
 *
 * Made by bananathrowingmachine on Feb 24, 2026.
 */
#include <khash.h>
#include <typedefs.h>

static uint8_t subsetSum(Constants* constants, int index, int goal, int* iterationCount, khash_t(answerMap) * h);

KHASH_MAP_INIT_INT(answerMap, uint8_t)

/**
 * Tests the iteration count of a basic recursive partition algorithm. gg
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
  khash_t(answerMap)* h = kh_init(answerMap);
  Output output;
  output.iterationCount = 0;
  output.result = subsetSum(&constants, 0, (constants.posSum + constants.negSum) / 2, &output.iterationCount, h);
  kh_destroy(answerMap, h);
  return output;
}

/**
 * Solves the subset sum problem recursively.
 */
static uint8_t subsetSum(Constants* constants, int index, int goal, int* iterationCount, khash_t(answerMap) * h) {
  int ret;
  khiter_t k;
  if (goal == 0)
    return 1;
  if (index >= constants->listLength)
    return 0;

  int goalDiff = goal - constants->inputList[index];
  if (goalDiff < constants->posSum && goalDiff > constants->negSum) {
    int num = index + 1 + goalDiff;
    k = kh_get(answerMap, h, num);
    if (k != kh_end(h)) {
      // to do
    }
  }
}