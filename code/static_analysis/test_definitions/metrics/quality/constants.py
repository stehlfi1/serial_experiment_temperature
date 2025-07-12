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

# Cognitive Complexity Thresholds (based on SonarQube standards)
SIMPLE_COGNITIVE_THRESHOLD = 5
COMPLEX_COGNITIVE_THRESHOLD = 15
VERY_COMPLEX_COGNITIVE_THRESHOLD = 25

# Halstead Metrics Constants
# These constants are based on Halstead's original work and empirical studies
HALSTEAD_DIFFICULTY_DIVISOR = 3000   # Used for bug prediction: B = V / 3000
HALSTEAD_EFFORT_THRESHOLD = 18       # Threshold for high effort indicators

# Maintainability Index Thresholds (based on Microsoft's Visual Studio standards)
# See: "Maintainability Index Range and Meaning" - Microsoft Documentation
HIGH_MAINTAINABILITY_THRESHOLD = 85    # Green zone: easily maintainable
MODERATE_MAINTAINABILITY_THRESHOLD = 65  # Yellow zone: moderately maintainable
LOW_MAINTAINABILITY_THRESHOLD = 50      # Red zone: difficult to maintain

# Lines of Code Thresholds
SMALL_FUNCTION_LINES = 10     # Functions <= 10 lines are considered small
LARGE_FUNCTION_LINES = 50     # Functions > 50 lines are considered large
VERY_LARGE_FUNCTION_LINES = 100  # Functions > 100 lines are considered very large

# Nesting Depth Thresholds
MAX_RECOMMENDED_NESTING = 4   # Maximum recommended nesting depth
DEEP_NESTING_THRESHOLD = 6    # Threshold for flagging deeply nested code

# Class Size Thresholds
SMALL_CLASS_METHODS = 5       # Classes with <= 5 methods are considered small
LARGE_CLASS_METHODS = 20      # Classes with > 20 methods are considered large
VERY_LARGE_CLASS_METHODS = 50 # Classes with > 50 methods are considered very large