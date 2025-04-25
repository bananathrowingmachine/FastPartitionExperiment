# Test file, should be gone soon

from complexityExperiment import complexityExperiment

with open("deviationResults.txt", "w") as f:
    f.write("Reset results.\n")
for i in range(0, 51):
    testSize = i * 5 if i != 0 else 2 # 2 is the minimum, then go to 5 and increment by 5.
    result = complexityExperiment.testSetBuilder(testSize)
    with open("deviationResults.txt", "a") as f:
        if result >= 200:
            f.write("Test size {} had error rate of {} up until deviation divisor 200, having never gone over the maximum fail rate. Moving on.\n".format(testSize, result[1]))
        else:
            f.write("Test size {} could handle a deviation divisor up to {}, before going over a 0.05%% fail rate. Moving on.\n".format(testSize, result[0]))

