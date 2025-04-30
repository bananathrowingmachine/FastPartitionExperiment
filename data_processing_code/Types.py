"""
Stores types used across multiple files to organize data transfer.

Made by bananathrowingmachine on Apr 29th, 2025
"""
from collections import namedtuple
from numpy import dtype, int64, float64

RawResultsDType = dtype([
    ('targetSum', int64),
    ('memoCrazy', float64), 
    ('memoNormal', float64), 
    ('tabNormal', float64), 
    ('recurseNormal', float64) 
])

ResultsWrapper = namedtuple('ResultsWrapper', ['IntCount', 'RawData', 'RanRecurse'])
