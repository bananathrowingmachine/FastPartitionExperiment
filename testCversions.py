from experiment_code.versions.python.RecursiveNormal import RecursiveNormal
from experiment_code.versions.c_bin._NewMemoizedCrazy import ffi
from FastPartitionExperiment import buildCLibrary
from pathlib import Path
buildCLibrary(Path(__file__).resolve().parent / "experiment_code" / "versions")
from experiment_code.versions.c_bin._RecursiveNormal import lib as RecursiveNormalC

testList = [1, 2, 3]
testListC = ffi.new("int[]", testList)
result = RecursiveNormalC.testIterations(testListC, len(testListC)) 
result = (result.iterationCount, bool(result.result))
print(result)
print(RecursiveNormal.testIterations(testList))