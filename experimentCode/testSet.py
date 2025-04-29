# Test file, should be gone soon

from complexityExperiment import complexityExperiment

avgSumDev = 0
fails = 0
for i in range(1, 21):
    sumDev, newFails = complexityExperiment.testSetBuilder(i*5)
    avgSumDev += sumDev
    fails += newFails
print("Avergae sum deviation was {:.5f}%. Amount of fails was {}.".format(avgSumDev, fails))

