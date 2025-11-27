"""
Stores types used across multiple files to organize data transfer.

Made by bananathrowingmachine on Nov 27th, 2025
"""
from collections import namedtuple
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from typing import Union

# Float64 max values = finfo(resolution=1e-15, min=-1.7976931348623157e+308, max=1.7976931348623157e+308, dtype=float64)
FullResultsDType = np.dtype([
    ('targetSum', np.uint64),
    ('newMemoCrazy', np.float64), 
    ('memoNormal', np.float64), 
    ('tabCrazy', np.float64),
    ('tabNormal', np.float64), 
    ('recurseNormal', np.float64) 
])

SpeedyResultsDType = np.dtype([
    ('targetSum', np.uint64),
    ('newMemoCrazy', np.float64), 
    ('oldMemoCrazy', np.float64), 
])

MachinePredResultsDType = np.dtype([
    ('newMemoCrazy', np.float64), 
    ('memoNormal', np.float64), 
    ('tabCrazy', np.float64),
    ('tabNormal', np.float64), 
])

UnionDType = Union[FullResultsDType, SpeedyResultsDType, MachinePredResultsDType]

ResultsWrapper = namedtuple('ResultsWrapper', ['IntCount', 'RawData', 'RecurseEstimate'])

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
        
