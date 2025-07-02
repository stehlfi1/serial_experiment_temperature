"""
Consistency analyzer for aggregating iteration comparison results.
Provides high-level consistency metrics for temperature research.
"""

import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import re

from similarity_calculator import SimilarityCalculator


class ConsistencyAnalyzer:
    """Analyze iteration consistency within temperature settings."""
    
    def __init__(self):
        self.similarity_calc = SimilarityCalculator()
    
    def analyze_temperature_consistency(self, base_dir: str, challenge: str, prompt: str, 
                                      model: str, temperature_folder: str) -> Dict[str, Any]:
        """
        Analyze consistency of iterations within a specific temperature setting.
        
        Args:
            base_dir: Base directory (e.g., "dry_run_output")
            challenge: Challenge name (e.g., "calculator")
            prompt: Prompt name (e.g., "5-role-zero_shot")
            model: Model name (e.g., "claude")
            temperature_folder: Temperature folder name (e.g., "temp_1.0")
            
        Returns:
            Dict with consistency analysis results
        """
        # Construct path to temperature directory
        temp_path = Path(base_dir) / "code" / challenge / prompt / temperature_folder
        
        if not temp_path.exists():
            return {
                "error": f"Temperature directory does not exist: {temp_path}",
                "path": str(temp_path)
            }
        
        # Get iteration comparison results
        comparison_results = self.similarity_calc.compare_iteration_pairs(str(temp_path), model)
        
        if "error" in comparison_results:
            return comparison_results
        
        # Extract consistency metrics
        consistency_analysis = {
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature_folder": temperature_folder,
            "temperature_params": self._parse_temperature_params(temperature_folder),
            "iterations_analyzed": comparison_results["iterations_found"],
            "total_comparisons": comparison_results["summary"].get("total_comparisons", 0),
            "consistency_scores": {},
            "detailed_metrics": {},
            "overall_assessment": {}
        }
        
        # Analyze pairwise comparisons
        self._analyze_pairwise_similarities(comparison_results, consistency_analysis)
        
        # Calculate consistency scores
        self._calculate_consistency_scores(comparison_results, consistency_analysis)
        
        # Generate overall assessment
        self._generate_overall_assessment(consistency_analysis)
        
        return consistency_analysis
    
    def analyze_multiple_temperatures(self, base_dir: str, challenge: str, prompt: str, 
                                    model: str) -> Dict[str, Any]:
        """
        Analyze consistency across multiple temperature settings for a model.
        
        Args:
            base_dir: Base directory
            challenge: Challenge name
            prompt: Prompt name
            model: Model name
            
        Returns:
            Dict with cross-temperature consistency analysis
        """
        prompt_path = Path(base_dir) / "code" / challenge / prompt
        
        if not prompt_path.exists():
            return {
                "error": f"Prompt directory does not exist: {prompt_path}",
                "path": str(prompt_path)
            }
        
        # Find all temperature folders
        temp_folders = []
        for subdir in prompt_path.iterdir():
            if subdir.is_dir() and subdir.name.startswith("temp_"):
                temp_folders.append(subdir.name)
        
        if not temp_folders:
            return {
                "error": f"No temperature folders found in {prompt_path}",
                "path": str(prompt_path)
            }
        
        temp_folders.sort()  # Sort for consistent ordering
        
        results = {
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature_folders": temp_folders,
            "temperature_analyses": {},
            "cross_temperature_comparison": {},
            "temperature_stability": {}
        }
        
        # Analyze each temperature setting
        for temp_folder in temp_folders:
            temp_analysis = self.analyze_temperature_consistency(
                base_dir, challenge, prompt, model, temp_folder
            )
            results["temperature_analyses"][temp_folder] = temp_analysis
        
        # Compare consistency across temperatures
        self._compare_temperature_consistency(results)
        
        return results
    
    def _parse_temperature_params(self, temperature_folder: str) -> Dict[str, Any]:
        """Parse temperature parameters from folder name."""
        params = {"temperature": None, "top_k": None, "top_p": None}
        
        # Parse temp_1.0_top_k_40_top_p_0.9 format
        parts = temperature_folder.split('_')
        for i, part in enumerate(parts):
            if part == "temp" and i+1 < len(parts):
                try:
                    params["temperature"] = float(parts[i+1])
                except ValueError:
                    pass
            elif part == "k" and i+1 < len(parts):  # top_k_40
                try:
                    params["top_k"] = int(parts[i+1])
                except ValueError:
                    pass
            elif part == "p" and i+1 < len(parts):  # top_p_0.9
                try:
                    params["top_p"] = float(parts[i+1])
                except ValueError:
                    pass
        
        return params
    
    def _analyze_pairwise_similarities(self, comparison_results: Dict[str, Any], 
                                     consistency_analysis: Dict[str, Any]):
        """Analyze pairwise similarity results."""
        pairwise_data = comparison_results.get("pairwise_comparisons", {})
        
        # Collect all similarity metrics
        all_similarities = {
            "overall": [],
            "structural": [],
            "semantic": [],
            "codebleu": [],
            "ast_edit_distance": [],
            "jaccard_identifiers": []
        }
        
        for comparison_key, comparison_data in pairwise_data.items():
            metrics = comparison_data.get("metrics", {})
            
            # Overall similarity
            if "composite" in metrics:
                composite = metrics["composite"]
                if "overall_similarity" in composite:
                    all_similarities["overall"].append(composite["overall_similarity"])
                if "structural_similarity" in composite:
                    all_similarities["structural"].append(composite["structural_similarity"])
                if "semantic_similarity" in composite:
                    all_similarities["semantic"].append(composite["semantic_similarity"])
            
            # CodeBLEU
            if "codebleu" in metrics and "codebleu" in metrics["codebleu"]:
                codebleu_score = metrics["codebleu"]["codebleu"]
                if isinstance(codebleu_score, (int, float)):
                    all_similarities["codebleu"].append(codebleu_score)
            
            # AST edit distance (convert to similarity)
            if "ast" in metrics and "ast_edit_distance" in metrics["ast"]:
                edit_dist = metrics["ast"]["ast_edit_distance"]
                if isinstance(edit_dist, (int, float)) and edit_dist != float('inf'):
                    similarity = 1.0 / (1.0 + edit_dist / 10.0)  # Normalize to similarity
                    all_similarities["ast_edit_distance"].append(similarity)
            
            # Jaccard identifiers
            if "jaccard" in metrics and "jaccard_identifiers" in metrics["jaccard"]:
                jaccard_score = metrics["jaccard"]["jaccard_identifiers"]
                if isinstance(jaccard_score, (int, float)):
                    all_similarities["jaccard_identifiers"].append(jaccard_score)
        
        # Calculate statistics for each metric
        detailed_metrics = {}
        for metric_name, values in all_similarities.items():
            if values:
                detailed_metrics[metric_name] = {
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "std": statistics.stdev(values) if len(values) > 1 else 0.0,
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                    "values": values
                }
            else:
                detailed_metrics[metric_name] = {
                    "mean": 0.0, "median": 0.0, "std": 0.0,
                    "min": 0.0, "max": 0.0, "count": 0, "values": []
                }
        
        consistency_analysis["detailed_metrics"] = detailed_metrics
    
    def _calculate_consistency_scores(self, comparison_results: Dict[str, Any], 
                                    consistency_analysis: Dict[str, Any]):
        """Calculate high-level consistency scores."""
        detailed = consistency_analysis["detailed_metrics"]
        
        consistency_scores = {}
        
        # Overall consistency (based on overall similarity mean and low std)
        if "overall" in detailed and detailed["overall"]["count"] > 0:
            mean_sim = detailed["overall"]["mean"]
            std_sim = detailed["overall"]["std"]
            # High consistency = high mean similarity and low standard deviation
            consistency_scores["overall_consistency"] = mean_sim * (1.0 - min(std_sim, 1.0))
        else:
            consistency_scores["overall_consistency"] = 0.0
        
        # Structural consistency
        if "structural" in detailed and detailed["structural"]["count"] > 0:
            mean_sim = detailed["structural"]["mean"]
            std_sim = detailed["structural"]["std"]
            consistency_scores["structural_consistency"] = mean_sim * (1.0 - min(std_sim, 1.0))
        else:
            consistency_scores["structural_consistency"] = 0.0
        
        # Semantic consistency
        if "semantic" in detailed and detailed["semantic"]["count"] > 0:
            mean_sim = detailed["semantic"]["mean"]
            std_sim = detailed["semantic"]["std"]
            consistency_scores["semantic_consistency"] = mean_sim * (1.0 - min(std_sim, 1.0))
        else:
            consistency_scores["semantic_consistency"] = 0.0
        
        # Consistency ranking
        scores = [
            consistency_scores.get("overall_consistency", 0.0),
            consistency_scores.get("structural_consistency", 0.0),
            consistency_scores.get("semantic_consistency", 0.0)
        ]
        consistency_scores["average_consistency"] = sum(scores) / len(scores)
        
        # Consistency grade
        avg_consistency = consistency_scores["average_consistency"]
        if avg_consistency >= 0.8:
            consistency_scores["consistency_grade"] = "A"
        elif avg_consistency >= 0.6:
            consistency_scores["consistency_grade"] = "B"
        elif avg_consistency >= 0.4:
            consistency_scores["consistency_grade"] = "C"
        elif avg_consistency >= 0.2:
            consistency_scores["consistency_grade"] = "D"
        else:
            consistency_scores["consistency_grade"] = "F"
        
        consistency_analysis["consistency_scores"] = consistency_scores
    
    def _generate_overall_assessment(self, consistency_analysis: Dict[str, Any]):
        """Generate human-readable overall assessment."""
        scores = consistency_analysis.get("consistency_scores", {})
        detailed = consistency_analysis.get("detailed_metrics", {})
        
        assessment = {
            "summary": "",
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        avg_consistency = scores.get("average_consistency", 0.0)
        grade = scores.get("consistency_grade", "F")
        iterations = consistency_analysis.get("iterations_analyzed", 0)
        
        # Generate summary
        temp_params = consistency_analysis.get("temperature_params", {})
        temp_str = f"temperature {temp_params.get('temperature', 'unknown')}"
        if temp_params.get("top_k"):
            temp_str += f", top_k {temp_params['top_k']}"
        if temp_params.get("top_p"):
            temp_str += f", top_p {temp_params['top_p']}"
        
        assessment["summary"] = (
            f"Model {consistency_analysis['model']} shows {grade}-grade consistency "
            f"at {temp_str} across {iterations} iterations "
            f"(consistency score: {avg_consistency:.3f})"
        )
        
        # Identify strengths and weaknesses
        if "overall" in detailed:
            overall_mean = detailed["overall"]["mean"]
            overall_std = detailed["overall"]["std"]
            
            if overall_mean > 0.7:
                assessment["strengths"].append(f"High average similarity ({overall_mean:.3f})")
            elif overall_mean < 0.3:
                assessment["weaknesses"].append(f"Low average similarity ({overall_mean:.3f})")
            
            if overall_std < 0.1:
                assessment["strengths"].append(f"Low variability ({overall_std:.3f})")
            elif overall_std > 0.3:
                assessment["weaknesses"].append(f"High variability ({overall_std:.3f})")
        
        # Recommendations
        if avg_consistency < 0.5:
            assessment["recommendations"].append("Consider using lower temperature for more consistent output")
        
        if iterations < 5:
            assessment["recommendations"].append("Increase number of iterations for more robust analysis")
        
        consistency_analysis["overall_assessment"] = assessment
    
    def _compare_temperature_consistency(self, results: Dict[str, Any]):
        """Compare consistency across different temperature settings."""
        temp_analyses = results.get("temperature_analyses", {})
        
        if len(temp_analyses) < 2:
            return
        
        # Extract consistency scores for each temperature
        temp_consistency = {}
        for temp_folder, analysis in temp_analyses.items():
            if "error" not in analysis:
                scores = analysis.get("consistency_scores", {})
                temp_consistency[temp_folder] = {
                    "overall": scores.get("overall_consistency", 0.0),
                    "structural": scores.get("structural_consistency", 0.0),
                    "semantic": scores.get("semantic_consistency", 0.0),
                    "average": scores.get("average_consistency", 0.0),
                    "grade": scores.get("consistency_grade", "F"),
                    "temperature": analysis.get("temperature_params", {}).get("temperature")
                }
        
        # Find best and worst temperatures
        if temp_consistency:
            best_temp = max(temp_consistency.items(), key=lambda x: x[1]["average"])
            worst_temp = min(temp_consistency.items(), key=lambda x: x[1]["average"])
            
            results["temperature_stability"] = {
                "best_temperature": {
                    "folder": best_temp[0],
                    "consistency": best_temp[1]["average"],
                    "grade": best_temp[1]["grade"]
                },
                "worst_temperature": {
                    "folder": worst_temp[0],
                    "consistency": worst_temp[1]["average"],
                    "grade": worst_temp[1]["grade"]
                },
                "consistency_by_temperature": temp_consistency,
                "temperature_effect": self._analyze_temperature_effect(temp_consistency)
            }
    
    def _analyze_temperature_effect(self, temp_consistency: Dict[str, Dict]) -> Dict[str, Any]:
        """Analyze how temperature affects consistency."""
        # Extract temperature values and consistency scores
        temp_values = []
        consistency_values = []
        
        for temp_folder, data in temp_consistency.items():
            temp = data.get("temperature")
            consistency = data.get("average", 0.0)
            if temp is not None:
                temp_values.append(temp)
                consistency_values.append(consistency)
        
        if len(temp_values) < 2:
            return {"error": "Insufficient data for temperature effect analysis"}
        
        # Calculate correlation
        try:
            correlation = self._calculate_correlation(temp_values, consistency_values)
            
            effect_analysis = {
                "correlation": correlation,
                "trend": "negative" if correlation < -0.3 else "positive" if correlation > 0.3 else "neutral",
                "interpretation": ""
            }
            
            if correlation < -0.5:
                effect_analysis["interpretation"] = "Higher temperature significantly reduces consistency"
            elif correlation < -0.3:
                effect_analysis["interpretation"] = "Higher temperature moderately reduces consistency"
            elif correlation > 0.5:
                effect_analysis["interpretation"] = "Higher temperature significantly increases consistency"
            elif correlation > 0.3:
                effect_analysis["interpretation"] = "Higher temperature moderately increases consistency"
            else:
                effect_analysis["interpretation"] = "Temperature has minimal effect on consistency"
            
            return effect_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze temperature effect: {str(e)}"}
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] * x[i] for i in range(n))
        sum_y2 = sum(y[i] * y[i] for i in range(n))
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0


if __name__ == "__main__":
    # Simple test
    analyzer = ConsistencyAnalyzer()
    
    # Test with a real directory (if it exists)
    test_result = analyzer.analyze_temperature_consistency(
        "dry_run_output", "calculator", "5-role-zero_shot", "claude", "temp_1.0"
    )
    
    print("Consistency analysis result:")
    print(json.dumps(test_result, indent=2, default=str))