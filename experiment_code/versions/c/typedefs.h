/**
 * Input and output structs/function for the C versions.
 *
 * Made by bananathrowingmachine of Feb 16, 2024
 */

typedef struct Constants {
  int* inputList;
  int listLength;
  int posSum;
  int negSum;
} Constants;

typedef struct Output {
  int iterationCount;
  bool result;
} Output;

Output testIterations(int* inputList, int listLength);

static bool subsetSum(Constants* constants, int index, int goal, int* iterationCount);