/**
 * Solves the partition problem using a top down dynamic programming algorithm, which is an algorithm that recurses but it stores results of solved subproblems and refers back to them if needed.
 *
 * Made by bananathrowingmachine on Feb 24, 2026.
 */
#include <khash.h>
#include <typedefs.h>

KHASH_MAP_INIT_INT(answerMap, uint8_t)

static uint8_t subsetSum(Constants* constants, int index, int goal, khash_t(answerMap) * h);

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
  khash_t(answerMap)* hashTable = kh_init(answerMap);
  Output output;
  output.result = subsetSum(&constants, 0, (constants.posSum + constants.negSum) / 2, hashTable);
  output.iterationCount = kh_size(hashTable);
  kh_destroy(answerMap, hashTable);
  return output;
}

/**
 * Solves the subset sum problem recursively with memoized answers to prevent calculating the same subproblem multiple times.
 */
static uint8_t subsetSum(Constants* constants, int index, int goal, khash_t(answerMap) * hashTable) {
  int ret;
  khiter_t hashIter;
  if (goal == 0)
    return 1;
  if (index >= constants->listLength)
    return 0;

  int goalDiff = goal - constants->inputList[index];
  if (goalDiff < constants->posSum && goalDiff > constants->negSum) {
    uint8_t take;
    int num = ((uint32_t)(goalDiff) << 7) | (index + 1);
    hashIter = kh_put(answerMap, hashTable, num, &ret);
    if (ret == 0)
      take = kh_val(hashTable, hashIter);
    else
      take = subsetSum(constants, index + 1, goalDiff, hashTable);
    if (take) {
      kh_val(hashTable, kh_put(answerMap, hashTable, num - 1, &ret)) = 1;
      return 1;
    }
  }
  uint8_t skip;
  int num = ((uint32_t)(goal) << 7) | (index + 1);
  hashIter = kh_put(answerMap, hashTable, num, &ret);
  if (ret == 0)
    skip = kh_val(hashTable, hashIter);
  else
    skip = subsetSum(constants, index + 1, goal, hashTable);
  kh_val(hashTable, kh_put(answerMap, hashTable, num - 1, &ret)) = skip;
  return skip;
}