# Test file, should be gone soon

from complexityExperiment import complexityExperiment

setSizeTests = [1, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
with open("deviationResults.txt", "w") as f:
    f.write("Reset results.")
for i in setSizeTests:
    result = complexityExperiment.testSetBuilder(i)
    with open("deviationResults.txt", "a") as f:
        if result >= 200:
            f.write("Size {} had great results up to deviation divisor 200. Continuting.\n".format(i))
        else:
            f.write("Size {} could handle a deviation divisor up to {}.\n".format(i, result))

