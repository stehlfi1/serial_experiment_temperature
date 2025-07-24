#!/usr/bin/env python3
"""
Advanced Test Runner for Temperature Research

Implements comprehensive code quality metrics for analyzing temperature impact on LLM-generated code.
Based on the thesis research goals for code quality and structural analysis.
"""

import ast
import sys
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import Counter, defaultdict
from dataclasses import asdict

from ..results.data_models import AdvancedMetrics
from .ast_analyzer import ASTAnalyzer
from ..test_definitions.metrics.quality.complexity_analysis import analyze_complexity_from_analyzer
from ..test_definitions.metrics.quality.halstead_analysis import analyze_halstead_from_analyzer
from ..test_definitions.metrics.quality.size_analysis import analyze_size_from_analyzer
from ..test_definitions.metrics.quality.maintainability_analysis import analyze_maintainability_from_analyzer
# AST analysis is now handled directly by shared ASTAnalyzer



class AdvancedTestRunner:
    """Comprehensive test runner for temperature research metrics."""
    
    def __init__(self):
        self.analyzer = ASTAnalyzer()
    
    def run_all_advanced_tests(self, code_path: Path) -> AdvancedMetrics:
        """Run all advanced tests on a code file."""
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse AST
            tree = ast.parse(source_code)
            
            # Reset analyzer and visit AST (single parse)
            self.analyzer.reset()
            self.analyzer.visit(tree)
            
            # Get data from modular metrics (pass shared analyzer)
            complexity_result = analyze_complexity_from_analyzer(self.analyzer)
            halstead_result = analyze_halstead_from_analyzer(self.analyzer)
            size_result = analyze_size_from_analyzer(self.analyzer, source_code)
            maintainability_result = analyze_maintainability_from_analyzer(self.analyzer, source_code)
            # Get AST data directly from shared analyzer
            ast_result = {
                "ast_node_count": self.analyzer.node_count,
                "ast_depth": self.analyzer.max_depth,
                "ast_node_types": dict(self.analyzer.node_types),
                "ast_unique_node_types": len(self.analyzer.node_types)
            }
            
            # Map to AdvancedMetrics dataclass
            metrics = AdvancedMetrics()
            
            # Map complexity data
            complexity_data = complexity_result["data"]["cyclomatic_complexity"]
            metrics.cyclomatic_complexity = complexity_data["total"]
            metrics.cyclomatic_complexity_per_function = complexity_data["per_function"]
            
            cognitive_data = complexity_result["data"]["cognitive_complexity"]
            metrics.cognitive_complexity = cognitive_data["total"]
            metrics.cognitive_complexity_per_function = cognitive_data["per_function"]
            
            nesting_data = complexity_result["data"]["nesting_depth"]
            metrics.max_nesting_depth = nesting_data["max_overall"]
            metrics.avg_nesting_depth = nesting_data["average"]
            metrics.nesting_depth_per_function = nesting_data["per_function"]
            
            # Map complexity distribution data
            distribution_data = complexity_data["distribution"]
            metrics.simple_function_ratio = distribution_data["simple_ratio"]
            metrics.complex_function_ratio = distribution_data["complex_ratio"]
            metrics.very_complex_function_ratio = distribution_data["very_complex_ratio"]
            
            # Map Halstead data
            metrics.halstead_volume = halstead_result.get("volume", 0)
            metrics.halstead_difficulty = halstead_result.get("difficulty", 0)
            metrics.halstead_effort = halstead_result.get("effort", 0)
            metrics.halstead_time = halstead_result.get("time", 0)
            metrics.halstead_bugs = halstead_result.get("bugs", 0)
            metrics.halstead_length = halstead_result.get("length", 0)
            metrics.halstead_vocabulary = halstead_result.get("vocabulary", 0)
            metrics.halstead_operators = halstead_result.get("operators", {}).get("unique", 0)
            metrics.halstead_operands = halstead_result.get("operands", {}).get("unique", 0)
            metrics.halstead_operator_count = halstead_result.get("operators", {}).get("total", 0)
            metrics.halstead_operand_count = halstead_result.get("operands", {}).get("total", 0)
            
            # Map AST data
            metrics.ast_node_count = ast_result["ast_node_count"]
            metrics.ast_depth = ast_result["ast_depth"]
            metrics.ast_node_types = ast_result["ast_node_types"]
            metrics.ast_unique_node_types = ast_result["ast_unique_node_types"]
            
            # Map size data from modular metrics
            size_data = size_result
            metrics.logical_lines_of_code = size_data["lines"]["logical"]
            metrics.physical_lines_of_code = size_data["lines"]["total"]
            metrics.comment_lines = size_data["lines"]["comments"]
            metrics.blank_lines = size_data["lines"]["blank"]
            metrics.code_to_comment_ratio = size_data["lines"]["code_to_comment_ratio"]
            
            # Function and class metrics
            metrics.function_count = size_data["functions"]["count"]
            metrics.class_count = size_data["classes"]["count"]
            metrics.method_count = size_data["functions"]["method_count"]
            metrics.methods_per_class = size_data["classes"]["methods_per_class"]
            metrics.parameters_per_function = size_data["functions"]["parameters_per_function"]
            metrics.avg_parameters_per_function = size_data["functions"]["avg_parameters_per_function"]
            metrics.wmc_per_class = size_data["classes"]["wmc_per_class"]
            metrics.avg_wmc = size_data["classes"]["avg_wmc"]
            
            # Import metrics
            metrics.import_count = size_data["imports"]["import_statements"]
            metrics.from_import_count = size_data["imports"]["from_import_statements"]
            metrics.unique_imports = size_data["imports"]["unique_modules"]
            metrics.stdlib_imports = size_data["imports"]["stdlib"]
            metrics.third_party_imports = size_data["imports"]["third_party"]
            
            # Map maintainability data from modular metrics
            maintainability_data = maintainability_result["data"]
            metrics.maintainability_index = maintainability_data["maintainability_index"]
            metrics.maintainability_rank = maintainability_data["maintainability_rank"]
            metrics.abc_assignment_count = maintainability_data["abc_assignment_count"]
            metrics.abc_branch_count = maintainability_data["abc_branch_count"]
            metrics.abc_condition_count = maintainability_data["abc_condition_count"]
            metrics.abc_magnitude = maintainability_data["abc_magnitude"]
            
            # Calculate remaining metrics using inline methods (temporary)
            self._calculate_structure_metrics(metrics)
            self._calculate_quality_metrics(metrics, source_code)
            
            return metrics
            
        except Exception as e:
            print(f"Error analyzing {code_path}: {e}")
            return AdvancedMetrics()
    
    
    def _calculate_structure_metrics(self, metrics: AdvancedMetrics):
        """Calculate structural and OOP metrics."""
        # Inheritance metrics
        if self.analyzer.inheritance_depths:
            metrics.depth_of_inheritance = self.analyzer.inheritance_depths.copy()
            metrics.max_dit = max(self.analyzer.inheritance_depths)
            metrics.avg_dit = sum(self.analyzer.inheritance_depths) / len(self.analyzer.inheritance_depths)
        
        # Control flow metrics
        metrics.loop_count = dict(self.analyzer.loops)
        metrics.conditional_count = dict(self.analyzer.conditionals)
        metrics.comprehension_count = dict(self.analyzer.comprehensions)
        
        # Code patterns
        metrics.lambda_count = self.analyzer.lambda_count
        metrics.generator_count = self.analyzer.generator_count
        metrics.decorator_count = self.analyzer.decorator_count
        metrics.docstring_count = self.analyzer.docstring_count
        metrics.return_statement_count = self.analyzer.return_count
        metrics.raise_statement_count = self.analyzer.raise_count
        metrics.assert_statement_count = self.analyzer.assert_count
        
        # Variable usage
        metrics.variable_count = len(self.analyzer.variables)
        metrics.global_variable_count = len(self.analyzer.global_vars)
        metrics.nonlocal_variable_count = len(self.analyzer.nonlocal_vars)
        
        # Operator distribution
        metrics.operator_distribution = dict(self.analyzer.operators)
        
        # Literals
        metrics.string_literal_count = self.analyzer.string_literals
        metrics.number_literal_count = self.analyzer.number_literals
        metrics.boolean_literal_count = self.analyzer.boolean_literals
    
    def _calculate_quality_metrics(self, metrics: AdvancedMetrics, source_code: str):
        """Calculate remaining quality metrics."""
        # Note: Maintainability Index and complexity distribution are now calculated by modular analysis
        
        # Basic naming convention analysis
        identifiers = list(self.analyzer.variables) + [f['name'] for f in self.analyzer.functions] + [c['name'] for c in self.analyzer.classes]
        if identifiers:
            snake_case_count = sum(1 for name in identifiers if re.match(r'^[a-z_][a-z0-9_]*$', name))
            metrics.naming_convention_score = snake_case_count / len(identifiers)
