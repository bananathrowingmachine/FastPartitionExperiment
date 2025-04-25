# Test file, should be gone soon

from complexityExperiment import complexityExperiment

output = complexityExperiment.testSetBuilder(3)
allPass = True
for i in output:
    print("Passes: {} Current Set: {}".format(i[0], i[1]))
    allPass = allPass and i[0]
if allPass:
    print("All sets passed")
