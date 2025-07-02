"""
AST-based similarity metrics for comparing Python code structures.
Implements TED, TSED, Node Histogram Distance, and Subtree Overlap Ratio.
"""

import ast
import hashlib
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set, Any, Optional
from pathlib import Path


class ASTNode:
    """Simplified AST node representation for tree edit distance calculations."""
    
    def __init__(self, node_type: str, value: str = "", children: List['ASTNode'] = None):
        self.node_type = node_type
        self.value = value
        self.children = children or []
        self.hash = None
    
    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        return (self.node_type == other.node_type and 
                self.value == other.value)
    
    def __hash__(self):
        if self.hash is None:
            self.hash = hash((self.node_type, self.value))
        return self.hash
    
    def __str__(self):
        return f"{self.node_type}({self.value})"


class ASTMetricsCalculator:
    """Calculate various AST-based similarity metrics between Python code files."""
    
    def __init__(self):
        self.node_type_weights = {
            'FunctionDef': 3,
            'ClassDef': 3,
            'If': 2,
            'For': 2,
            'While': 2,
            'Try': 2,
            'Import': 1,
            'ImportFrom': 1,
            'Assign': 1
        }
    
    def calculate_all_metrics(self, file1: str, file2: str) -> Dict[str, float]:
        """
        Calculate all AST metrics between two Python files.
        
        Args:
            file1: Path to first Python file
            file2: Path to second Python file
            
        Returns:
            Dict with all AST similarity metrics
        """
        try:
            with open(file1, 'r', encoding='utf-8') as f:
                code1 = f.read()
            with open(file2, 'r', encoding='utf-8') as f:
                code2 = f.read()
            
            return self.calculate_all_metrics_from_strings(code1, code2)
            
        except Exception as e:
            return {
                "ast_edit_distance": float('inf'),
                "tsed": float('inf'),
                "node_histogram_distance": 1.0,
                "subtree_overlap_ratio": 0.0,
                "error": str(e)
            }
    
    def calculate_all_metrics_from_strings(self, code1: str, code2: str) -> Dict[str, float]:
        """
        Calculate all AST metrics between two code strings.
        
        Args:
            code1: First Python code string
            code2: Second Python code string
            
        Returns:
            Dict with all AST similarity metrics
        """
        try:
            # Parse ASTs
            ast1 = ast.parse(code1)
            ast2 = ast.parse(code2)
            
            # Convert to simplified representation
            tree1 = self._ast_to_tree(ast1)
            tree2 = self._ast_to_tree(ast2)
            
            # Calculate all metrics
            ted = self._calculate_tree_edit_distance(tree1, tree2)
            tsed = self._calculate_tsed(tree1, tree2)
            node_hist_dist = self._calculate_node_histogram_distance(ast1, ast2)
            subtree_overlap = self._calculate_subtree_overlap_ratio(tree1, tree2)
            
            return {
                "ast_edit_distance": ted,
                "tsed": tsed,
                "node_histogram_distance": node_hist_dist,
                "subtree_overlap_ratio": subtree_overlap
            }
            
        except Exception as e:
            return {
                "ast_edit_distance": float('inf'),
                "tsed": float('inf'),
                "node_histogram_distance": 1.0,
                "subtree_overlap_ratio": 0.0,
                "error": str(e)
            }
    
    def _ast_to_tree(self, node) -> ASTNode:
        """Convert Python AST to simplified tree representation."""
        node_type = type(node).__name__
        
        # Extract meaningful values from specific node types
        value = ""
        if hasattr(node, 'name'):
            value = str(node.name)
        elif hasattr(node, 'id'):
            value = str(node.id)
        elif hasattr(node, 'attr'):
            value = str(node.attr)
        elif isinstance(node, ast.Constant):
            value = str(node.value)
        elif isinstance(node, (ast.Num, ast.Str)):  # For older Python versions
            value = str(node.n if hasattr(node, 'n') else node.s)
        
        # Recursively process children
        children = []
        for child in ast.iter_child_nodes(node):
            children.append(self._ast_to_tree(child))
        
        return ASTNode(node_type, value, children)
    
    def _calculate_tree_edit_distance(self, tree1: ASTNode, tree2: ASTNode) -> int:
        """
        Calculate Tree Edit Distance (TED) between two trees.
        Uses dynamic programming with memoization.
        """
        memo = {}
        
        def ted_recursive(t1: Optional[ASTNode], t2: Optional[ASTNode]) -> int:
            # Base cases
            if t1 is None and t2 is None:
                return 0
            if t1 is None:
                return 1 + sum(ted_recursive(None, child) for child in t2.children)
            if t2 is None:
                return 1 + sum(ted_recursive(child, None) for child in t1.children)
            
            # Create memo key
            key = (id(t1), id(t2))
            if key in memo:
                return memo[key]
            
            # If nodes are equal, recurse on children
            if t1 == t2:
                cost = 0
                # Align children optimally (simplified to sequential matching)
                max_children = max(len(t1.children), len(t2.children))
                for i in range(max_children):
                    c1 = t1.children[i] if i < len(t1.children) else None
                    c2 = t2.children[i] if i < len(t2.children) else None
                    cost += ted_recursive(c1, c2)
            else:
                # Try substitution, insertion, deletion
                # Substitution: replace t1 with t2, then align their children
                substitute_cost = 1  # Cost of substituting the node
                max_children = max(len(t1.children), len(t2.children))
                for i in range(max_children):
                    c1 = t1.children[i] if i < len(t1.children) else None
                    c2 = t2.children[i] if i < len(t2.children) else None
                    substitute_cost += ted_recursive(c1, c2)
                
                # Deletion: delete t1 and insert entire t2 subtree
                delete_cost = 1 + ted_recursive(None, t2)
                
                # Insertion: insert t2 and delete entire t1 subtree  
                insert_cost = 1 + ted_recursive(t1, None)
                
                cost = min(substitute_cost, delete_cost, insert_cost)
            
            memo[key] = cost
            return cost
        
        return ted_recursive(tree1, tree2)
    
    def _calculate_tsed(self, tree1: ASTNode, tree2: ASTNode) -> float:
        """
        Calculate Tree Similarity Edit Distance (TSED) - weighted version of TED.
        Uses node type weights to emphasize structural differences.
        """
        memo = {}
        
        def tsed_recursive(t1: Optional[ASTNode], t2: Optional[ASTNode]) -> float:
            if t1 is None and t2 is None:
                return 0.0
            if t1 is None:
                weight = self.node_type_weights.get(t2.node_type, 1)
                return weight + sum(tsed_recursive(None, child) for child in t2.children)
            if t2 is None:
                weight = self.node_type_weights.get(t1.node_type, 1)
                return weight + sum(tsed_recursive(child, None) for child in t1.children)
            
            key = (id(t1), id(t2))
            if key in memo:
                return memo[key]
            
            if t1 == t2:
                cost = 0.0
                max_children = max(len(t1.children), len(t2.children))
                for i in range(max_children):
                    c1 = t1.children[i] if i < len(t1.children) else None
                    c2 = t2.children[i] if i < len(t2.children) else None
                    cost += tsed_recursive(c1, c2)
            else:
                # Get weights for both node types
                weight = max(self.node_type_weights.get(t1.node_type, 1),
                           self.node_type_weights.get(t2.node_type, 1))
                
                # Substitution: replace t1 with t2, then align their children
                substitute_cost = weight  # Weighted cost of substituting the node
                max_children = max(len(t1.children), len(t2.children))
                for i in range(max_children):
                    c1 = t1.children[i] if i < len(t1.children) else None
                    c2 = t2.children[i] if i < len(t2.children) else None
                    substitute_cost += tsed_recursive(c1, c2)
                
                # Deletion: delete t1 and insert entire t2 subtree
                delete_cost = weight + tsed_recursive(None, t2)
                
                # Insertion: insert t2 and delete entire t1 subtree
                insert_cost = weight + tsed_recursive(t1, None)
                
                cost = min(substitute_cost, delete_cost, insert_cost)
            
            memo[key] = cost
            return cost
        
        return tsed_recursive(tree1, tree2)
    
    def _calculate_node_histogram_distance(self, ast1, ast2) -> float:
        """
        Calculate node histogram distance - compare frequency of node types.
        Returns normalized distance (0 = identical, 1 = completely different).
        """
        def get_node_histogram(tree) -> Counter:
            histogram = Counter()
            for node in ast.walk(tree):
                histogram[type(node).__name__] += 1
            return histogram
        
        hist1 = get_node_histogram(ast1)
        hist2 = get_node_histogram(ast2)
        
        # Get all unique node types
        all_types = set(hist1.keys()) | set(hist2.keys())
        
        if not all_types:
            return 0.0
        
        # Calculate Manhattan distance
        distance = 0
        total_nodes = 0
        for node_type in all_types:
            count1 = hist1.get(node_type, 0)
            count2 = hist2.get(node_type, 0)
            distance += abs(count1 - count2)
            total_nodes += max(count1, count2)
        
        # Normalize by total nodes
        return distance / total_nodes if total_nodes > 0 else 0.0
    
    def _calculate_subtree_overlap_ratio(self, tree1: ASTNode, tree2: ASTNode) -> float:
        """
        Calculate subtree overlap ratio - percentage of subtrees shared between trees.
        Returns ratio (0 = no overlap, 1 = identical).
        """
        def get_subtree_hashes(tree: ASTNode) -> Set[str]:
            """Get hashes of all subtrees rooted at each node."""
            hashes = set()
            
            def hash_subtree(node: ASTNode) -> str:
                # Create hash from node type, value, and children hashes
                child_hashes = []
                for child in node.children:
                    child_hash = hash_subtree(child)
                    child_hashes.append(child_hash)
                    hashes.add(child_hash)
                
                # Sort child hashes for consistent ordering
                child_hashes.sort()
                subtree_repr = f"{node.node_type}:{node.value}:[{','.join(child_hashes)}]"
                subtree_hash = hashlib.md5(subtree_repr.encode()).hexdigest()
                hashes.add(subtree_hash)
                return subtree_hash
            
            hash_subtree(tree)
            return hashes
        
        subtrees1 = get_subtree_hashes(tree1)
        subtrees2 = get_subtree_hashes(tree2)
        
        if not subtrees1 and not subtrees2:
            return 1.0
        
        if not subtrees1 or not subtrees2:
            return 0.0
        
        # Calculate Jaccard similarity of subtree sets
        intersection = len(subtrees1 & subtrees2)
        union = len(subtrees1 | subtrees2)
        
        return intersection / union if union > 0 else 0.0


def calculate_ast_metrics(file1: str, file2: str) -> Dict[str, float]:
    """
    Convenience function to calculate all AST metrics between two files.
    
    Args:
        file1: Path to first Python file
        file2: Path to second Python file
        
    Returns:
        Dict with all AST similarity metrics
    """
    calculator = ASTMetricsCalculator()
    return calculator.calculate_all_metrics(file1, file2)


if __name__ == "__main__":
    # Simple test
    test_code1 = """
def add(a, b):
    return a + b

result = add(1, 2)
print(result)
"""
    
    test_code2 = """
def add(x, y):
    return x + y

result = add(1, 2)
print(result)
"""
    
    test_code3 = """
def multiply(a, b):
    return a * b

result = multiply(2, 3)
print(result)
"""
    
    calculator = ASTMetricsCalculator()
    
    # Test similar code
    result1 = calculator.calculate_all_metrics_from_strings(test_code1, test_code2)
    print("Similar code metrics:", result1)
    
    # Test different code
    result2 = calculator.calculate_all_metrics_from_strings(test_code1, test_code3)
    print("Different code metrics:", result2)
    
    # Test identical code
    result3 = calculator.calculate_all_metrics_from_strings(test_code1, test_code1)
    print("Identical code metrics:", result3)