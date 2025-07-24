#!/usr/bin/env python3
"""
AST Analyzer for Temperature Research

Comprehensive AST visitor for analyzing code quality metrics across different
temperature settings in LLM-generated code.
"""

import ast
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import Counter, defaultdict


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
        
        # Cognitive complexity tracking (proper implementation)
        self.cognitive_complexity = 0
        self.function_cognitive_complexities = []
        self.current_cognitive = 0
        self.cognitive_nesting_level = 0
        
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
        
        # Additional control flow tracking
        self.yield_count = 0
        self.await_count = 0
        
        # Decorator type classification
        self.property_methods = 0
        self.static_methods = 0
        self.class_methods = 0
    
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
        
        # Classify decorator types
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == 'property':
                    self.property_methods += 1
                elif decorator.id == 'staticmethod':
                    self.static_methods += 1
                elif decorator.id == 'classmethod':
                    self.class_methods += 1
        
        # Analyze function complexity
        old_cc = self.cyclomatic_complexity
        old_nesting = self.max_nesting
        old_cognitive = self.current_cognitive
        old_cog_nesting = self.cognitive_nesting_level
        
        # Reset for this function
        self.cyclomatic_complexity = 1  # Reset for this function
        self.max_nesting = 0
        self.current_cognitive = 0
        self.cognitive_nesting_level = 0
        
        self.generic_visit(node)
        
        # Store function-specific metrics
        self.function_complexities.append(self.cyclomatic_complexity)
        self.nesting_depths.append(self.max_nesting)
        self.function_cognitive_complexities.append(self.current_cognitive)
        
        # Restore global counters
        self.cyclomatic_complexity = old_cc
        self.max_nesting = max(self.max_nesting, old_nesting)
        self.current_cognitive = old_cognitive
        self.cognitive_nesting_level = old_cog_nesting
    
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
        self._add_complexity(1)
        self.conditionals['if'] += 1
        self.conditions += 1
        
        # Count elif branches
        current = node
        while hasattr(current, 'orelse') and current.orelse:
            if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                self.conditionals['elif'] += 1
                current = current.orelse[0]
            else:
                break
        
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_While(self, node):
        """Track while loops."""
        self._add_complexity(1)
        self.loops['while'] += 1
        self.conditions += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_For(self, node):
        """Track for loops."""
        self._add_complexity(1)
        self.loops['for'] += 1
        self.branches += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_Try(self, node):
        """Track try-except blocks."""
        complexity_increase = len(node.handlers) + (1 if node.orelse else 0) + (1 if node.finalbody else 0)
        self._add_complexity(complexity_increase, cognitive_bonus=True)
        self.conditionals['try'] += 1
        self.branches += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_With(self, node):
        """Track with statements."""
        self._add_complexity(1)
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
    
    def visit_Yield(self, node):
        """Track yield statements."""
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_YieldFrom(self, node):
        """Track yield from statements."""
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_Await(self, node):
        """Track await expressions."""
        self.await_count += 1
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
        # For Halstead operands, skip built-in names and keywords (matching HalsteadAnalyzer)
        if node.id not in ['True', 'False', 'None']:
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
        # Each additional operand adds complexity (matching ComplexityAnalyzer)
        complexity_increase = len(node.values) - 1
        if complexity_increase > 0:
            self._add_complexity(complexity_increase)
        self.generic_visit(node)
    
    def _enter_block(self):
        """Enter a nested block."""
        self.current_nesting += 1
        self.cognitive_nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
    
    def _exit_block(self):
        """Exit a nested block."""
        self.current_nesting -= 1
        self.cognitive_nesting_level -= 1
    
    def _add_complexity(self, amount, cognitive_bonus=False):
        """Add complexity to both cyclomatic and cognitive measures."""
        self.cyclomatic_complexity += amount
        
        # Cognitive complexity includes nesting bonus
        cognitive_increase = amount
        if cognitive_bonus or self.cognitive_nesting_level > 0:
            cognitive_increase += self.cognitive_nesting_level
        
        self.current_cognitive += cognitive_increase
        self.cognitive_complexity += cognitive_increase