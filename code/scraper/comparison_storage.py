"""
Comparison storage system for managing similarity analysis results.
Provides organized storage and retrieval of comparison data in /comparisons folder.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import uuid

from consistency_analyzer import ConsistencyAnalyzer


class ComparisonStorage:
    """Manage storage and retrieval of comparison analysis results."""
    
    def __init__(self, base_dir: str = "dry_run_output"):
        self.base_dir = Path(base_dir)
        self.similarity_dir = self.base_dir / "similarity_metrics"
        self.static_analysis_dir = self.base_dir / "static_analysis"
        
        # Create directories if they don't exist
        self._ensure_directories()
        
        self.consistency_analyzer = ConsistencyAnalyzer()
    
    def _ensure_directories(self):
        """Create comparison directories if they don't exist."""
        for directory in [self.similarity_dir, self.static_analysis_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def store_similarity_data(self, model: str, challenge: str, prompt: str, 
                            temperature_folder: str, pairwise_similarities: Dict[str, Dict[str, float]]) -> str:
        """
        Store raw similarity data for a specific model/challenge/prompt/temperature.
        
        Args:
            model: Model name (e.g., "claude")
            challenge: Challenge name (e.g., "calculator") 
            prompt: Prompt name (e.g., "5-role-zero_shot")
            temperature_folder: Temperature folder name (e.g., "temp_1.0")
            pairwise_similarities: Dict of iteration pairs to similarity metrics
            
        Returns:
            Path to stored file
        """
        # Create filename
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}.json"
        filepath = self.similarity_dir / filename
        
        # Clean data format - only raw metrics
        clean_data = {
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature_folder": temperature_folder,
            "generated_at": datetime.now().isoformat(),
            "pairwise_similarities": pairwise_similarities
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def store_multi_temperature_analysis(self, model: str, challenge: str, prompt: str, 
                                       analysis_result: Dict[str, Any]) -> str:
        """
        Store multi-temperature analysis result.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            analysis_result: Multi-temperature analysis result
            
        Returns:
            Path to stored file
        """
        filename = f"{model}_{challenge}_{prompt}_multi_temp.json"
        filepath = self.iteration_consistency_dir / filename
        
        storage_data = {
            "metadata": {
                "stored_at": datetime.now().isoformat(),
                "storage_id": str(uuid.uuid4()),
                "model": model,
                "challenge": challenge,
                "prompt": prompt,
                "analysis_type": "multi_temperature_consistency"
            },
            "analysis_result": analysis_result
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def store_pairwise_details(self, comparison_id: str, pairwise_data: Dict[str, Any]) -> str:
        """
        Store detailed pairwise comparison data.
        
        Args:
            comparison_id: Unique identifier for this comparison set
            pairwise_data: Detailed pairwise comparison results
            
        Returns:
            Path to stored file
        """
        filename = f"pairwise_{comparison_id}.json"
        filepath = self.pairwise_details_dir / filename
        
        storage_data = {
            "metadata": {
                "stored_at": datetime.now().isoformat(),
                "comparison_id": comparison_id,
                "analysis_type": "pairwise_details"
            },
            "pairwise_data": pairwise_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_consistency_analysis(self, model: str, challenge: str, prompt: str, 
                                temperature_folder: str) -> Optional[Dict[str, Any]]:
        """
        Load consistency analysis result.
        
        Args:
            model: Model name
            challenge: Challenge name  
            prompt: Prompt name
            temperature_folder: Temperature folder name
            
        Returns:
            Stored analysis result or None if not found
        """
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}.json"
        filepath = self.iteration_consistency_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("analysis_result")
        except Exception as e:
            print(f"Error loading consistency analysis: {e}")
            return None
    
    def load_multi_temperature_analysis(self, model: str, challenge: str, 
                                      prompt: str) -> Optional[Dict[str, Any]]:
        """Load multi-temperature analysis result."""
        filename = f"{model}_{challenge}_{prompt}_multi_temp.json"
        filepath = self.iteration_consistency_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("analysis_result")
        except Exception as e:
            print(f"Error loading multi-temperature analysis: {e}")
            return None
    
    def run_and_store_consistency_analysis(self, model: str, challenge: str, prompt: str, 
                                         temperature_folder: str, force_recompute: bool = False) -> str:
        """
        Run consistency analysis and store the result.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            temperature_folder: Temperature folder name
            force_recompute: Whether to recompute even if result exists
            
        Returns:
            Path to stored result
        """
        # Check if analysis already exists
        if not force_recompute:
            existing = self.load_consistency_analysis(model, challenge, prompt, temperature_folder)
            if existing:
                print(f"Using existing analysis for {model}/{challenge}/{prompt}/{temperature_folder}")
                filename = f"{model}_{challenge}_{prompt}_{temperature_folder}.json"
                return str(self.iteration_consistency_dir / filename)
        
        # Run analysis
        print(f"Running consistency analysis for {model}/{challenge}/{prompt}/{temperature_folder}")
        analysis_result = self.consistency_analyzer.analyze_temperature_consistency(
            str(self.base_dir), challenge, prompt, model, temperature_folder
        )
        
        # Store result
        return self.store_consistency_analysis(model, challenge, prompt, temperature_folder, analysis_result)
    
    def run_and_store_multi_temperature_analysis(self, model: str, challenge: str, prompt: str, 
                                               force_recompute: bool = False) -> str:
        """
        Run multi-temperature analysis and store the result.
        
        Args:
            model: Model name
            challenge: Challenge name
            prompt: Prompt name
            force_recompute: Whether to recompute even if result exists
            
        Returns:
            Path to stored result
        """
        # Check if analysis already exists
        if not force_recompute:
            existing = self.load_multi_temperature_analysis(model, challenge, prompt)
            if existing:
                print(f"Using existing multi-temp analysis for {model}/{challenge}/{prompt}")
                filename = f"{model}_{challenge}_{prompt}_multi_temp.json"
                return str(self.iteration_consistency_dir / filename)
        
        # Run analysis
        print(f"Running multi-temperature analysis for {model}/{challenge}/{prompt}")
        analysis_result = self.consistency_analyzer.analyze_multiple_temperatures(
            str(self.base_dir), challenge, prompt, model
        )
        
        # Store result
        return self.store_multi_temperature_analysis(model, challenge, prompt, analysis_result)
    
    def batch_analyze_all_available(self, force_recompute: bool = False) -> Dict[str, List[str]]:
        """
        Run consistency analysis for all available model/challenge/prompt/temperature combinations.
        
        Args:
            force_recompute: Whether to recompute existing analyses
            
        Returns:
            Dict with lists of created files
        """
        code_dir = self.base_dir / "code"
        if not code_dir.exists():
            return {"error": [f"Code directory does not exist: {code_dir}"]}
        
        results = {
            "consistency_analyses": [],
            "multi_temperature_analyses": [],
            "errors": []
        }
        
        # Find all available combinations
        for challenge_dir in code_dir.iterdir():
            if not challenge_dir.is_dir():
                continue
            
            challenge = challenge_dir.name
            
            for prompt_dir in challenge_dir.iterdir():
                if not prompt_dir.is_dir():
                    continue
                
                prompt = prompt_dir.name
                
                # Get all temperature folders
                temp_folders = []
                for temp_dir in prompt_dir.iterdir():
                    if temp_dir.is_dir() and temp_dir.name.startswith("temp_"):
                        temp_folders.append(temp_dir.name)
                
                if not temp_folders:
                    continue
                
                # Find available models
                models = set()
                for temp_folder in temp_folders:
                    temp_path = prompt_dir / temp_folder
                    for iter_dir in temp_path.iterdir():
                        if iter_dir.is_dir() and iter_dir.name.startswith("iteration_"):
                            for code_file in iter_dir.glob("*.py"):
                                if code_file.stem != "generation_params":
                                    models.add(code_file.stem)
                
                # Run analyses for each model
                for model in models:
                    try:
                        # Individual temperature analyses
                        for temp_folder in temp_folders:
                            try:
                                filepath = self.run_and_store_consistency_analysis(
                                    model, challenge, prompt, temp_folder, force_recompute
                                )
                                results["consistency_analyses"].append(filepath)
                            except Exception as e:
                                error_msg = f"Error analyzing {model}/{challenge}/{prompt}/{temp_folder}: {str(e)}"
                                results["errors"].append(error_msg)
                                print(error_msg)
                        
                        # Multi-temperature analysis
                        if len(temp_folders) > 1:
                            try:
                                filepath = self.run_and_store_multi_temperature_analysis(
                                    model, challenge, prompt, force_recompute
                                )
                                results["multi_temperature_analyses"].append(filepath)
                            except Exception as e:
                                error_msg = f"Error in multi-temp analysis {model}/{challenge}/{prompt}: {str(e)}"
                                results["errors"].append(error_msg)
                                print(error_msg)
                        
                    except Exception as e:
                        error_msg = f"Error processing model {model} for {challenge}/{prompt}: {str(e)}"
                        results["errors"].append(error_msg)
                        print(error_msg)
        
        return results
    
    def list_stored_analyses(self) -> Dict[str, List[str]]:
        """List all stored analysis files."""
        result = {
            "iteration_consistency": [],
            "pairwise_details": [],
            "visualization_data": []
        }
        
        # List iteration consistency files
        if self.iteration_consistency_dir.exists():
            for filepath in self.iteration_consistency_dir.glob("*.json"):
                result["iteration_consistency"].append(str(filepath))
        
        # List pairwise details files
        if self.pairwise_details_dir.exists():
            for filepath in self.pairwise_details_dir.glob("*.json"):
                result["pairwise_details"].append(str(filepath))
        
        # List visualization data files
        if self.visualization_data_dir.exists():
            for filepath in self.visualization_data_dir.glob("*.json"):
                result["visualization_data"].append(str(filepath))
        
        return result
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a summary report of all stored analyses."""
        stored_files = self.list_stored_analyses()
        
        summary = {
            "generated_at": datetime.now().isoformat(),
            "total_files": sum(len(files) for files in stored_files.values()),
            "file_counts": {category: len(files) for category, files in stored_files.items()},
            "analyses_summary": {},
            "models_analyzed": set(),
            "challenges_analyzed": set(),
            "prompts_analyzed": set()
        }
        
        # Analyze iteration consistency files
        consistency_summaries = []
        for filepath in stored_files["iteration_consistency"]:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data.get("metadata", {})
                analysis = data.get("analysis_result", {})
                
                if "error" not in analysis:
                    summary["models_analyzed"].add(metadata.get("model", "unknown"))
                    summary["challenges_analyzed"].add(metadata.get("challenge", "unknown"))
                    summary["prompts_analyzed"].add(metadata.get("prompt", "unknown"))
                    
                    consistency_scores = analysis.get("consistency_scores", {})
                    consistency_summaries.append({
                        "file": filepath,
                        "model": metadata.get("model"),
                        "challenge": metadata.get("challenge"),
                        "prompt": metadata.get("prompt"),
                        "temperature_folder": metadata.get("temperature_folder"),
                        "consistency_grade": consistency_scores.get("consistency_grade", "F"),
                        "average_consistency": consistency_scores.get("average_consistency", 0.0)
                    })
                    
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
        
        # Convert sets to lists for JSON serialization
        summary["models_analyzed"] = list(summary["models_analyzed"])
        summary["challenges_analyzed"] = list(summary["challenges_analyzed"])
        summary["prompts_analyzed"] = list(summary["prompts_analyzed"])
        
        summary["analyses_summary"]["consistency_analyses"] = consistency_summaries
        
        return summary


if __name__ == "__main__":
    # Simple test
    storage = ComparisonStorage("dry_run_output")
    
    # List existing analyses
    stored = storage.list_stored_analyses()
    print("Stored analyses:")
    for category, files in stored.items():
        print(f"  {category}: {len(files)} files")
    
    # Generate summary report
    summary = storage.generate_summary_report()
    print("\nSummary report:")
    print(json.dumps(summary, indent=2, default=str))