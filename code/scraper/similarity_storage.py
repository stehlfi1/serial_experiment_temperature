"""
Clean similarity storage system for raw comparison metrics.
Stores only essential data without statistical bloat.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from similarity_calculator import SimilarityCalculator


class SimilarityStorage:
    """Store and manage raw similarity metrics data."""
    
    def __init__(self, base_dir: str = "dry_run_output"):
        self.base_dir = Path(base_dir)
        self.similarity_dir = self.base_dir / "similarity_metrics"
        self.similarity_dir.mkdir(parents=True, exist_ok=True)
        
        self.similarity_calc = SimilarityCalculator()
    
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
        pairwise_data = {}
        
        for i in range(len(iterations)):
            for j in range(i + 1, len(iterations)):
                iter1_num, file1 = iterations[i]
                iter2_num, file2 = iterations[j]
                
                # Calculate all similarity metrics
                similarity_result = self.similarity_calc.calculate_all_similarities(file1, file2)
                
                # Extract clean metrics
                clean_metrics = self._extract_clean_metrics(similarity_result)
                
                # Store with clear iteration pair key
                pair_key = f"iter_{iter1_num}_vs_{iter2_num}"
                pairwise_data[pair_key] = clean_metrics
        
        # Store clean data
        return self._store_similarity_data(model, challenge, prompt, temperature_folder, pairwise_data)
    
    def _extract_clean_metrics(self, similarity_result: Dict[str, Any]) -> Dict[str, float]:
        """Extract only the core similarity metrics without statistical noise."""
        clean_metrics = {}
        
        # CodeBLEU metrics
        if "codebleu" in similarity_result.get("metrics", {}):
            codebleu_data = similarity_result["metrics"]["codebleu"]
            if "codebleu" in codebleu_data and not isinstance(codebleu_data["codebleu"], str):
                clean_metrics["codebleu"] = round(codebleu_data["codebleu"], 4)
            if "syntax_match" in codebleu_data and not isinstance(codebleu_data["syntax_match"], str):
                clean_metrics["codebleu_syntax"] = round(codebleu_data["syntax_match"], 4)
            if "dataflow_match" in codebleu_data and not isinstance(codebleu_data["dataflow_match"], str):
                clean_metrics["codebleu_dataflow"] = round(codebleu_data["dataflow_match"], 4)
        
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
                             temperature_folder: str, pairwise_data: Dict[str, Dict[str, float]]) -> str:
        """Store clean similarity data."""
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}.json"
        filepath = self.similarity_dir / filename
        
        # Parse temperature from folder name
        temp_params = self._parse_temperature_folder(temperature_folder)
        
        # Clean data structure
        data = {
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature": temp_params.get("temperature"),
            "top_k": temp_params.get("top_k"),
            "top_p": temp_params.get("top_p"),
            "iterations_compared": len(pairwise_data),
            "generated_at": datetime.now().isoformat(),
            "similarities": pairwise_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def _store_error(self, model: str, challenge: str, prompt: str, 
                    temperature_folder: str, error_msg: str) -> str:
        """Store error information."""
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}_error.json"
        filepath = self.similarity_dir / filename
        
        data = {
            "model": model,
            "challenge": challenge,
            "prompt": prompt,
            "temperature_folder": temperature_folder,
            "error": error_msg,
            "generated_at": datetime.now().isoformat()
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
                            # Check if file already exists
                            filename = f"{model}_{challenge}_{prompt}_{temp_folder}.json"
                            if not force_recompute and (self.similarity_dir / filename).exists():
                                print(f"Skipping {model}/{challenge}/{prompt}/{temp_folder} (already exists)")
                                continue
                            
                            print(f"Analyzing {model}/{challenge}/{prompt}/{temp_folder}")
                            filepath = self.analyze_and_store_temperature(model, challenge, prompt, temp_folder)
                            results["files_created"].append(filepath)
                            
                        except Exception as e:
                            error_msg = f"Error analyzing {model}/{challenge}/{prompt}/{temp_folder}: {str(e)}"
                            results["errors"].append(error_msg)
                            print(error_msg)
        
        return results
    
    def load_similarity_data(self, model: str, challenge: str, prompt: str, 
                           temperature_folder: str) -> Optional[Dict[str, Any]]:
        """Load similarity data for a specific combination."""
        filename = f"{model}_{challenge}_{prompt}_{temperature_folder}.json"
        filepath = self.similarity_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def list_available_data(self) -> List[str]:
        """List all available similarity data files."""
        if not self.similarity_dir.exists():
            return []
        
        return [str(f) for f in self.similarity_dir.glob("*.json") if not f.name.endswith("_error.json")]


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