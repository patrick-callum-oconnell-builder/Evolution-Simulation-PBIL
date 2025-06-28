"""
Evolution Simulation Package

A Python wrapper around high-performance C implementations of evolutionary algorithms,
specifically Population Based Incremental Learning (PBIL) for solving MAXSAT problems.
"""

from .pbil import PBILWrapper, run_pbil
from .maxsat_problem import MAXSATProblem

__version__ = "1.0.0"
__all__ = ["PBILWrapper", "run_pbil", "MAXSATProblem"] 