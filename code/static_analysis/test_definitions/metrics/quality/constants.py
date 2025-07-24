"""
Constants for quality analysis metrics.

This module defines thresholds and constants used in code quality analysis
to provide consistent and configurable metrics across all test modules.
"""

# Cyclomatic Complexity Thresholds (based on McCabe's recommendations)
# See: McCabe, T.J. (1976). "A Complexity Measure"
SIMPLE_COMPLEXITY_THRESHOLD = 5      # Functions with CC <= 5 are considered simple
COMPLEX_COMPLEXITY_THRESHOLD = 10    # Functions with CC > 10 are considered complex  
VERY_COMPLEX_COMPLEXITY_THRESHOLD = 20  # Functions with CC > 20 are considered very complex

# Halstead Metrics Constants
# These constants are based on Halstead's original work and empirical studies
HALSTEAD_DIFFICULTY_DIVISOR = 3000   # Used for bug prediction: B = V / 3000
HALSTEAD_EFFORT_THRESHOLD = 18       # Threshold for high effort indicators