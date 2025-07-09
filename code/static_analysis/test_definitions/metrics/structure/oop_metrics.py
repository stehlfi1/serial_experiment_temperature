#!/usr/bin/env python3
"""
Object-Oriented Programming (OOP) Metrics Test

This script analyzes OOP characteristics in Python code including inheritance,
coupling, methods per class, and other object-oriented design metrics.
Part of the structure test group for temperature research.
"""

import ast
import sys
from pathlib import Path
from typing import Dict, Any, List, Set
import json


class OOPAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing OOP metrics."""
    
    def __init__(self):
        self.classes = {}  # {class_name: class_info}
        self.functions = []  # Standalone functions
        self.current_class = None
        self.inheritance_map = {}  # {class: [base_classes]}
        self.method_calls = set()  # Track method calls for coupling
        
    def visit_ClassDef(self, node):
        class_name = node.name
        base_classes = [base.id if isinstance(base, ast.Name) else str(base) 
                       for base in node.bases if hasattr(base, 'id')]
        
        # Count methods and attributes
        methods = []
        attributes = set()
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append({
                    'name': item.name,
                    'args_count': len(item.args.args),
                    'is_property': any(isinstance(d, ast.Name) and d.id == 'property' 
                                     for d in item.decorator_list),
                    'is_static': any(isinstance(d, ast.Name) and d.id == 'staticmethod'
                                   for d in item.decorator_list),
                    'is_class': any(isinstance(d, ast.Name) and d.id == 'classmethod'
                                  for d in item.decorator_list)
                })
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.add(target.id)
        
        self.classes[class_name] = {
            'name': class_name,
            'base_classes': base_classes,
            'methods': methods,
            'attributes': list(attributes),
            'method_count': len(methods),
            'attribute_count': len(attributes),
            'decorator_count': len(node.decorator_list)
        }
        
        self.inheritance_map[class_name] = base_classes
        
        # Visit methods with class context
        old_class = self.current_class
        self.current_class = class_name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node):
        if self.current_class is None:
            # Standalone function
            self.functions.append({
                'name': node.name,
                'args_count': len(node.args.args),
                'decorator_count': len(node.decorator_list)
            })
        
        self.generic_visit(node)
    
    def visit_Call(self, node):
        # Track method calls for coupling analysis
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                self.method_calls.add(f"{node.func.value.id}.{node.func.attr}")
            elif isinstance(node.func.value, ast.Call):
                self.method_calls.add(f"chained.{node.func.attr}")
        
        self.generic_visit(node)


def calculate_depth_of_inheritance(inheritance_map: Dict[str, List[str]]) -> Dict[str, int]:
    """Calculate Depth of Inheritance Tree (DIT) for each class."""
    dit = {}
    
    def get_depth(class_name: str, visited: Set[str] = None) -> int:
        if visited is None:
            visited = set()
        
        if class_name in visited:
            return 0  # Circular inheritance, treat as depth 0
        
        if class_name not in inheritance_map:
            return 0  # No inheritance info
        
        base_classes = inheritance_map[class_name]
        if not base_classes:
            return 0  # No base classes
        
        visited.add(class_name)
        max_depth = 0
        
        for base in base_classes:
            if base in inheritance_map:
                depth = 1 + get_depth(base, visited.copy())
                max_depth = max(max_depth, depth)
            else:
                max_depth = max(max_depth, 1)  # External base class
        
        return max_depth
    
    for class_name in inheritance_map:
        dit[class_name] = get_depth(class_name)
    
    return dit


def calculate_number_of_children(inheritance_map: Dict[str, List[str]]) -> Dict[str, int]:
    """Calculate Number of Children (NOC) for each class."""
    noc = {class_name: 0 for class_name in inheritance_map}
    
    for class_name, base_classes in inheritance_map.items():
        for base in base_classes:
            if base in noc:
                noc[base] += 1
    
    return noc


def analyze_oop_metrics(code_content: str) -> Dict[str, Any]:
    """
    Analyze OOP metrics in Python code.
    
    Args:
        code_content: String containing Python source code
        
    Returns:
        Dictionary containing OOP metrics
    """
    try:
        tree = ast.parse(code_content)
        analyzer = OOPAnalyzer()
        analyzer.visit(tree)
        
        # Calculate inheritance metrics
        dit = calculate_depth_of_inheritance(analyzer.inheritance_map)
        noc = calculate_number_of_children(analyzer.inheritance_map)
        
        # Calculate methods per class
        methods_per_class = [cls['method_count'] for cls in analyzer.classes.values()]
        
        # Calculate coupling (simplified: unique method calls)
        coupling_per_class = []
        for class_name in analyzer.classes:
            # Count method calls that could indicate coupling
            class_coupling = len([call for call in analyzer.method_calls 
                                if not call.startswith('self.')])
            coupling_per_class.append(class_coupling)
        
        # Calculate parameters per method
        parameters_per_method = []
        for cls in analyzer.classes.values():
            for method in cls['methods']:
                parameters_per_method.append(method['args_count'])
        
        # Add standalone function parameters
        for func in analyzer.functions:
            parameters_per_method.append(func['args_count'])
        
        return {
            "class_count": len(analyzer.classes),
            "method_count": sum(cls['method_count'] for cls in analyzer.classes.values()),
            "function_count": len(analyzer.functions),
            "methods_per_class": methods_per_class,
            "avg_methods_per_class": sum(methods_per_class) / len(methods_per_class) if methods_per_class else 0,
            "parameters_per_function": parameters_per_method,
            "avg_parameters_per_function": sum(parameters_per_method) / len(parameters_per_method) if parameters_per_method else 0,
            "depth_of_inheritance": list(dit.values()),
            "max_dit": max(dit.values()) if dit else 0,
            "avg_dit": sum(dit.values()) / len(dit) if dit else 0,
            "children_per_class": list(noc.values()),
            "max_noc": max(noc.values()) if noc else 0,
            "avg_noc": sum(noc.values()) / len(noc) if noc else 0,
            "coupling_per_class": coupling_per_class,
            "max_cbo": max(coupling_per_class) if coupling_per_class else 0,
            "avg_cbo": sum(coupling_per_class) / len(coupling_per_class) if coupling_per_class else 0,
            "inheritance_relationships": len([cls for cls in analyzer.inheritance_map.values() if cls]),
            "total_attributes": sum(cls['attribute_count'] for cls in analyzer.classes.values()),
            "classes_with_inheritance": len([cls for cls in analyzer.inheritance_map.values() if cls]),
            "error": None
        }
        
    except SyntaxError as e:
        return {
            "class_count": 0,
            "method_count": 0,
            "function_count": 0,
            "methods_per_class": [],
            "avg_methods_per_class": 0,
            "parameters_per_function": [],
            "avg_parameters_per_function": 0,
            "depth_of_inheritance": [],
            "max_dit": 0,
            "avg_dit": 0,
            "children_per_class": [],
            "max_noc": 0,
            "avg_noc": 0,
            "coupling_per_class": [],
            "max_cbo": 0,
            "avg_cbo": 0,
            "inheritance_relationships": 0,
            "total_attributes": 0,
            "classes_with_inheritance": 0,
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "class_count": 0,
            "method_count": 0,
            "function_count": 0,
            "methods_per_class": [],
            "avg_methods_per_class": 0,
            "parameters_per_function": [],
            "avg_parameters_per_function": 0,
            "depth_of_inheritance": [],
            "max_dit": 0,
            "avg_dit": 0,
            "children_per_class": [],
            "max_noc": 0,
            "avg_noc": 0,
            "coupling_per_class": [],
            "max_cbo": 0,
            "avg_cbo": 0,
            "inheritance_relationships": 0,
            "total_attributes": 0,
            "classes_with_inheritance": 0,
            "error": f"Analysis error: {str(e)}"
        }


def main():
    """Main entry point for OOP metrics analysis test."""
    if len(sys.argv) != 2:
        print("Usage: python oop_metrics.py <code_file_path>")
        sys.exit(1)
    
    code_file = Path(sys.argv[1])
    
    if not code_file.exists():
        result = {
            "file_exists": False,
            "error": f"File not found: {code_file}",
            "class_count": 0,
            "method_count": 0,
            "function_count": 0,
            "methods_per_class": [],
            "avg_methods_per_class": 0,
            "parameters_per_function": [],
            "avg_parameters_per_function": 0,
            "depth_of_inheritance": [],
            "max_dit": 0,
            "avg_dit": 0,
            "children_per_class": [],
            "max_noc": 0,
            "avg_noc": 0,
            "coupling_per_class": [],
            "max_cbo": 0,
            "avg_cbo": 0,
            "inheritance_relationships": 0,
            "total_attributes": 0,
            "classes_with_inheritance": 0
        }
    else:
        try:
            with open(code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            result = analyze_oop_metrics(code_content)
            result["file_exists"] = True
            
        except Exception as e:
            result = {
                "file_exists": True,
                "error": f"Failed to read file: {str(e)}",
                "class_count": 0,
                "method_count": 0,
                "function_count": 0,
                "methods_per_class": [],
                "avg_methods_per_class": 0,
                "parameters_per_function": [],
                "avg_parameters_per_function": 0,
                "depth_of_inheritance": [],
                "max_dit": 0,
                "avg_dit": 0,
                "children_per_class": [],
                "max_noc": 0,
                "avg_noc": 0,
                "coupling_per_class": [],
                "max_cbo": 0,
                "avg_cbo": 0,
                "inheritance_relationships": 0,
                "total_attributes": 0,
                "classes_with_inheritance": 0
            }
    
    # Output results as JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
