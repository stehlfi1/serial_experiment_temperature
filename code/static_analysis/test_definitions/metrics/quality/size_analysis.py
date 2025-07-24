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

# Import shared analyzer integration
try:
    from ...execution.ast_analyzer import ASTAnalyzer
except ImportError:
    # Fallback for CLI usage
    import sys
    import importlib.util
    from pathlib import Path
    
    ast_analyzer_path = Path(__file__).parent.parent.parent.parent / "execution" / "ast_analyzer.py"
    spec = importlib.util.spec_from_file_location("ast_analyzer", ast_analyzer_path)
    ast_analyzer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ast_analyzer_module)
    ASTAnalyzer = ast_analyzer_module.ASTAnalyzer


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


def _analyze_imports_from_strings(imports: list, from_imports: list) -> dict:
    """Analyze import patterns from string lists (shared analyzer format)."""
    # Classify imports
    stdlib_modules = {
        'os', 'sys', 'math', 'json', 're', 'collections', 'itertools', 'functools',
        'pathlib', 'datetime', 'time', 'random', 'string', 'io', 'typing', 'copy',
        'pickle', 'sqlite3', 'urllib', 'http', 'email', 'html', 'xml', 'csv'
    }
    
    stdlib_count = 0
    third_party_count = 0
    local_count = 0
    
    all_imports = imports + from_imports
    
    for imp in all_imports:
        # For shared analyzer, imports are simple strings
        module_name = imp
        top_level = module_name.split('.')[0]
        
        if top_level in stdlib_modules:
            stdlib_count += 1
        elif module_name.startswith('.'):
            local_count += 1  # Relative imports
        else:
            third_party_count += 1
    
    return {
        "total": len(all_imports),
        "import_statements": len(imports),
        "from_import_statements": len(from_imports),
        "stdlib": stdlib_count,
        "third_party": third_party_count,
        "local": local_count,
        "unique_modules": len(set(all_imports))
    }


def analyze_size_from_analyzer(analyzer, source_code: str) -> dict:
    """Analyze size metrics from a pre-populated ASTAnalyzer."""
    # Count lines
    line_metrics = count_lines(source_code)
    
    # Analyze imports (adapt to shared analyzer's string format)
    import_metrics = _analyze_imports_from_strings(analyzer.imports, analyzer.from_imports)
    
    # Calculate function metrics
    function_metrics = {
        "count": len(analyzer.functions),
        "method_count": len(analyzer.methods),
        "total_callable_count": len(analyzer.functions) + len(analyzer.methods),
        "parameters_per_function": [f.get("args", 0) for f in analyzer.functions],
        "parameters_per_method": [m.get("args", 0) for m in analyzer.methods],
        "avg_parameters_per_function": sum(f.get("args", 0) for f in analyzer.functions) / max(len(analyzer.functions), 1),
        "avg_parameters_per_method": sum(m.get("args", 0) for m in analyzer.methods) / max(len(analyzer.methods), 1),
        "max_parameters": max([f.get("args", 0) for f in analyzer.functions] + [m.get("args", 0) for m in analyzer.methods], default=0),
        "decorated_functions": sum(1 for f in analyzer.functions if f.get("decorators", 0) > 0),
        "decorated_methods": sum(1 for m in analyzer.methods if m.get("decorators", 0) > 0)
    }
    
    # Calculate class metrics
    class_metrics = {
        "count": len(analyzer.classes),
        "methods_per_class": [c.get("methods", 0) for c in analyzer.classes],
        "avg_methods_per_class": sum(c.get("methods", 0) for c in analyzer.classes) / max(len(analyzer.classes), 1),
        "max_methods_per_class": max([c.get("methods", 0) for c in analyzer.classes], default=0),
        "inheritance_usage": sum(1 for c in analyzer.classes if c.get("bases", 0) > 0),
        "max_inheritance_depth": max([c.get("bases", 0) for c in analyzer.classes], default=0),
        "decorated_classes": sum(1 for c in analyzer.classes if c.get("decorators", 0) > 0)
    }
    
    # Calculate WMC (Weighted Methods per Class) using complexity data
    wmc_per_class = []
    if analyzer.classes and analyzer.function_complexities:
        avg_cc = sum(analyzer.function_complexities) / len(analyzer.function_complexities)
        for class_info in analyzer.classes:
            # Simple WMC: methods * average complexity
            wmc = class_info.get("methods", 0) * avg_cc
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
            "decorators": analyzer.decorator_count,
            "docstrings": analyzer.docstring_count,
            "lambdas": analyzer.lambda_count,
            "comprehensions": sum(analyzer.comprehensions.values()),
            "generators": analyzer.generator_count,
            "docstring_coverage": analyzer.docstring_count / max(len(analyzer.functions) + len(analyzer.classes), 1)
        }
    }


def analyze_size(file_path: str) -> dict:
    """Analyze size metrics for a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Parse AST
        tree = ast.parse(source_code)
        
        # Use shared analyzer instead of duplicate SizeAnalyzer
        analyzer = ASTAnalyzer()
        analyzer.reset()
        analyzer.visit(tree)
        
        # Use the shared analyzer integration function
        return analyze_size_from_analyzer(analyzer, source_code)
        
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
