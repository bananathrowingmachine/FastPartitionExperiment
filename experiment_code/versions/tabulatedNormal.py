"""
Solves the partition problem using a iterative dynamic programming algorithm that tabulates results.
"""
class tabulatedNormal:
    def __init__(self):
        """
        Algorithm setup. Creates the input and output, parses the incoming numbers then runs partition. Nothing in here is part of the algorithm being tested.
        """
        self.iterationCount = 0

    @classmethod
    def testIterations(cls, inputSet: set[int]) -> tuple[int, bool]:
        """
        Creates a new instance of the problem, runs the input on it, then returns iteration count, as well as if the set can or cannot be subdivided.
        """
        solver = cls()
        return (solver.iterationCount, False)