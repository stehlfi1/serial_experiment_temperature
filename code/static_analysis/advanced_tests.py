#!/usr/bin/env python3
"""
Advanced Test Runner for Temperature Research

This module implements advanced code quality and similarity tests
for analyzing the impact of temperature on LLM-generated code.
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter
import math

from .results.data_models import AdvancedMetrics, TEST_GROUPS, TestGroup


class AdvancedTestRunner:
    """Advanced test runner for temperature research metrics."""
    
    def __init__(self):
        self.test_groups = TEST_GROUPS
    
    def run_quality_tests(self, code_path: Path) -> Dict[str, Any]:
        """Run all quality tests on a code file."""
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            analyzer = CodeQualityAnalyzer(code, tree)
            
            return {
                "cyclomatic_complexity": analyzer.cyclomatic_complexity(),
                "halstead_metrics": analyzer.halstead_metrics(),
                "cognitive_complexity": analyzer.cognitive_complexity(),
                "maintainability_index": analyzer.maintainability_index(),
                "nesting_depth": analyzer.nesting_depth()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def run_structure_tests(self, code_path: Path) -> Dict[str, Any]:
        """Run all structural analysis tests on a code file."""
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            analyzer = StructureAnalyzer(tree)
            
            return {
                "ast_node_count": analyzer.node_count(),
                "ast_depth": analyzer.tree_depth(),
                "function_count": analyzer.function_count(),
                "class_count": analyzer.class_count(),
                "import_count": analyzer.import_count(),
                "variable_count": analyzer.variable_count()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def run_all_tests(self, code_path: Path, test_groups: List[str] = None) -> AdvancedMetrics:
        """Run all specified test groups and return advanced metrics."""
        metrics = AdvancedMetrics()
        
        if not test_groups:
            test_groups = ["quality", "structure"]
        
        try:
            if "quality" in test_groups:
                quality_results = self.run_quality_tests(code_path)
                if "error" not in quality_results:
                    metrics.cyclomatic_complexity = quality_results.get("cyclomatic_complexity")
                    halstead = quality_results.get("halstead_metrics", {})
                    metrics.halstead_volume = halstead.get("volume")
                    metrics.halstead_difficulty = halstead.get("difficulty")
                    metrics.halstead_effort = halstead.get("effort")
                    metrics.cognitive_complexity = quality_results.get("cognitive_complexity")
                    metrics.maintainability_index = quality_results.get("maintainability_index")
                    metrics.nesting_depth = quality_results.get("nesting_depth")
            
            if "structure" in test_groups:
                structure_results = self.run_structure_tests(code_path)
                if "error" not in structure_results:
                    metrics.ast_node_count = structure_results.get("ast_node_count")
                    metrics.ast_depth = structure_results.get("ast_depth")
                    metrics.function_count = structure_results.get("function_count")
                    metrics.class_count = structure_results.get("class_count")
                    metrics.import_count = structure_results.get("import_count")
                    metrics.variable_count = structure_results.get("variable_count")
        
        except Exception as e:
            # Log error but return partial metrics
            pass
        
        return metrics


class CodeQualityAnalyzer:
    """Analyzer for code quality metrics."""
    
    def __init__(self, code: str, tree: ast.AST):
        self.code = code
        self.tree = tree
        self.lines = code.split('\n')
    
    def cyclomatic_complexity(self) -> float:
        """Calculate cyclomatic complexity (decision points + 1)."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(self.tree):
            # Decision points
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.ListComp):
                complexity += sum(1 for _ in node.generators)
        
        return float(complexity)
    
    def halstead_metrics(self) -> Dict[str, float]:
        """Calculate Halstead metrics."""
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp):
                operators.add(type(node.op).__name__)
                operator_count += 1
            elif isinstance(node, ast.UnaryOp):
                operators.add(type(node.op).__name__)
                operator_count += 1
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    operators.add(type(op).__name__)
                    operator_count += 1
            elif isinstance(node, ast.Name):
                operands.add(node.id)
                operand_count += 1
            elif isinstance(node, ast.Constant):
                operands.add(str(node.value))
                operand_count += 1
        
        n1 = len(operators)  # Number of distinct operators
        n2 = len(operands)   # Number of distinct operands
        N1 = operator_count  # Total number of operators
        N2 = operand_count   # Total number of operands
        
        if n1 == 0 or n2 == 0:
            return {"volume": 0.0, "difficulty": 0.0, "effort": 0.0}
        
        vocabulary = n1 + n2
        length = N1 + N2
        
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        effort = difficulty * volume
        
        return {
            "volume": volume,
            "difficulty": difficulty,
            "effort": effort
        }
    
    def cognitive_complexity(self) -> float:
        """Calculate cognitive complexity (simplified version)."""
        complexity = 0
        nesting = 0
        
        def visit_node(node, depth=0):
            nonlocal complexity, nesting
            
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1 + depth
            elif isinstance(node, ast.Try):
                complexity += 1 + depth
            
            # Increase nesting for certain structures
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                depth += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(self.tree)
        return float(complexity)
    
    def maintainability_index(self) -> float:
        """Calculate maintainability index (simplified version)."""
        loc = len([line for line in self.lines if line.strip()])
        cc = self.cyclomatic_complexity()
        halstead = self.halstead_metrics()
        
        if loc == 0:
            return 0.0
        
        # Simplified MI calculation
        mi = max(0, (171 - 5.2 * math.log(halstead["volume"]) - 0.23 * cc - 16.2 * math.log(loc)) * 100 / 171)
        return mi
    
    def nesting_depth(self) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0
        
        def visit_node(node, depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try, ast.With)):
                depth += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(self.tree)
        return max_depth


class StructureAnalyzer:
    """Analyzer for code structure metrics."""
    
    def __init__(self, tree: ast.AST):
        self.tree = tree
    
    def node_count(self) -> int:
        """Count total AST nodes."""
        return len(list(ast.walk(self.tree)))
    
    def tree_depth(self) -> int:
        """Calculate maximum AST depth."""
        def get_depth(node):
            if not hasattr(node, '__dict__'):
                return 1
            
            children = list(ast.iter_child_nodes(node))
            if not children:
                return 1
            
            return 1 + max(get_depth(child) for child in children)
        
        return get_depth(self.tree)
    
    def function_count(self) -> int:
        """Count function definitions."""
        return len([n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))])
    
    def class_count(self) -> int:
        """Count class definitions."""
        return len([n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)])
    
    def import_count(self) -> int:
        """Count import statements."""
        return len([n for n in ast.walk(self.tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
    
    def variable_count(self) -> int:
        """Count unique variable names."""
        variables = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variables.add(node.id)
        return len(variables)


class SimilarityAnalyzer:
    """Analyzer for code similarity metrics (to be implemented)."""
    
    @staticmethod
    def bleu_score(code1: str, code2: str) -> float:
        """Calculate BLEU score between two code snippets."""
        # TODO: Implement BLEU score calculation
        return 0.0
    
    @staticmethod
    def ast_edit_distance(code1: str, code2: str) -> float:
        """Calculate AST edit distance between two code snippets."""
        # TODO: Implement AST edit distance calculation
        return 0.0
    
    @staticmethod
    def jaccard_similarity(code1: str, code2: str) -> float:
        """Calculate Jaccard similarity between two code snippets."""
        # TODO: Implement Jaccard similarity calculation
        return 0.0
