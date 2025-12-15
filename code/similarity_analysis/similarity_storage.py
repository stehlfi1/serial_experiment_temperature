"""
Clean similarity storage system for raw comparison metrics.
Stores only essential data without statistical bloat.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from .similarity_calculator import SimilarityCalculator


class SimilarityStorage:
    """Store and manage raw similarity metrics data."""
    
    def __init__(self, base_dir: str = "dry_run_output"):
        self.base_dir = Path(base_dir)
        # New hierarchical structure
        self.similarity_dir = self.base_dir / "similarity_analysis" / "pairwise_within_temperature"
        self.similarity_dir.mkdir(parents=True, exist_ok=True)

        self.similarity_calc = SimilarityCalculator(enable_codebleu=True)
    
    def analyze_and_store_temperature(self, model: str, challenge: str, prompt: str, 
                                    temperature_folder: str) -> str:
        """
        Analyze iterations within a temperature and store clean similarity data.
        
        Args:
            model: Model name (e.g., "claude")
            challenge: Challenge name (e.g., "calculator")
            prompt: Prompt name (e.g., "5-role-zero_shot")
            temperature_folder: Temperature folder name (e.g., "temp_1.0")
            
        Returns:
            Path to stored file
        """
        # Path to temperature directory
        temp_path = self.base_dir / "code" / challenge / prompt / temperature_folder
        
        if not temp_path.exists():
            return self._store_error(model, challenge, prompt, temperature_folder, 
                                   f"Temperature directory not found: {temp_path}")
        
        # Find iteration directories and model files
        iterations = []
        for iter_dir in temp_path.iterdir():
            if iter_dir.is_dir() and iter_dir.name.startswith("iteration_"):
                model_file = iter_dir / f"{model}.py"
                if model_file.exists():
                    iter_num = int(iter_dir.name.split('_')[1])
                    iterations.append((iter_num, str(model_file)))
        
        if len(iterations) < 2:
            return self._store_error(model, challenge, prompt, temperature_folder, 
                                   f"Need at least 2 iterations, found {len(iterations)}")
        
        # Sort by iteration number
        iterations.sort()
        
        # Calculate pairwise similarities
        pairwise_data = []

        for i in range(len(iterations)):
            for j in range(i + 1, len(iterations)):
                iter1_num, file1 = iterations[i]
                iter2_num, file2 = iterations[j]

                # Calculate all similarity metrics
                similarity_result = self.similarity_calc.calculate_all_similarities(file1, file2)

                # Extract clean metrics
                clean_metrics = self._extract_clean_metrics(similarity_result)

                # Add iteration indices to metrics
                comparison = {
                    "i": iter1_num,
                    "j": iter2_num,
                    **clean_metrics
                }
                pairwise_data.append(comparison)
        
        # Store clean data
        return self._store_similarity_data(model, challenge, prompt, temperature_folder, pairwise_data)
    
    def _extract_clean_metrics(self, similarity_result: Dict[str, Any]) -> Dict[str, float]:
        """Extract only the core similarity metrics without statistical noise."""
        clean_metrics = {}

        # CodeBLEU metrics (including BLEU)
        if "codebleu" in similarity_result.get("metrics", {}):
            codebleu_data = similarity_result["metrics"]["codebleu"]
            if "codebleu" in codebleu_data and not isinstance(codebleu_data["codebleu"], str):
                clean_metrics["codebleu"] = round(codebleu_data["codebleu"], 4)
            if "bleu" in codebleu_data and not isinstance(codebleu_data["bleu"], str):
                clean_metrics["bleu"] = round(codebleu_data["bleu"], 4)
            if "syntax_match" in codebleu_data and not isinstance(codebleu_data["syntax_match"], str):
                clean_metrics["syntax_match"] = round(codebleu_data["syntax_match"], 4)
            if "dataflow_match" in codebleu_data and not isinstance(codebleu_data["dataflow_match"], str):
                clean_metrics["dataflow_match"] = round(codebleu_data["dataflow_match"], 4)
            if "weighted_ngram_match" in codebleu_data and not isinstance(codebleu_data["weighted_ngram_match"], str):
                clean_metrics["weighted_ngram_match"] = round(codebleu_data["weighted_ngram_match"], 4)
        
        # AST metrics
        if "ast" in similarity_result.get("metrics", {}):
            ast_data = similarity_result["metrics"]["ast"]
            if "ast_edit_distance" in ast_data and not isinstance(ast_data["ast_edit_distance"], str):
                clean_metrics["ast_edit_distance"] = ast_data["ast_edit_distance"]
            if "tsed" in ast_data and not isinstance(ast_data["tsed"], str):
                clean_metrics["tsed"] = round(ast_data["tsed"], 4)
            if "node_histogram_distance" in ast_data and not isinstance(ast_data["node_histogram_distance"], str):
                clean_metrics["node_histogram_distance"] = round(ast_data["node_histogram_distance"], 4)
            if "subtree_overlap_ratio" in ast_data and not isinstance(ast_data["subtree_overlap_ratio"], str):
                clean_metrics["subtree_overlap_ratio"] = round(ast_data["subtree_overlap_ratio"], 4)
        
        # Jaccard metrics
        if "jaccard" in similarity_result.get("metrics", {}):
            jaccard_data = similarity_result["metrics"]["jaccard"]
            if "jaccard_identifiers" in jaccard_data and not isinstance(jaccard_data["jaccard_identifiers"], str):
                clean_metrics["jaccard_identifiers"] = round(jaccard_data["jaccard_identifiers"], 4)
            if "jaccard_tokens" in jaccard_data and not isinstance(jaccard_data["jaccard_tokens"], str):
                clean_metrics["jaccard_tokens"] = round(jaccard_data["jaccard_tokens"], 4)
            if "jaccard_ast_names" in jaccard_data and not isinstance(jaccard_data["jaccard_ast_names"], str):
                clean_metrics["jaccard_ast_names"] = round(jaccard_data["jaccard_ast_names"], 4)
        
        return clean_metrics
    
    def _store_similarity_data(self, model: str, challenge: str, prompt: str,
                             temperature_folder: str, pairwise_data: List[Dict[str, Any]]) -> str:
        """Store clean similarity data in new hierarchical structure."""
        # Create hierarchical path: challenge/model/temp_X.X.json
        challenge_dir = self.similarity_dir / challenge
        model_dir = challenge_dir / model
        model_dir.mkdir(parents=True, exist_ok=True)

        # Simple filename based on temperature folder
        filename = f"{temperature_folder}.json"
        filepath = model_dir / filename

        # Parse temperature from folder name
        temp_params = self._parse_temperature_folder(temperature_folder)

        # Calculate actual number of iterations from pairwise data
        # For n iterations, we have n*(n-1)/2 pairwise comparisons
        num_comparisons = len(pairwise_data)
        num_iterations = int((1 + (1 + 8 * num_comparisons) ** 0.5) / 2) if num_comparisons > 0 else 0

        # Clean data structure with metadata
        data = {
            "metadata": {
                "analysis_type": "pairwise_within_temperature",
                "challenge": challenge,
                "model": model,
                "temperature": temp_params.get("temperature"),
                "prompt": prompt,
                "generated_at": datetime.now().isoformat(),
                "iterations": num_iterations,
                "comparisons": num_comparisons,
                "temperature_params": {
                    "temperature": temp_params.get("temperature"),
                    "top_k": temp_params.get("top_k"),
                    "top_p": temp_params.get("top_p"),
                    "temperature_folder": temperature_folder
                }
            },
            "similarities": pairwise_data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)
    
    def _store_error(self, model: str, challenge: str, prompt: str,
                    temperature_folder: str, error_msg: str) -> str:
        """Store error information in new hierarchical structure."""
        # Create hierarchical path
        challenge_dir = self.similarity_dir / challenge
        model_dir = challenge_dir / model
        model_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{temperature_folder}_error.json"
        filepath = model_dir / filename

        # Parse temperature from folder name for consistency
        temp_params = self._parse_temperature_folder(temperature_folder)

        data = {
            "metadata": {
                "analysis_type": "pairwise_within_temperature",
                "challenge": challenge,
                "model": model,
                "temperature": temp_params.get("temperature"),
                "prompt": prompt,
                "generated_at": datetime.now().isoformat(),
                "error": error_msg,
                "temperature_params": {
                    "temperature": temp_params.get("temperature"),
                    "top_k": temp_params.get("top_k"),
                    "top_p": temp_params.get("top_p"),
                    "temperature_folder": temperature_folder
                }
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)
    
    def _parse_temperature_folder(self, temperature_folder: str) -> Dict[str, Any]:
        """Parse temperature parameters from folder name."""
        params = {"temperature": None, "top_k": None, "top_p": None}
        
        parts = temperature_folder.split('_')
        for i, part in enumerate(parts):
            if part == "temp" and i+1 < len(parts):
                try:
                    params["temperature"] = float(parts[i+1])
                except ValueError:
                    pass
            elif part == "k" and i+1 < len(parts):
                try:
                    params["top_k"] = int(parts[i+1])
                except ValueError:
                    pass
            elif part == "p" and i+1 < len(parts):
                try:
                    params["top_p"] = float(parts[i+1])
                except ValueError:
                    pass
        
        return params
    
    def batch_analyze_all(self, force_recompute: bool = False) -> Dict[str, Any]:
        """
        Analyze all available model/challenge/prompt/temperature combinations.
        
        Args:
            force_recompute: Whether to recompute existing analyses
            
        Returns:
            Dict with analysis results
        """
        code_dir = self.base_dir / "code"
        if not code_dir.exists():
            return {"error": f"Code directory does not exist: {code_dir}"}
        
        results = {
            "files_created": [],
            "files_skipped": [],
            "errors": []
        }
        
        # Find all combinations
        for challenge_dir in code_dir.iterdir():
            if not challenge_dir.is_dir():
                continue
            
            challenge = challenge_dir.name
            
            for prompt_dir in challenge_dir.iterdir():
                if not prompt_dir.is_dir():
                    continue
                
                prompt = prompt_dir.name
                
                # Find temperature folders
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
                
                # Analyze each model/temperature combination
                for model in models:
                    for temp_folder in temp_folders:
                        try:
                            # Check if file already exists in new structure
                            filepath_check = self.similarity_dir / challenge / model / f"{temp_folder}.json"
                            if not force_recompute and filepath_check.exists():
                                print(f"Skipping {model}/{challenge}/{prompt}/{temp_folder} (already exists)")
                                results["files_skipped"].append(str(filepath_check))
                                continue

                            print(f"Analyzing {model}/{challenge}/{prompt}/{temp_folder}")
                            filepath = self.analyze_and_store_temperature(model, challenge, prompt, temp_folder)
                            results["files_created"].append(filepath)

                        except Exception as e:
                            error_msg = f"Error analyzing {model}/{challenge}/{prompt}/{temp_folder}: {str(e)}"
                            results["errors"].append(error_msg)
                            print(error_msg)
        
        return results
    
    def load_similarity_data(self, model: str, challenge: str,
                           temperature_folder: str) -> Optional[Dict[str, Any]]:
        """
        Load similarity data for a specific combination.

        Args:
            model: Model name (e.g., "claude")
            challenge: Challenge name (e.g., "calculator")
            temperature_folder: Temperature folder name (e.g., "temp_1.0")

        Returns:
            Dict with similarity data or None if not found
        """
        # New hierarchical path: challenge/model/temp_X.X.json
        filepath = self.similarity_dir / challenge / model / f"{temperature_folder}.json"

        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def list_available_data(self) -> List[str]:
        """List all available similarity data files in new hierarchical structure."""
        if not self.similarity_dir.exists():
            return []

        # Find all JSON files in challenge/model/ subdirectories
        files = []
        for json_file in self.similarity_dir.glob("*/*/*.json"):
            if not json_file.name.endswith("_error.json"):
                files.append(str(json_file))

        return sorted(files)


if __name__ == "__main__":
    # Test the clean storage system
    storage = SimilarityStorage("dry_run_output")
    
    # Analyze all available data
    results = storage.batch_analyze_all()
    
    print("Clean similarity analysis results:")
    print(f"Files created: {len(results['files_created'])}")
    print(f"Errors: {len(results['errors'])}")
    
    for file in results["files_created"][:3]:
        print(f"  {file}")