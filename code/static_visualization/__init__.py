"""
Static analysis visualization module.
Generates publication-ready plots and tables for code quality metrics.
"""

from .data_loader import StaticAnalysisDataLoader
from .quality_plots import QualityPlotter

__all__ = [
    'StaticAnalysisDataLoader',
    'QualityPlotter',
]
