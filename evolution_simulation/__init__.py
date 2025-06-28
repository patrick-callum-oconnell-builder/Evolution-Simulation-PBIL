"""
PBIL (Population Based Incremental Learning) Package

A Python package for PBIL optimization with high-performance C backend for MAXSAT problems.
"""

from .pbil import PBIL
from .maxsat_problem import MAXSATProblem
from .c_interface import CInterface

__version__ = "0.1.0"
__all__ = ["PBIL", "MAXSATProblem", "CInterface"] 