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

from .data_models import AdvancedMetrics


class ASTAnalyzer(ast.NodeVisitor):
    """AST visitor for comprehensive code analysis."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters for new analysis."""
        # Basic structure
        self.node_count = 0
        self.max_depth = 0
        self.current_depth = 0
        self.node_types = Counter()
        
        # Functions and classes
        self.functions = []
        self.classes = []
        self.methods = []
        self.current_class = None
        
        # Complexity tracking
        self.cyclomatic_complexity = 1  # Start with 1
        self.function_complexities = []
        self.nesting_depths = []
        self.max_nesting = 0
        self.current_nesting = 0
        
        # Halstead metrics
        self.operators = Counter()
        self.operands = Counter() 
        self.operator_instances = []
        self.operand_instances = []
        
        # Control flow
        self.loops = Counter()
        self.conditionals = Counter()
        self.comprehensions = Counter()
        
        # Variables and usage
        self.variables = set()
        self.global_vars = set()
        self.nonlocal_vars = set()
        self.imports = []
        self.from_imports = []
        
        # Code patterns
        self.lambda_count = 0
        self.generator_count = 0
        self.decorator_count = 0
        self.docstring_count = 0
        self.return_count = 0
        self.raise_count = 0
        self.assert_count = 0
        
        # Literals
        self.string_literals = 0
        self.number_literals = 0
        self.boolean_literals = 0
        
        # OOP metrics
        self.inheritance_depths = []
        self.children_per_class = []
        self.coupling_counts = []
        
        # ABC metrics
        self.assignments = 0
        self.branches = 0
        self.conditions = 0
    
    def visit(self, node):
        """Override visit to track depth and node counts."""
        self.node_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.node_types[type(node).__name__] += 1
        
        # Call the specific visitor
        result = super().visit(node)
        
        self.current_depth -= 1
        return result
    
    def visit_FunctionDef(self, node):
        """Analyze function definitions."""
        func_info = {
            'name': node.name,
            'args': len(node.args.args),
            'lineno': node.lineno,
            'decorators': len(node.decorator_list),
            'docstring': ast.get_docstring(node) is not None
        }
        
        if self.current_class:
            self.methods.append(func_info)
        else:
            self.functions.append(func_info)
        
        self.decorator_count += len(node.decorator_list)
        if func_info['docstring']:
            self.docstring_count += 1
        
        # Analyze function complexity
        old_cc = self.cyclomatic_complexity
        old_nesting = self.max_nesting
        self.cyclomatic_complexity = 1  # Reset for this function
        self.max_nesting = 0
        
        self.generic_visit(node)
        
        # Store function-specific metrics
        self.function_complexities.append(self.cyclomatic_complexity)
        self.nesting_depths.append(self.max_nesting)
        
        # Restore global counters
        self.cyclomatic_complexity = old_cc
        self.max_nesting = max(self.max_nesting, old_nesting)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async function definitions."""
        self.visit_FunctionDef(node)  # Same analysis as regular functions
    
    def visit_ClassDef(self, node):
        """Analyze class definitions."""
        old_class = self.current_class
        self.current_class = node.name
        
        class_info = {
            'name': node.name,
            'bases': len(node.bases),
            'methods': 0,
            'lineno': node.lineno,
            'decorators': len(node.decorator_list),
            'docstring': ast.get_docstring(node) is not None
        }
        
        self.classes.append(class_info)
        self.decorator_count += len(node.decorator_list)
        if class_info['docstring']:
            self.docstring_count += 1
        
        # Calculate inheritance depth (simplified)
        inheritance_depth = len(node.bases)
        self.inheritance_depths.append(inheritance_depth)
        
        self.generic_visit(node)
        
        # Count methods in this class
        methods_in_class = len([m for m in self.methods if 'class' not in m or m.get('class') == node.name])
        class_info['methods'] = methods_in_class
        
        self.current_class = old_class
    
    def visit_Import(self, node):
        """Track import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Track from-import statements."""
        for alias in node.names:
            import_name = f"{node.module}.{alias.name}" if node.module else alias.name
            self.from_imports.append(import_name)
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Track if statements for complexity."""
        self.cyclomatic_complexity += 1
        self.conditionals['if'] += 1
        self.conditions += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_While(self, node):
        """Track while loops."""
        self.cyclomatic_complexity += 1
        self.loops['while'] += 1
        self.conditions += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_For(self, node):
        """Track for loops."""
        self.cyclomatic_complexity += 1
        self.loops['for'] += 1
        self.branches += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_Try(self, node):
        """Track try-except blocks."""
        self.cyclomatic_complexity += len(node.handlers) + (1 if node.orelse else 0) + (1 if node.finalbody else 0)
        self.conditionals['try'] += 1
        self.branches += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_With(self, node):
        """Track with statements."""
        self.cyclomatic_complexity += 1
        self.branches += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_Lambda(self, node):
        """Track lambda expressions."""
        self.lambda_count += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        """Track generator expressions."""
        self.generator_count += 1
        self.comprehensions['generator'] += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        """Track list comprehensions."""
        self.comprehensions['list'] += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        """Track dictionary comprehensions."""
        self.comprehensions['dict'] += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        """Track set comprehensions."""
        self.comprehensions['set'] += 1
        self.generic_visit(node)
    
    def visit_Return(self, node):
        """Track return statements."""
        self.return_count += 1
        self.generic_visit(node)
    
    def visit_Raise(self, node):
        """Track raise statements."""
        self.raise_count += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        """Track assert statements."""
        self.assert_count += 1
        self.generic_visit(node)
    
    def visit_Global(self, node):
        """Track global variables."""
        for name in node.names:
            self.global_vars.add(name)
        self.generic_visit(node)
    
    def visit_Nonlocal(self, node):
        """Track nonlocal variables."""
        for name in node.names:
            self.nonlocal_vars.add(name)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Track variable names."""
        self.variables.add(node.id)
        self.operands[node.id] += 1
        self.operand_instances.append(node.id)
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Track assignments."""
        self.assignments += len(node.targets)
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        """Track augmented assignments."""
        self.assignments += 1
        self.generic_visit(node)
    
    def visit_Str(self, node):
        """Track string literals."""
        self.string_literals += 1
        self.generic_visit(node)
    
    def visit_Constant(self, node):
        """Track constants (Python 3.8+)."""
        if isinstance(node.value, str):
            self.string_literals += 1
        elif isinstance(node.value, (int, float)):
            self.number_literals += 1
        elif isinstance(node.value, bool):
            self.boolean_literals += 1
        self.generic_visit(node)
    
    def visit_Num(self, node):
        """Track numeric literals (Python < 3.8)."""
        self.number_literals += 1
        self.generic_visit(node)
    
    def visit_BinOp(self, node):
        """Track binary operators."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_UnaryOp(self, node):
        """Track unary operators."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """Track comparison operators."""
        for op in node.ops:
            op_name = type(op).__name__
            self.operators[op_name] += 1
            self.operator_instances.append(op_name)
        self.conditions += len(node.ops)
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Track boolean operators."""
        op_name = type(node.op).__name__
        self.operators[op_name] += 1
        self.operator_instances.append(op_name)
        self.generic_visit(node)
    
    def _enter_block(self):
        """Enter a nested block."""
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
    
    def _exit_block(self):
        """Exit a nested block."""
        self.current_nesting -= 1


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
            
            # Reset analyzer and visit AST
            self.analyzer.reset()
            self.analyzer.visit(tree)
            
            # Calculate all metrics
            metrics = AdvancedMetrics()
            
            # Complexity metrics
            self._calculate_complexity_metrics(metrics, source_code)
            
            # Halstead metrics
            self._calculate_halstead_metrics(metrics)
            
            # Size metrics
            self._calculate_size_metrics(metrics, source_code)
            
            # Structure metrics
            self._calculate_structure_metrics(metrics)
            
            # AST metrics
            self._calculate_ast_metrics(metrics)
            
            # Quality metrics
            self._calculate_quality_metrics(metrics, source_code)
            
            return metrics
            
        except Exception as e:
            print(f"Error analyzing {code_path}: {e}")
            return AdvancedMetrics()
    
    def _calculate_complexity_metrics(self, metrics: AdvancedMetrics, source_code: str):
        """Calculate complexity-related metrics."""
        # Cyclomatic complexity
        total_cc = sum(self.analyzer.function_complexities) if self.analyzer.function_complexities else 1
        metrics.cyclomatic_complexity = total_cc
        metrics.cyclomatic_complexity_per_function = self.analyzer.function_complexities.copy()
        
        # Nesting depth
        metrics.max_nesting_depth = self.analyzer.max_nesting
        if self.analyzer.nesting_depths:
            metrics.avg_nesting_depth = sum(self.analyzer.nesting_depths) / len(self.analyzer.nesting_depths)
            metrics.nesting_depth_per_function = self.analyzer.nesting_depths.copy()
        
        # Cognitive complexity (simplified approximation)
        cognitive_total = 0
        cognitive_per_func = []
        for i, cc in enumerate(self.analyzer.function_complexities):
            nesting = self.analyzer.nesting_depths[i] if i < len(self.analyzer.nesting_depths) else 0
            cognitive = cc + (nesting * 2)  # Simplified cognitive complexity
            cognitive_total += cognitive
            cognitive_per_func.append(cognitive)
        
        metrics.cognitive_complexity = cognitive_total
        metrics.cognitive_complexity_per_function = cognitive_per_func
        
        # ABC metrics
        metrics.abc_assignment_count = self.analyzer.assignments
        metrics.abc_branch_count = self.analyzer.branches
        metrics.abc_condition_count = self.analyzer.conditions
        if any([self.analyzer.assignments, self.analyzer.branches, self.analyzer.conditions]):
            metrics.abc_magnitude = math.sqrt(
                self.analyzer.assignments**2 + 
                self.analyzer.branches**2 + 
                self.analyzer.conditions**2
            )
    
    def _calculate_halstead_metrics(self, metrics: AdvancedMetrics):
        """Calculate comprehensive Halstead metrics."""
        if not self.analyzer.operators and not self.analyzer.operands:
            return
        
        # Basic counts
        n1 = len(self.analyzer.operators)  # Unique operators
        n2 = len(self.analyzer.operands)   # Unique operands
        N1 = sum(self.analyzer.operators.values())  # Total operators
        N2 = sum(self.analyzer.operands.values())   # Total operands
        
        metrics.halstead_operators = n1
        metrics.halstead_operands = n2
        metrics.halstead_operator_count = N1
        metrics.halstead_operand_count = N2
        
        # Derived metrics
        n = n1 + n2  # Vocabulary
        N = N1 + N2  # Length
        
        metrics.halstead_vocabulary = n
        metrics.halstead_length = N
        
        if n > 0 and N > 0:
            # Volume
            V = N * math.log2(n) if n > 1 else 0
            metrics.halstead_volume = V
            
            # Difficulty  
            if n2 > 0:
                D = (n1 / 2) * (N2 / n2)
                metrics.halstead_difficulty = D
                
                # Effort
                E = D * V
                metrics.halstead_effort = E
                
                # Time (in seconds)
                T = E / 18
                metrics.halstead_time = T
                
                # Bugs
                B = V / 3000
                metrics.halstead_bugs = B
    
    def _calculate_size_metrics(self, metrics: AdvancedMetrics, source_code: str):
        """Calculate size-related metrics."""
        lines = source_code.split('\n')
        
        # Line counts
        logical_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                logical_lines += 1
        
        metrics.logical_lines_of_code = logical_lines
        metrics.physical_lines_of_code = len(lines)
        metrics.comment_lines = comment_lines
        metrics.blank_lines = blank_lines
        
        if logical_lines > 0:
            metrics.code_to_comment_ratio = logical_lines / max(comment_lines, 1)
        
        # Function and class metrics
        metrics.function_count = len(self.analyzer.functions)
        metrics.class_count = len(self.analyzer.classes)
        metrics.method_count = len(self.analyzer.methods)
        
        if self.analyzer.classes:
            methods_per_class = [cls.get('methods', 0) for cls in self.analyzer.classes]
            metrics.methods_per_class = methods_per_class
        
        if self.analyzer.functions:
            params_per_func = [func.get('args', 0) for func in self.analyzer.functions]
            metrics.parameters_per_function = params_per_func
            metrics.avg_parameters_per_function = sum(params_per_func) / len(params_per_func)
        
        # WMC calculation
        if self.analyzer.classes and self.analyzer.function_complexities:
            wmc_per_class = []
            # This is simplified - ideally we'd track which methods belong to which class
            avg_cc = sum(self.analyzer.function_complexities) / len(self.analyzer.function_complexities)
            for cls in self.analyzer.classes:
                wmc = cls.get('methods', 0) * avg_cc
                wmc_per_class.append(wmc)
            metrics.wmc_per_class = wmc_per_class
            metrics.avg_wmc = sum(wmc_per_class) / len(wmc_per_class)
        
        # Import metrics
        metrics.import_count = len(self.analyzer.imports)
        metrics.from_import_count = len(self.analyzer.from_imports)
        all_imports = set(self.analyzer.imports + self.analyzer.from_imports)
        metrics.unique_imports = len(all_imports)
        
        # Classify imports (simplified)
        stdlib_count = 0
        third_party_count = 0
        for imp in all_imports:
            if imp.split('.')[0] in ['os', 'sys', 'math', 'json', 're', 'collections', 'pathlib', 'datetime']:
                stdlib_count += 1
            else:
                third_party_count += 1
        
        metrics.stdlib_imports = stdlib_count
        metrics.third_party_imports = third_party_count
    
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
    
    def _calculate_ast_metrics(self, metrics: AdvancedMetrics):
        """Calculate AST-specific metrics."""
        metrics.ast_node_count = self.analyzer.node_count
        metrics.ast_depth = self.analyzer.max_depth
        metrics.ast_node_types = dict(self.analyzer.node_types)
        metrics.ast_unique_node_types = len(self.analyzer.node_types)
    
    def _calculate_quality_metrics(self, metrics: AdvancedMetrics, source_code: str):
        """Calculate quality and maintainability metrics."""
        # Maintainability Index (simplified version)
        # MI = 171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * ln(Lines of Code)
        if (metrics.halstead_volume and metrics.halstead_volume > 0 and 
            metrics.cyclomatic_complexity and 
            metrics.logical_lines_of_code and metrics.logical_lines_of_code > 0):
            
            mi = (171 - 
                  5.2 * math.log(metrics.halstead_volume) - 
                  0.23 * metrics.cyclomatic_complexity - 
                  16.2 * math.log(metrics.logical_lines_of_code))
            
            metrics.maintainability_index = max(0, mi)  # MI can't be negative
            
            # Maintainability rank
            if mi > 85:
                metrics.maintainability_rank = "A"
            elif mi > 70:
                metrics.maintainability_rank = "B"
            elif mi > 50:
                metrics.maintainability_rank = "C"
            else:
                metrics.maintainability_rank = "D"
        
        # Function complexity distribution
        if self.analyzer.function_complexities:
            total_funcs = len(self.analyzer.function_complexities)
            simple_funcs = sum(1 for cc in self.analyzer.function_complexities if cc <= 5)
            complex_funcs = sum(1 for cc in self.analyzer.function_complexities if cc > 10)
            very_complex_funcs = sum(1 for cc in self.analyzer.function_complexities if cc > 20)
            
            metrics.simple_function_ratio = simple_funcs / total_funcs
            metrics.complex_function_ratio = complex_funcs / total_funcs
            metrics.very_complex_function_ratio = very_complex_funcs / total_funcs
        
        # Basic naming convention analysis
        identifiers = list(self.analyzer.variables) + [f['name'] for f in self.analyzer.functions] + [c['name'] for c in self.analyzer.classes]
        if identifiers:
            snake_case_count = sum(1 for name in identifiers if re.match(r'^[a-z_][a-z0-9_]*$', name))
            metrics.naming_convention_score = snake_case_count / len(identifiers)
