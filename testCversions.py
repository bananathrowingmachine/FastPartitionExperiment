from experiment_code.versions.python.MemoizedNormal import MemoizedNormal
from experiment_code.versions.python.OldMemoizedCrazy import OldMemoizedCrazy
from experiment_code.versions.python.NewMemoizedCrazy import NewMemoizedCrazy
import experiment_code.versions.python.TabulatedCrazy as TabulatedCrazy
import experiment_code.versions.python.TabulatedNormal as TabulatedNormal
from experiment_code.versions.python.RecursiveNormal import RecursiveNormal
from FastPartitionExperiment import buildCLibrary
from pathlib import Path
import time

buildCLibrary(Path(__file__).resolve().parent / "experiment_code" / "versions")
from experiment_code.versions.c_bin._MemoizedNormal import lib as MemoizedNormalC
from experiment_code.versions.c_bin._OldMemoizedCrazy import lib as OldMemoizedCrazyC
from experiment_code.versions.c_bin._NewMemoizedCrazy import lib as NewMemoizedCrazyC
from experiment_code.versions.c_bin._TabulatedCrazy import lib as TabulatedCrazyC
from experiment_code.versions.c_bin._TabulatedNormal import lib as TabulatedNormalC
from experiment_code.versions.c_bin._RecursiveNormal import lib as RecursiveNormalC
from experiment_code.versions.c_bin._NewMemoizedCrazy import ffi

# whichever iteration gets tested first seems to always be slower even if retested
startupInput = [11, 13, 17, 19, 29, 31, 41, 43]
NewMemoizedCrazyC.testIterations(ffi.new("int[]", startupInput), len(startupInput)) 

testList = [11, 13, 17, 19, 29, 31, 41, 43]
testListC = ffi.new("int[]", testList)

startTime = time.time_ns()
result = TabulatedCrazyC.testIterations(testListC, len(testList)) 
result = (result.iterationCount, bool(result.result))
endTime = time.time_ns()
print(f"{result} -> {(endTime-startTime)/1000}ms")

startTime = time.time_ns()
result = TabulatedCrazy.testIterations(testList)
endTime = time.time_ns()
print(f"{result} -> {(endTime-startTime)/1000}ms")

startTime = time.time_ns()
result = TabulatedNormalC.testIterations(testListC, len(testList))
result = (result.iterationCount, bool(result.result))
endTime = time.time_ns()
print(f"{result} -> {(endTime-startTime)/1000}ms")

startTime = time.time_ns()
result = RecursiveNormal.testIterations(testList)
endTime = time.time_ns()
print(f"{result} -> {(endTime-startTime)/1000}ms")