"""
Visualization data exporter for generating chart-ready formats.
Exports comparison data in formats optimized for visualization dashboards.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import statistics

from comparison_storage import ComparisonStorage


class VisualizationExporter:
    """Export comparison data in chart-ready formats."""
    
    def __init__(self, base_dir: str = "dry_run_output"):
        self.storage = ComparisonStorage(base_dir)
        self.viz_dir = self.storage.visualization_data_dir
    
    def export_temperature_trends(self, model: str, challenge: str, prompt: str) -> str:
        """
        Export temperature trend data for line charts.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            
        Returns:
            Path to exported visualization data file
        """
        # Load multi-temperature analysis
        analysis = self.storage.load_multi_temperature_analysis(model, challenge, prompt)
        
        if not analysis or "error" in analysis:
            return self._export_error_data("temperature_trends", 
                                          f"{model}_{challenge}_{prompt}_trends", 
                                          "Multi-temperature analysis not available")
        
        # Extract trend data
        temp_analyses = analysis.get("temperature_analyses", {})
        stability_data = analysis.get("temperature_stability", {})
        
        trend_data = {
            "chart_type": "line",
            "title": f"Temperature Consistency Trends - {model} ({challenge}/{prompt})",
            "x_axis": {"label": "Temperature", "type": "continuous"},
            "y_axis": {"label": "Consistency Score", "type": "continuous", "range": [0, 1]},
            "series": [],
            "metadata": {
                "model": model,
                "challenge": challenge,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # Extract data points for each consistency metric
        consistency_series = {
            "overall": {"name": "Overall Consistency", "data": [], "color": "#1f77b4"},
            "structural": {"name": "Structural Consistency", "data": [], "color": "#ff7f0e"},
            "semantic": {"name": "Semantic Consistency", "data": [], "color": "#2ca02c"}
        }
        
        # Collect data points
        for temp_folder, temp_analysis in temp_analyses.items():
            if "error" in temp_analysis:
                continue
            
            temp_params = temp_analysis.get("temperature_params", {})
            temperature = temp_params.get("temperature")
            
            if temperature is None:
                continue
            
            scores = temp_analysis.get("consistency_scores", {})
            
            # Add data points
            for metric, series in consistency_series.items():
                score_key = f"{metric}_consistency"
                if score_key in scores:
                    series["data"].append({"x": temperature, "y": scores[score_key]})
        
        # Sort data points by temperature and add to series
        for series in consistency_series.values():
            series["data"].sort(key=lambda p: p["x"])
            if series["data"]:  # Only add series with data
                trend_data["series"].append(series)
        
        # Add temperature effect analysis if available
        if "temperature_effect" in stability_data:
            effect = stability_data["temperature_effect"]
            trend_data["annotations"] = [{
                "type": "text",
                "text": f"Temperature Effect: {effect.get('interpretation', 'Unknown')}",
                "position": "bottom-right"
            }]
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_temperature_trends.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(trend_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_model_comparison_heatmap(self, challenge: str, prompt: str) -> str:
        """
        Export model comparison data as heatmap format.
        
        Args:
            challenge: Challenge name
            prompt: Prompt name
            
        Returns:
            Path to exported heatmap data file
        """
        # Get all models that have analyses for this challenge/prompt
        models = ["claude", "chatgpt", "gemini"]  # Common models
        
        heatmap_data = {
            "chart_type": "heatmap",
            "title": f"Model Consistency Comparison - {challenge}/{prompt}",
            "x_axis": {"label": "Temperature", "categories": []},
            "y_axis": {"label": "Model", "categories": models},
            "data": [],
            "color_scale": {
                "min": 0, "max": 1,
                "colors": ["#d73027", "#fee08b", "#d9ef8b", "#4575b4"]
            },
            "metadata": {
                "challenge": challenge,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # Collect temperature folders across all models
        all_temp_folders = set()
        model_data = {}
        
        for model in models:
            analysis = self.storage.load_multi_temperature_analysis(model, challenge, prompt)
            if analysis and "error" not in analysis:
                temp_analyses = analysis.get("temperature_analyses", {})
                model_data[model] = temp_analyses
                all_temp_folders.update(temp_analyses.keys())
        
        # Sort temperature folders
        temp_folders = sorted(all_temp_folders)
        
        # Extract temperature values for sorting
        def parse_temp(temp_folder):
            try:
                parts = temp_folder.split('_')
                for i, part in enumerate(parts):
                    if part == "temp" and i+1 < len(parts):
                        return float(parts[i+1])
            except:
                pass
            return 0.0
        
        temp_folders.sort(key=parse_temp)
        heatmap_data["x_axis"]["categories"] = temp_folders
        
        # Build heatmap data matrix
        for y, model in enumerate(models):
            for x, temp_folder in enumerate(temp_folders):
                value = 0.0  # Default value
                
                if model in model_data and temp_folder in model_data[model]:
                    temp_analysis = model_data[model][temp_folder]
                    if "error" not in temp_analysis:
                        scores = temp_analysis.get("consistency_scores", {})
                        value = scores.get("average_consistency", 0.0)
                
                heatmap_data["data"].append({
                    "x": x, "y": y, "value": value,
                    "model": model, "temperature": temp_folder
                })
        
        # Export to file
        filename = f"{challenge}_{prompt}_model_comparison_heatmap.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(heatmap_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_consistency_distribution(self, model: str, challenge: str, prompt: str) -> str:
        """
        Export consistency score distribution for histogram/box plot.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            
        Returns:
            Path to exported distribution data file
        """
        analysis = self.storage.load_multi_temperature_analysis(model, challenge, prompt)
        
        if not analysis or "error" in analysis:
            return self._export_error_data("consistency_distribution",
                                          f"{model}_{challenge}_{prompt}_distribution",
                                          "Multi-temperature analysis not available")
        
        temp_analyses = analysis.get("temperature_analyses", {})
        
        distribution_data = {
            "chart_type": "box_plot",
            "title": f"Consistency Score Distribution - {model} ({challenge}/{prompt})",
            "data": {},
            "summary_stats": {},
            "metadata": {
                "model": model,
                "challenge": challenge,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # Collect consistency scores by temperature
        for temp_folder, temp_analysis in temp_analyses.items():
            if "error" in temp_analysis:
                continue
            
            temp_params = temp_analysis.get("temperature_params", {})
            temperature = temp_params.get("temperature", "unknown")
            
            # Get detailed metrics for distribution
            detailed_metrics = temp_analysis.get("detailed_metrics", {})
            
            temp_data = {
                "temperature": temperature,
                "temperature_folder": temp_folder,
                "overall_similarities": [],
                "structural_similarities": [],
                "semantic_similarities": []
            }
            
            # Extract similarity values for distribution
            if "overall" in detailed_metrics:
                temp_data["overall_similarities"] = detailed_metrics["overall"].get("values", [])
            
            if "structural" in detailed_metrics:
                temp_data["structural_similarities"] = detailed_metrics["structural"].get("values", [])
            
            if "semantic" in detailed_metrics:
                temp_data["semantic_similarities"] = detailed_metrics["semantic"].get("values", [])
            
            # Calculate summary statistics
            temp_data["summary"] = {}
            for metric_type in ["overall_similarities", "structural_similarities", "semantic_similarities"]:
                values = temp_data[metric_type]
                if values:
                    temp_data["summary"][metric_type] = {
                        "mean": statistics.mean(values),
                        "median": statistics.median(values),
                        "std": statistics.stdev(values) if len(values) > 1 else 0.0,
                        "min": min(values),
                        "max": max(values),
                        "q25": statistics.quantiles(values, n=4)[0] if len(values) >= 4 else min(values),
                        "q75": statistics.quantiles(values, n=4)[2] if len(values) >= 4 else max(values)
                    }
            
            distribution_data["data"][temp_folder] = temp_data
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_consistency_distribution.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(distribution_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_similarity_matrix(self, model: str, challenge: str, prompt: str, 
                                temperature_folder: str) -> str:
        """
        Export pairwise similarity matrix for a specific temperature.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            temperature_folder: Temperature folder name
            
        Returns:
            Path to exported similarity matrix data file
        """
        analysis = self.storage.load_consistency_analysis(model, challenge, prompt, temperature_folder)
        
        if not analysis or "error" in analysis:
            return self._export_error_data("similarity_matrix",
                                          f"{model}_{challenge}_{prompt}_{temperature_folder}_matrix",
                                          "Consistency analysis not available")
        
        # Extract iteration list and pairwise comparisons
        iterations = analysis.get("iterations_analyzed", 0)
        
        # Create iteration names
        iteration_names = [f"iter_{i+1}" for i in range(iterations)]
        
        matrix_data = {
            "chart_type": "similarity_matrix",
            "title": f"Iteration Similarity Matrix - {model} ({challenge}/{prompt}/{temperature_folder})",
            "labels": iteration_names,
            "matrix": [],
            "metadata": {
                "model": model,
                "challenge": challenge,
                "prompt": prompt,
                "temperature_folder": temperature_folder,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        # Initialize matrix with 1.0 on diagonal
        matrix = []
        for i in range(iterations):
            row = []
            for j in range(iterations):
                if i == j:
                    row.append(1.0)  # Perfect similarity with self
                else:
                    row.append(0.0)  # Will be filled from pairwise data
            matrix.append(row)
        
        # Fill matrix from detailed metrics
        detailed_metrics = analysis.get("detailed_metrics", {})
        if "overall" in detailed_metrics and "values" in detailed_metrics["overall"]:
            similarities = detailed_metrics["overall"]["values"]
            
            # Map similarities to matrix positions (simplified approach)
            sim_index = 0
            for i in range(iterations):
                for j in range(i+1, iterations):
                    if sim_index < len(similarities):
                        similarity = similarities[sim_index]
                        matrix[i][j] = similarity
                        matrix[j][i] = similarity  # Symmetric matrix
                        sim_index += 1
        
        matrix_data["matrix"] = matrix
        
        # Export to file
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}_similarity_matrix.json"
        filepath = self.viz_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(matrix_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def export_all_visualizations(self) -> Dict[str, List[str]]:
        """
        Export all available visualization data.
        
        Returns:
            Dict with lists of exported files by visualization type
        """
        results = {
            "temperature_trends": [],
            "model_comparison_heatmaps": [],
            "consistency_distributions": [],
            "similarity_matrices": [],
            "errors": []
        }
        
        # Get all available analyses
        stored_analyses = self.storage.list_stored_analyses()
        
        # Track unique model/challenge/prompt combinations
        combinations = set()
        temp_combinations = set()
        
        for filepath in stored_analyses["iteration_consistency"]:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data.get("metadata", {})
                if metadata.get("analysis_type") == "multi_temperature_consistency":
                    combo = (metadata.get("model"), metadata.get("challenge"), metadata.get("prompt"))
                    combinations.add(combo)
                elif metadata.get("analysis_type") == "iteration_consistency":
                    combo = (metadata.get("model"), metadata.get("challenge"), 
                           metadata.get("prompt"), metadata.get("temperature_folder"))
                    temp_combinations.add(combo)
                    
            except Exception as e:
                results["errors"].append(f"Error reading {filepath}: {str(e)}")
        
        # Export temperature trends and model comparisons
        challenge_prompt_pairs = set()
        for model, challenge, prompt in combinations:
            if model and challenge and prompt:
                try:
                    # Temperature trends
                    filepath = self.export_temperature_trends(model, challenge, prompt)
                    results["temperature_trends"].append(filepath)
                    
                    # Consistency distributions
                    filepath = self.export_consistency_distribution(model, challenge, prompt)
                    results["consistency_distributions"].append(filepath)
                    
                    challenge_prompt_pairs.add((challenge, prompt))
                    
                except Exception as e:
                    results["errors"].append(f"Error exporting for {model}/{challenge}/{prompt}: {str(e)}")
        
        # Export model comparison heatmaps
        for challenge, prompt in challenge_prompt_pairs:
            try:
                filepath = self.export_model_comparison_heatmap(challenge, prompt)
                results["model_comparison_heatmaps"].append(filepath)
            except Exception as e:
                results["errors"].append(f"Error exporting heatmap for {challenge}/{prompt}: {str(e)}")
        
        # Export similarity matrices
        for model, challenge, prompt, temp_folder in temp_combinations:
            if model and challenge and prompt and temp_folder:
                try:
                    filepath = self.export_similarity_matrix(model, challenge, prompt, temp_folder)
                    results["similarity_matrices"].append(filepath)
                except Exception as e:
                    results["errors"].append(f"Error exporting matrix for {model}/{challenge}/{prompt}/{temp_folder}: {str(e)}")
        
        return results
    
    def _export_error_data(self, chart_type: str, filename_base: str, error_message: str) -> str:
        """Export error data for visualization."""
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
    # Simple test
    exporter = VisualizationExporter("dry_run_output")
    
    # Export all available visualizations
    results = exporter.export_all_visualizations()
    
    print("Visualization export results:")
    for viz_type, files in results.items():
        print(f"  {viz_type}: {len(files)} files")
        for file in files[:3]:  # Show first 3 files
            print(f"    {file}")
        if len(files) > 3:
            print(f"    ... and {len(files) - 3} more")