"""
Stores types used across multiple files to organize data transfer.

Made by bananathrowingmachine on Feb 16, 2026
"""
from collections import namedtuple
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from typing import Union
from enum import StrEnum

class AlgoNames(StrEnum):
    """
    A enum of each of the algorithm names to make declaring which one is wanted more clear
    """
    TargetSum = 'targetSum'
    NewMemoizedCrazy = 'newMemoCrazy'
    OldMemoizedCrazy = 'oldMemoCrazy'
    MemoizedNormal = 'memoNormal'
    TabulatedCrazy = 'tabCrazy'
    TabulatedNormal = 'tabNormal'
    RecursiveNormal = 'recurseNormal'

FullResultsDType = np.dtype([
    (AlgoNames.TargetSum, np.uint32),
    (AlgoNames.NewMemoizedCrazy, np.float64), 
    (AlgoNames.MemoizedNormal, np.float64), 
    (AlgoNames.TabulatedCrazy, np.float64),
    (AlgoNames.TabulatedNormal, np.float64), 
    (AlgoNames.RecursiveNormal, np.float64) 
])

SpeedyResultsDType = np.dtype([
    (AlgoNames.TargetSum, np.uint32),
    (AlgoNames.NewMemoizedCrazy, np.float64), 
    (AlgoNames.OldMemoizedCrazy, np.float64), 
])

MachinePredResultsDType = np.dtype([
    (AlgoNames.NewMemoizedCrazy, np.float64), 
    (AlgoNames.MemoizedNormal, np.float64), 
    (AlgoNames.TabulatedCrazy, np.float64),
    (AlgoNames.TabulatedNormal, np.float64), 
])

UnionDType = Union[FullResultsDType, SpeedyResultsDType, MachinePredResultsDType]

@dataclass(frozen=True)
class ResultsWrapper:
    """
    A helpful wrapper with the current chunk of results and a few other helpful pieces of information.
    """
    IntCount: int
    RecurseEstimate: int
    RawData: np.ndarray = field(default_factory=lambda: np.empty(21, dtype=UnionDType))

@dataclass(frozen=True)
class DisagreeData:
    """
    A combined grouping of all the data needed to log disagreements.
    """
    AlgoOutputs: list[bool]
    IntCount: int
    TargetIndex: int
    TestNum: int
    TargetSum: int
    CurrentList: list[int]

@dataclass()
class DataProcessingInfo:
    """
    A combined grouping of all the different data processing data that goes with each algorithm, used solely in MainDataProcessor.py.
    """
    OfficialName: str
    DataFrame: pd.DataFrame
    BarColor: tuple[float, float, float]
    EdgeColor: tuple[float, float, float]