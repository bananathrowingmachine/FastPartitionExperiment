from experiment_code.versions.python.MemoizedNormal import MemoizedNormal
from experiment_code.versions.python.OldMemoizedCrazy import OldMemoizedCrazy
from experiment_code.versions.python.NewMemoizedCrazy import NewMemoizedCrazy
import experiment_code.versions.python.TabulatedCrazy as TabulatedCrazy
import experiment_code.versions.python.TabulatedNormal as TabulatedNormal
from experiment_code.versions.python.RecursiveNormal import RecursiveNormal
from FastPartitionExperiment import buildCLibrary
from pathlib import Path
buildCLibrary(Path(__file__).resolve().parent / "experiment_code" / "versions")
from experiment_code.versions.c_bin._MemoizedNormal import lib as MemoizedNormalC
from experiment_code.versions.c_bin._OldMemoizedCrazy import lib as OldMemoizedCrazyC
from experiment_code.versions.c_bin._NewMemoizedCrazy import lib as NewMemoizedCrazyC
from experiment_code.versions.c_bin._TabulatedCrazy import lib as TabulatedCrazyC
from experiment_code.versions.c_bin._TabulatedNormal import lib as TabulatedNormalC
from experiment_code.versions.c_bin._RecursiveNormal import lib as RecursiveNormalC
from experiment_code.versions.c_bin._NewMemoizedCrazy import ffi

testList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
testListC = ffi.new("int[]", testList)
result = TabulatedNormalC.testIterations(testListC, len(testListC)) 
result = (result.iterationCount, bool(result.result))
print(result)
print(TabulatedNormal.testIterations(testList))