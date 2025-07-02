"""
Main similarity calculator orchestrator that combines all similarity metrics.
Provides a unified interface for comparing Python code files.
"""

import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import json

from codebleu_wrapper import CodeBLEUCalculator, CODEBLEU_AVAILABLE
from ast_metrics import ASTMetricsCalculator
from jaccard_calculator import JaccardCalculator


class SimilarityCalculator:
    """Main orchestrator for calculating all code similarity metrics."""
    
    def __init__(self, enable_codebleu: bool = True):
        """
        Initialize similarity calculator with optional components.
        
        Args:
            enable_codebleu: Whether to use CodeBLEU (requires external library)
        """
        self.enable_codebleu = enable_codebleu and CODEBLEU_AVAILABLE
        
        # Initialize component calculators
        if self.enable_codebleu:
            try:
                self.codebleu_calc = CodeBLEUCalculator()
            except ImportError:
                self.codebleu_calc = None
                self.enable_codebleu = False
        else:
            self.codebleu_calc = None
            
        self.ast_calc = ASTMetricsCalculator()
        self.jaccard_calc = JaccardCalculator()
    
    def calculate_all_similarities(self, file1: str, file2: str) -> Dict[str, Any]:
        """
        Calculate all similarity metrics between two Python files.
        
        Args:
            file1: Path to first Python file
            file2: Path to second Python file
            
        Returns:
            Dict with all similarity metrics and metadata
        """
        start_time = time.time()
        
        result = {
            "file1": str(file1),
            "file2": str(file2),
            "timestamp": time.time(),
            "metrics": {},
            "errors": [],
            "calculation_time": 0.0
        }
        
        # Calculate CodeBLEU metrics
        if self.enable_codebleu and self.codebleu_calc:
            try:
                codebleu_metrics = self.codebleu_calc.calculate_similarity(file1, file2)
                result["metrics"]["codebleu"] = codebleu_metrics
                
                if "error" in codebleu_metrics:
                    result["errors"].append(f"CodeBLEU: {codebleu_metrics['error']}")
                    
            except Exception as e:
                result["errors"].append(f"CodeBLEU calculation failed: {str(e)}")
                result["metrics"]["codebleu"] = {"error": str(e)}
        else:
            result["metrics"]["codebleu"] = {"error": "CodeBLEU not available"}
        
        # Calculate AST metrics
        try:
            ast_metrics = self.ast_calc.calculate_all_metrics(file1, file2)
            result["metrics"]["ast"] = ast_metrics
            
            if "error" in ast_metrics:
                result["errors"].append(f"AST: {ast_metrics['error']}")
                
        except Exception as e:
            result["errors"].append(f"AST calculation failed: {str(e)}")
            result["metrics"]["ast"] = {"error": str(e)}
        
        # Calculate Jaccard metrics
        try:
            jaccard_metrics = self.jaccard_calc.calculate_similarity(file1, file2)
            result["metrics"]["jaccard"] = jaccard_metrics
            
            if "error" in jaccard_metrics:
                result["errors"].append(f"Jaccard: {jaccard_metrics['error']}")
                
        except Exception as e:
            result["errors"].append(f"Jaccard calculation failed: {str(e)}")
            result["metrics"]["jaccard"] = {"error": str(e)}
        
        # Calculate composite scores
        result["metrics"]["composite"] = self._calculate_composite_scores(result["metrics"])
        
        result["calculation_time"] = time.time() - start_time
        return result
    
    def _calculate_composite_scores(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate composite similarity scores from individual metrics."""
        composite = {}
        
        try:
            # Overall similarity score (weighted average of available metrics)
            scores = []
            weights = []
            
            # CodeBLEU score (if available)
            if "codebleu" in metrics and "codebleu" in metrics["codebleu"]:
                if not isinstance(metrics["codebleu"]["codebleu"], str):  # Not an error
                    scores.append(metrics["codebleu"]["codebleu"])
                    weights.append(0.3)
            
            # AST similarity (inverse of normalized edit distance)
            if "ast" in metrics:
                ast_data = metrics["ast"]
                if "ast_edit_distance" in ast_data and not isinstance(ast_data["ast_edit_distance"], str):
                    # Normalize edit distance to similarity (simple approach)
                    if ast_data["ast_edit_distance"] != float('inf'):
                        ast_sim = 1.0 / (1.0 + ast_data["ast_edit_distance"] / 10.0)
                        scores.append(ast_sim)
                        weights.append(0.25)
                
                if "subtree_overlap_ratio" in ast_data and not isinstance(ast_data["subtree_overlap_ratio"], str):
                    scores.append(ast_data["subtree_overlap_ratio"])
                    weights.append(0.2)
            
            # Jaccard similarity (weighted average of token-based similarities)
            if "jaccard" in metrics:
                jaccard_data = metrics["jaccard"]
                jaccard_scores = []
                jaccard_weights = []
                
                for metric, weight in [("jaccard_identifiers", 0.4), 
                                     ("jaccard_ast_names", 0.3),
                                     ("jaccard_words", 0.2),
                                     ("jaccard_tokens", 0.1)]:
                    if metric in jaccard_data and not isinstance(jaccard_data[metric], str):
                        jaccard_scores.append(jaccard_data[metric])
                        jaccard_weights.append(weight)
                
                if jaccard_scores:
                    weighted_jaccard = sum(s * w for s, w in zip(jaccard_scores, jaccard_weights))
                    weighted_jaccard /= sum(jaccard_weights)
                    scores.append(weighted_jaccard)
                    weights.append(0.25)
            
            # Calculate weighted overall similarity
            if scores and weights:
                composite["overall_similarity"] = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
            else:
                composite["overall_similarity"] = 0.0
            
            # Structural similarity (focus on AST metrics)
            structural_scores = []
            if "ast" in metrics:
                ast_data = metrics["ast"]
                if "node_histogram_distance" in ast_data and not isinstance(ast_data["node_histogram_distance"], str):
                    structural_scores.append(1.0 - ast_data["node_histogram_distance"])
                if "subtree_overlap_ratio" in ast_data and not isinstance(ast_data["subtree_overlap_ratio"], str):
                    structural_scores.append(ast_data["subtree_overlap_ratio"])
            
            composite["structural_similarity"] = sum(structural_scores) / len(structural_scores) if structural_scores else 0.0
            
            # Semantic similarity (focus on CodeBLEU and identifier overlap)
            semantic_scores = []
            if "codebleu" in metrics and "codebleu" in metrics["codebleu"]:
                if not isinstance(metrics["codebleu"]["codebleu"], str):
                    semantic_scores.append(metrics["codebleu"]["codebleu"])
            
            if "jaccard" in metrics and "jaccard_identifiers" in metrics["jaccard"]:
                if not isinstance(metrics["jaccard"]["jaccard_identifiers"], str):
                    semantic_scores.append(metrics["jaccard"]["jaccard_identifiers"])
            
            composite["semantic_similarity"] = sum(semantic_scores) / len(semantic_scores) if semantic_scores else 0.0
            
        except Exception as e:
            composite["error"] = str(e)
            composite["overall_similarity"] = 0.0
            composite["structural_similarity"] = 0.0
            composite["semantic_similarity"] = 0.0
        
        return composite
    
    def compare_iteration_pairs(self, iteration_dir: str, model_name: str) -> Dict[str, Any]:
        """
        Compare all pairs of iterations for a specific model in a temperature directory.
        
        Args:
            iteration_dir: Path to directory containing iteration subdirectories
            model_name: Name of the model (e.g., 'claude', 'chatgpt')
            
        Returns:
            Dict with pairwise comparison results
        """
        iteration_path = Path(iteration_dir)
        if not iteration_path.exists():
            return {"error": f"Directory {iteration_dir} does not exist"}
        
        # Find all iteration directories
        iteration_dirs = []
        for subdir in iteration_path.iterdir():
            if subdir.is_dir() and subdir.name.startswith("iteration_"):
                model_file = subdir / f"{model_name}.py"
                if model_file.exists():
                    iteration_dirs.append((subdir.name, str(model_file)))
        
        if len(iteration_dirs) < 2:
            return {"error": f"Need at least 2 iterations for comparison, found {len(iteration_dirs)}"}
        
        # Sort by iteration number
        iteration_dirs.sort(key=lambda x: int(x[0].split('_')[1]))
        
        results = {
            "model": model_name,
            "temperature_dir": str(iteration_path),
            "iterations_found": len(iteration_dirs),
            "iteration_list": [name for name, _ in iteration_dirs],
            "pairwise_comparisons": {},
            "summary": {}
        }
        
        # Compare all pairs
        similarities = []
        comparison_count = 0
        
        for i in range(len(iteration_dirs)):
            for j in range(i + 1, len(iteration_dirs)):
                iter_name1, file1 = iteration_dirs[i]
                iter_name2, file2 = iteration_dirs[j]
                
                comparison_key = f"{iter_name1}_vs_{iter_name2}"
                comparison_result = self.calculate_all_similarities(file1, file2)
                
                results["pairwise_comparisons"][comparison_key] = comparison_result
                
                # Collect similarity scores for summary
                if "composite" in comparison_result["metrics"]:
                    overall_sim = comparison_result["metrics"]["composite"].get("overall_similarity", 0.0)
                    similarities.append(overall_sim)
                
                comparison_count += 1
        
        # Calculate summary statistics
        if similarities:
            results["summary"] = {
                "avg_similarity": sum(similarities) / len(similarities),
                "min_similarity": min(similarities),
                "max_similarity": max(similarities),
                "std_similarity": self._calculate_std(similarities),
                "total_comparisons": comparison_count
            }
        
        return results
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5


def calculate_file_similarity(file1: str, file2: str) -> Dict[str, Any]:
    """
    Convenience function to calculate all similarities between two files.
    
    Args:
        file1: Path to first Python file
        file2: Path to second Python file
        
    Returns:
        Dict with all similarity metrics
    """
    calculator = SimilarityCalculator()
    return calculator.calculate_all_similarities(file1, file2)


if __name__ == "__main__":
    # Simple test
    import tempfile
    import os
    
    # Create test files
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
    
    # Write to temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
        
        f1.write(test_code1)
        f2.write(test_code2)
        f1.flush()
        f2.flush()
        
        try:
            calculator = SimilarityCalculator()
            result = calculator.calculate_all_similarities(f1.name, f2.name)
            
            print("Similarity calculation result:")
            print(json.dumps(result, indent=2, default=str))
            
        finally:
            # Clean up
            try:
                os.unlink(f1.name)
                os.unlink(f2.name)
            except:
                pass