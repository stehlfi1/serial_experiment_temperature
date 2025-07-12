from pathlib import Path
from typing import Optional
import json
from datetime import datetime


def create_temp_folder_name(temperature: float, top_k: int = None, top_p: float = None) -> str:
    """Create temperature folder name with optional top_k and top_p parameters."""
    folder_name = f"temp_{temperature}"
    if top_k is not None:
        folder_name += f"_top_k_{top_k}"
    if top_p is not None:
        folder_name += f"_top_p_{top_p}"
    return folder_name


def parse_temp_folder_params(folder_path: str) -> dict:
    """Extract temperature and optional top_k/top_p from folder name."""
    folder_name = Path(folder_path).name
    params = {"temperature": None, "top_k": None, "top_p": None}
    
    # Parse temp_1.0_top_k_40_top_p_0.9
    parts = folder_name.split('_')
    for i, part in enumerate(parts):
        if part == "temp" and i+1 < len(parts):
            params["temperature"] = float(parts[i+1])
        elif part == "k" and i+1 < len(parts):  # top_k_40
            params["top_k"] = int(parts[i+1])
        elif part == "p" and i+1 < len(parts):  # top_p_0.9
            params["top_p"] = float(parts[i+1])
    
    return params


def find_next_iteration(temp_folder_path: Path) -> int:
    """Find the next available iteration number in the temperature folder."""
    if not temp_folder_path.exists():
        return 1
    
    i = 1
    while (temp_folder_path / f"iteration_{i}").exists():
        i += 1
    return i


def get_iteration_range(temp_folder_path: Path, requested_iterations: int) -> range:
    """Get iteration range starting from next available iteration."""
    start = find_next_iteration(temp_folder_path)
    return range(start, start + requested_iterations)


def create_output_directories(base_dir: str, challenge_name: str, prompt_name: str, iteration: int, 
                             temperature: float = 1.0, top_k: int = None, top_p: float = None) -> tuple[str, str]:
    """Create output directories for code and response files."""
    project_root = Path(__file__).parent.parent.parent
    temp_folder = create_temp_folder_name(temperature, top_k, top_p)
    code_dir = project_root / base_dir / "code" / challenge_name / prompt_name / temp_folder / f"iteration_{iteration}"
    response_dir = project_root / base_dir / "response" / challenge_name / prompt_name / temp_folder / f"iteration_{iteration}"
    
    code_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)
    
    return str(code_dir), str(response_dir)


def write_generation_metadata(code_dir: str, llms: list, temperature: float, top_k: int = None, top_p: float = None) -> None:
    """Write generation parameters metadata to the code directory."""
    metadata = {
        "generation_timestamp": datetime.now().isoformat(),
        "models": {}
    }
    
    for llm in llms:
        metadata["models"][llm.name] = {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "model_id": llm.model,
            "provider": llm.model.split('/')[0] if '/' in llm.model else "unknown"
        }
    
    metadata_file = Path(code_dir) / "generation_params.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def write_llm_output(code_dir: str, response_dir: str, llm_name: str, response_content: str) -> None:
    """Write LLM response and extracted code to files."""
    from ..shared.utils import extract_python_code
    
    response_file = Path(response_dir) / f"{llm_name}_response.txt"
    with open(response_file, "w", encoding="utf-8") as f:
        f.write(response_content)
    
    code_file = Path(code_dir) / f"{llm_name}.py"
    with open(code_file, "w", encoding="utf-8") as f:
        f.write(extract_python_code(response_content))