# The eventual graph and data table building code. Currently will just be an example of getting the output from my code and playing around with it.
from experiment_code.complexityExperiment import complexityExperiment

# Currently all numbers are randints or randfloats, there is no meaning to a single one.
seperatorBar = "=============================================================================================="
data = complexityExperiment.testProblemSize(10) 

print(data[0].memoCrazy) # The same thing as above but named

# The rest of the algorithms can be accessed as such.
print(data[0].memoNormal) 
print(data[0].tabNormal)
print(data[0].recurseNormal)
print(seperatorBar)

# The 5th data category, 25% of the way to the max sum size.
print(data[5].memoCrazy) 
print(data[5].memoNormal) 
print(data[5].tabNormal)
print(data[5].recurseNormal)
print(seperatorBar)

# Additionally the sum target can be accessed as such
print(data[0].sumTarget) 


