/**
 * Input and output structs/function for the C versions.
 *
 * Made by bananathrowingmachine of Feb 17, 2024
 */
#include <stdint.h>

typedef struct Constants {
  int* inputList;
  int listLength;
  int posSum;
  int negSum;
} Constants;

typedef struct Output {
  int iterationCount;
  uint8_t result;
} Output;

/**
 * Tests the iteration count of the algorithm it shares a file with.
 *
 * @param inputList List of integers to be tested on.
 * @param listLength Length of the list given above.
 * @returns Struct of the iteration count followed by a boolean on if the input can be partitioned.
 */
Output testIterations(int* inputList, int listLength);
