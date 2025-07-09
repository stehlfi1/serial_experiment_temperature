"""
Clean visualization data exporter with explicit metric labeling.
Creates chart-ready data with clear metric identification.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from .similarity_storage import SimilarityStorage


class CleanVizExporter:
    """Export clean visualization data with explicit metric labels."""
    
    def __init__(self, base_dir: str = "dry_run_output"):
        self.storage = SimilarityStorage(base_dir)
        self.viz_dir = self.storage.base_dir / "similarity_metrics" / "visualization"
        self.viz_dir.mkdir(parents=True, exist_ok=True)
    
    def export_similarity_matrix(self, model: str, challenge: str, prompt: str, 
                                temperature_folder: str, metric: str = "codebleu") -> str:
        """
        Export similarity matrix for a specific metric.
        
        Args:
            model: Model name
            challenge: Challenge name  
            prompt: Prompt name
            temperature_folder: Temperature folder name
            metric: Which similarity metric to use for the matrix
            
        Returns:
            Path to exported file
        """
        # Load similarity data
        data = self.storage.load_similarity_data(model, challenge, prompt, temperature_folder)
        
        if not data or "similarities" not in data:
            return self._export_error("similarity_matrix", 
                                    f"{model}_{challenge}_{prompt}_{temperature_folder}_{metric}",
                                    f"No similarity data found")
        
        similarities = data["similarities"]
        
        # Extract iterations from similarity keys
        iterations = set()
        for pair_key in similarities.keys():
            # Parse "iter_1_vs_2" format
            parts = pair_key.split('_')
            if len(parts) >= 4 and parts[0] == "iter" and parts[2] == "vs":
                iterations.add(int(parts[1]))
                iterations.add(int(parts[3]))
        
        if len(iterations) < 2:
            return self._export_error("similarity_matrix", 
                                    f"{model}_{challenge}_{prompt}_{temperature_folder}_{metric}",
                                    f"Insufficient iterations for matrix")
        
        iterations = sorted(iterations)
        iteration_labels = [f"iter_{i}" for i in iterations]
        
        # Build similarity matrix
        matrix = []
        for i, iter1 in enumerate(iterations):
            row = []
            for j, iter2 in enumerate(iterations):
                if i == j:
                    row.append(1.0)  # Perfect similarity with self
                else:
                    # Find similarity value
                    similarity_val = 0.0
                    pair_key1 = f"iter_{min(iter1, iter2)}_vs_{max(iter1, iter2)}"
                    
                    if pair_key1 in similarities and metric in similarities[pair_key1]:
                        similarity_val = similarities[pair_key1][metric]
                    
                    row.append(similarity_val)
            matrix.append(row)
        
        # Create chart data with explicit metric labeling
        chart_data = {
            "chart_type": "similarity_matrix",
            "title": f"{metric.upper()} Similarity Matrix - {model} ({temperature_folder})",
            "metric": metric,
            "metric_description": self._get_metric_description(metric),
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature": data.get("temperature"),
            "labels": iteration_labels,
            "matrix": matrix,
            "generated_at": datetime.now().isoformat()
        }
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}_{metric}_matrix.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_metric_comparison(self, model: str, challenge: str, prompt: str, 
                               temperature_folder: str) -> str:
        """
        Export comparison of all metrics for line/bar charts.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name  
            temperature_folder: Temperature folder name
            
        Returns:
            Path to exported file
        """
        # Load similarity data
        data = self.storage.load_similarity_data(model, challenge, prompt, temperature_folder)
        
        if not data or "similarities" not in data:
            return self._export_error("metric_comparison",
                                    f"{model}_{challenge}_{prompt}_{temperature_folder}",
                                    "No similarity data found")
        
        similarities = data["similarities"]
        
        # Collect all available metrics
        all_metrics = set()
        for pair_data in similarities.values():
            all_metrics.update(pair_data.keys())
        
        if not all_metrics:
            return self._export_error("metric_comparison",
                                    f"{model}_{challenge}_{prompt}_{temperature_folder}",
                                    "No metrics found")
        
        # Calculate average value for each metric across all pairs
        metric_averages = {}
        metric_values = {}
        
        for metric in all_metrics:
            values = []
            for pair_data in similarities.values():
                if metric in pair_data:
                    values.append(pair_data[metric])
            
            if values:
                metric_averages[metric] = sum(values) / len(values)
                metric_values[metric] = values
        
        # Create chart data
        chart_data = {
            "chart_type": "metric_comparison",
            "title": f"Similarity Metrics Comparison - {model} ({temperature_folder})",
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature": data.get("temperature"),
            "metrics": {},
            "generated_at": datetime.now().isoformat()
        }
        
        # Add each metric with description and values
        for metric, avg_value in metric_averages.items():
            chart_data["metrics"][metric] = {
                "name": metric,
                "description": self._get_metric_description(metric),
                "average_value": round(avg_value, 4),
                "all_values": [round(v, 4) for v in metric_values[metric]],
                "value_count": len(metric_values[metric])
            }
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}_metrics.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_temperature_comparison(self, model: str, challenge: str, prompt: str, 
                                    metric: str = "codebleu") -> str:
        """
        Export temperature comparison for a specific metric.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            metric: Which metric to compare across temperatures
            
        Returns:
            Path to exported file
        """
        # Find all temperature folders for this model/challenge/prompt
        temp_data = {}
        
        similarity_files = self.storage.similarity_dir.glob(f"{model}_{challenge}_{prompt}_temp_*.json")
        
        for filepath in similarity_files:
            data = self.storage.load_similarity_data(model, challenge, prompt, 
                                                   filepath.stem.split('_')[-1])  # Extract temp_X.X
            
            if not data or "similarities" not in data:
                continue
            
            temperature = data.get("temperature")
            if temperature is None:
                continue
            
            # Calculate average metric value
            metric_values = []
            for pair_data in data["similarities"].values():
                if metric in pair_data:
                    metric_values.append(pair_data[metric])
            
            if metric_values:
                temp_data[temperature] = {
                    "temperature": temperature,
                    "average_value": sum(metric_values) / len(metric_values),
                    "all_values": metric_values,
                    "temperature_folder": data.get("temperature_folder", f"temp_{temperature}")
                }
        
        if len(temp_data) < 2:
            return self._export_error("temperature_comparison",
                                    f"{model}_{challenge}_{prompt}_{metric}",
                                    f"Need at least 2 temperatures, found {len(temp_data)}")
        
        # Sort by temperature
        sorted_temps = sorted(temp_data.keys())
        
        # Create chart data
        chart_data = {
            "chart_type": "temperature_comparison", 
            "title": f"{metric.upper()} vs Temperature - {model}",
            "metric": metric,
            "metric_description": self._get_metric_description(metric),
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "x_axis": {"label": "Temperature", "values": sorted_temps},
            "y_axis": {"label": f"{metric.upper()} Similarity", "metric": metric},
            "data_points": [],
            "generated_at": datetime.now().isoformat()
        }
        
        # Add data points
        for temp in sorted_temps:
            temp_info = temp_data[temp]
            chart_data["data_points"].append({
                "x": temp,
                "y": round(temp_info["average_value"], 4),
                "temperature_folder": temp_info["temperature_folder"],
                "sample_count": len(temp_info["all_values"])
            })
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_{metric}_vs_temperature.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chart_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_all_visualizations(self) -> Dict[str, List[str]]:
        """Export all available visualizations with clear metric labeling."""
        results = {
            "similarity_matrices": [],
            "metric_comparisons": [],
            "temperature_comparisons": [],
            "errors": []
        }
        
        # Get all available data files
        available_files = self.storage.list_available_data()
        
        # Extract unique combinations
        combinations = set()
        for filepath in available_files:
            filename = Path(filepath).name
            # Parse "model_challenge_prompt_temperature.json"
            parts = filename[:-5].split('_')  # Remove .json
            if len(parts) >= 4:
                # Reconstruct parts (handle multi-word names)
                for i in range(1, len(parts) - 2):
                    if parts[i].startswith("temp"):
                        model = "_".join(parts[:i-2])
                        challenge = parts[i-2]
                        prompt = parts[i-1] 
                        temp_folder = "_".join(parts[i:])
                        combinations.add((model, challenge, prompt, temp_folder))
                        break
        
        # Export visualizations for each combination
        key_metrics = ["codebleu", "jaccard_identifiers", "ast_edit_distance", "subtree_overlap_ratio"]
        
        for model, challenge, prompt, temp_folder in combinations:
            try:
                # Metric comparison for this combination
                filepath = self.export_metric_comparison(model, challenge, prompt, temp_folder)
                results["metric_comparisons"].append(filepath)
                
                # Similarity matrices for key metrics
                for metric in key_metrics:
                    try:
                        filepath = self.export_similarity_matrix(model, challenge, prompt, temp_folder, metric)
                        results["similarity_matrices"].append(filepath)
                    except Exception as e:
                        results["errors"].append(f"Matrix export error for {metric}: {str(e)}")
                
            except Exception as e:
                results["errors"].append(f"Export error for {model}/{challenge}/{prompt}/{temp_folder}: {str(e)}")
        
        # Export temperature comparisons for each model/challenge/prompt
        model_combinations = set()
        for model, challenge, prompt, _ in combinations:
            model_combinations.add((model, challenge, prompt))
        
        for model, challenge, prompt in model_combinations:
            for metric in key_metrics:
                try:
                    filepath = self.export_temperature_comparison(model, challenge, prompt, metric)
                    results["temperature_comparisons"].append(filepath)
                except Exception as e:
                    results["errors"].append(f"Temperature comparison error for {metric}: {str(e)}")
        
        return results
    
    def _get_metric_description(self, metric: str) -> str:
        """Get human-readable description of metric."""
        descriptions = {
            "codebleu": "Code-aware BLEU similarity (0-1, higher=more similar)",
            "codebleu_syntax": "CodeBLEU syntax component (0-1, higher=more similar)",
            "codebleu_dataflow": "CodeBLEU dataflow component (0-1, higher=more similar)",
            "ast_edit_distance": "AST edit distance (lower=more similar)",
            "tsed": "Tree Similarity Edit Distance (lower=more similar)",
            "node_histogram_distance": "AST node type distribution distance (0-1, lower=more similar)",
            "subtree_overlap_ratio": "Percentage of shared AST subtrees (0-1, higher=more similar)",
            "jaccard_identifiers": "Jaccard similarity of identifier names (0-1, higher=more similar)",
            "jaccard_tokens": "Jaccard similarity of all tokens (0-1, higher=more similar)",
            "jaccard_ast_names": "Jaccard similarity of AST names (0-1, higher=more similar)"
        }
        return descriptions.get(metric, f"Similarity metric: {metric}")
    
    def _export_error(self, chart_type: str, filename_base: str, error_message: str) -> str:
        """Export error data."""
        error_data = {
            "chart_type": chart_type,
            "error": error_message,
            "generated_at": datetime.now().isoformat()
        }
        
        filename = f"{filename_base}_error.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)


if __name__ == "__main__":
    # Test the clean visualization exporter
    exporter = CleanVizExporter("dry_run_output")
    
    # Export all visualizations
    results = exporter.export_all_visualizations()
    
    print("Clean visualization export results:")
    for viz_type, files in results.items():
        print(f"  {viz_type}: {len(files)} files")
        for file in files[:2]:  # Show first 2 files
            print(f"    {Path(file).name}")
        if len(files) > 2:
            print(f"    ... and {len(files) - 2} more")