#!/usr/bin/env python3
"""
Size Analysis Test

Analyzes code size metrics (LLOC, functions, classes, parameters, etc.)
for temperature research on LLM-generated code.
"""

import ast
import sys
import json
from pathlib import Path
from collections import Counter


class SizeAnalyzer(ast.NodeVisitor):
    """Analyzes size metrics in Python code."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters."""
        self.functions = []
        self.classes = []
        self.methods = []
        self.imports = []
        self.from_imports = []
        
        # Track current context
        self.current_class = None
        self.class_method_counts = {}
        
        # Code patterns
        self.decorators = 0
        self.docstrings = 0
        self.lambdas = 0
        self.comprehensions = 0
        self.generators = 0
        
        # Variable tracking
        self.variables = set()
        self.global_vars = set()
        self.nonlocal_vars = set()
        
        # Statement counts
        self.statements = Counter()
    
    def visit_FunctionDef(self, node):
        """Analyze function definitions."""
        func_info = {
            "name": node.name,
            "args": len(node.args.args),
            "defaults": len(node.args.defaults),
            "kwonlyargs": len(node.args.kwonlyargs),
            "vararg": node.args.vararg is not None,
            "kwarg": node.args.kwarg is not None,
            "decorators": len(node.decorator_list),
            "docstring": ast.get_docstring(node) is not None,
            "lineno": node.lineno,
            "is_method": self.current_class is not None,
            "class": self.current_class
        }
        
        # Count total parameters including special ones
        total_params = (len(node.args.args) + 
                       len(node.args.kwonlyargs) + 
                       (1 if node.args.vararg else 0) + 
                       (1 if node.args.kwarg else 0))
        func_info["total_parameters"] = total_params
        
        if self.current_class:
            self.methods.append(func_info)
            if self.current_class not in self.class_method_counts:
                self.class_method_counts[self.current_class] = 0
            self.class_method_counts[self.current_class] += 1
        else:
            self.functions.append(func_info)
        
        self.decorators += len(node.decorator_list)
        if func_info["docstring"]:
            self.docstrings += 1
        
        self.statements["FunctionDef"] += 1
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async functions same as regular functions."""
        self.visit_FunctionDef(node)
        self.statements["AsyncFunctionDef"] += 1
    
    def visit_ClassDef(self, node):
        """Analyze class definitions."""
        old_class = self.current_class
        self.current_class = node.name
        
        class_info = {
            "name": node.name,
            "bases": len(node.bases),
            "keywords": len(node.keywords),
            "decorators": len(node.decorator_list),
            "docstring": ast.get_docstring(node) is not None,
            "lineno": node.lineno,
            "methods": 0  # Will be updated after visiting
        }
        
        self.classes.append(class_info)
        self.decorators += len(node.decorator_list)
        if class_info["docstring"]:
            self.docstrings += 1
        
        self.statements["ClassDef"] += 1
        self.generic_visit(node)
        
        # Update method count for this class
        class_info["methods"] = self.class_method_counts.get(node.name, 0)
        self.current_class = old_class
    
    def visit_Import(self, node):
        """Track import statements."""
        for alias in node.names:
            import_info = {
                "name": alias.name,
                "asname": alias.asname,
                "type": "import"
            }
            self.imports.append(import_info)
        
        self.statements["Import"] += 1
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Track from-import statements."""
        for alias in node.names:
            import_info = {
                "module": node.module,
                "name": alias.name,
                "asname": alias.asname,
                "level": node.level,
                "type": "from_import"
            }
            self.from_imports.append(import_info)
        
        self.statements["ImportFrom"] += 1
        self.generic_visit(node)
    
    def visit_Lambda(self, node):
        """Count lambda expressions."""
        self.lambdas += 1
        lambda_params = (len(node.args.args) + 
                        len(node.args.kwonlyargs) + 
                        (1 if node.args.vararg else 0) + 
                        (1 if node.args.kwarg else 0))
        self.statements["Lambda"] += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        """Count list comprehensions."""
        self.comprehensions += 1
        self.statements["ListComp"] += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        """Count dictionary comprehensions."""
        self.comprehensions += 1
        self.statements["DictComp"] += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        """Count set comprehensions."""
        self.comprehensions += 1
        self.statements["SetComp"] += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        """Count generator expressions."""
        self.generators += 1
        self.statements["GeneratorExp"] += 1
        self.generic_visit(node)
    
    def visit_Global(self, node):
        """Track global variable declarations."""
        for name in node.names:
            self.global_vars.add(name)
        self.statements["Global"] += 1
        self.generic_visit(node)
    
    def visit_Nonlocal(self, node):
        """Track nonlocal variable declarations."""
        for name in node.names:
            self.nonlocal_vars.add(name)
        self.statements["Nonlocal"] += 1
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Track variable names."""
        if node.id not in ['True', 'False', 'None']:
            self.variables.add(node.id)
        self.generic_visit(node)
    
    # Statement counting
    def visit_Assign(self, node):
        self.statements["Assign"] += 1
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        self.statements["AugAssign"] += 1
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node):
        self.statements["AnnAssign"] += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        self.statements["If"] += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.statements["While"] += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.statements["For"] += 1
        self.generic_visit(node)
    
    def visit_Try(self, node):
        self.statements["Try"] += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        self.statements["With"] += 1
        self.generic_visit(node)
    
    def visit_Return(self, node):
        self.statements["Return"] += 1
        self.generic_visit(node)
    
    def visit_Raise(self, node):
        self.statements["Raise"] += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        self.statements["Assert"] += 1
        self.generic_visit(node)
    
    def visit_Delete(self, node):
        self.statements["Delete"] += 1
        self.generic_visit(node)
    
    def visit_Pass(self, node):
        self.statements["Pass"] += 1
        self.generic_visit(node)
    
    def visit_Break(self, node):
        self.statements["Break"] += 1
        self.generic_visit(node)
    
    def visit_Continue(self, node):
        self.statements["Continue"] += 1
        self.generic_visit(node)


def count_lines(source_code: str) -> dict:
    """Count different types of lines in source code."""
    lines = source_code.split('\n')
    
    logical_lines = 0
    comment_lines = 0
    blank_lines = 0
    docstring_lines = 0
    
    in_docstring = False
    docstring_delimiter = None
    
    for line in lines:
        stripped = line.strip()
        
        # Check for docstring delimiters
        if '"""' in stripped or "'''" in stripped:
            if not in_docstring:
                in_docstring = True
                docstring_delimiter = '"""' if '"""' in stripped else "'''"
                # Check if docstring starts and ends on same line
                if stripped.count(docstring_delimiter) >= 2:
                    in_docstring = False
                    docstring_lines += 1
                    continue
                else:
                    docstring_lines += 1
                    continue
            else:
                if docstring_delimiter in stripped:
                    in_docstring = False
                    docstring_lines += 1
                    continue
        
        if in_docstring:
            docstring_lines += 1
        elif not stripped:
            blank_lines += 1
        elif stripped.startswith('#'):
            comment_lines += 1
        else:
            logical_lines += 1
    
    return {
        "total": len(lines),
        "logical": logical_lines,
        "comments": comment_lines,
        "blank": blank_lines,
        "docstring": docstring_lines,
        "code_to_comment_ratio": logical_lines / max(comment_lines, 1),
        "documentation_ratio": (comment_lines + docstring_lines) / max(logical_lines, 1)
    }


def analyze_imports(imports: list, from_imports: list) -> dict:
    """Analyze import patterns."""
    all_imports = imports + from_imports
    
    # Classify imports
    stdlib_modules = {
        'os', 'sys', 'math', 'json', 're', 'collections', 'itertools', 'functools',
        'pathlib', 'datetime', 'time', 'random', 'string', 'io', 'typing', 'copy',
        'pickle', 'sqlite3', 'urllib', 'http', 'email', 'html', 'xml', 'csv'
    }
    
    stdlib_count = 0
    third_party_count = 0
    local_count = 0
    
    for imp in all_imports:
        module_name = imp.get('module') or imp.get('name', '')
        top_level = module_name.split('.')[0]
        
        if top_level in stdlib_modules:
            stdlib_count += 1
        elif imp.get('type') == 'from_import' and imp.get('level', 0) > 0:
            local_count += 1  # Relative imports
        elif not module_name or module_name.startswith('.'):
            local_count += 1
        else:
            third_party_count += 1
    
    return {
        "total": len(all_imports),
        "import_statements": len(imports),
        "from_import_statements": len(from_imports),
        "stdlib": stdlib_count,
        "third_party": third_party_count,
        "local": local_count,
        "unique_modules": len(set(imp.get('module') or imp.get('name', '') for imp in all_imports))
    }


def analyze_size(file_path: str) -> dict:
    """Analyze size metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Analyze code
        analyzer = SizeAnalyzer()
        analyzer.visit(tree)
        
        # Count lines
        line_metrics = count_lines(source_code)
        
        # Analyze imports
        import_metrics = analyze_imports(analyzer.imports, analyzer.from_imports)
        
        # Calculate function metrics
        function_metrics = {
            "count": len(analyzer.functions),
            "method_count": len(analyzer.methods),
            "total_callable_count": len(analyzer.functions) + len(analyzer.methods),
            "parameters_per_function": [f["total_parameters"] for f in analyzer.functions],
            "parameters_per_method": [m["total_parameters"] for m in analyzer.methods],
            "avg_parameters_per_function": sum(f["total_parameters"] for f in analyzer.functions) / max(len(analyzer.functions), 1),
            "avg_parameters_per_method": sum(m["total_parameters"] for m in analyzer.methods) / max(len(analyzer.methods), 1),
            "max_parameters": max([f["total_parameters"] for f in analyzer.functions] + [m["total_parameters"] for m in analyzer.methods], default=0),
            "decorated_functions": sum(1 for f in analyzer.functions if f["decorators"] > 0),
            "decorated_methods": sum(1 for m in analyzer.methods if m["decorators"] > 0)
        }
        
        # Calculate class metrics
        class_metrics = {
            "count": len(analyzer.classes),
            "methods_per_class": [c["methods"] for c in analyzer.classes],
            "avg_methods_per_class": sum(c["methods"] for c in analyzer.classes) / max(len(analyzer.classes), 1),
            "max_methods_per_class": max([c["methods"] for c in analyzer.classes], default=0),
            "inheritance_usage": sum(1 for c in analyzer.classes if c["bases"] > 0),
            "max_inheritance_depth": max([c["bases"] for c in analyzer.classes], default=0),
            "decorated_classes": sum(1 for c in analyzer.classes if c["decorators"] > 0)
        }
        
        # Calculate WMC (Weighted Methods per Class) - simplified
        wmc_per_class = []
        for class_info in analyzer.classes:
            # Simple WMC: just count methods (ideally would weight by complexity)
            wmc = class_info["methods"]
            wmc_per_class.append(wmc)
        
        class_metrics["wmc_per_class"] = wmc_per_class
        class_metrics["avg_wmc"] = sum(wmc_per_class) / max(len(wmc_per_class), 1)
        
        return {
            "status": "success",
            "lines": line_metrics,
            "functions": function_metrics,
            "classes": class_metrics,
            "imports": import_metrics,
            "variables": {
                "total_unique": len(analyzer.variables),
                "global_declared": len(analyzer.global_vars),
                "nonlocal_declared": len(analyzer.nonlocal_vars)
            },
            "code_patterns": {
                "decorators": analyzer.decorators,
                "docstrings": analyzer.docstrings,
                "lambdas": analyzer.lambdas,
                "comprehensions": analyzer.comprehensions,
                "generators": analyzer.generators,
                "docstring_coverage": analyzer.docstrings / max(len(analyzer.functions) + len(analyzer.classes), 1)
            },
            "statements": dict(analyzer.statements),
            "statement_count": sum(analyzer.statements.values())
        }
        
    except SyntaxError as e:
        return {
            "status": "syntax_error",
            "error": f"Syntax error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    """Main function for command line usage."""
    if len(sys.argv) != 2:
        print("Usage: python size_analysis.py <model_name>")
        sys.exit(1)
    
    model_name = sys.argv[1]
    file_path = f"{model_name}.py"
    
    if not Path(file_path).exists():
        result = {
            "status": "file_not_found",
            "error": f"File {file_path} not found"
        }
    else:
        result = analyze_size(file_path)
    
    # Output results as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
