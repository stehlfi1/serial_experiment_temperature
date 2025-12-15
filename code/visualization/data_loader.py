"""
Data loader for similarity analysis results.
Loads all similarity JSON files and combines into unified DataFrame.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_filtering import get_non_compilable_iterations, get_exclusion_summary


class SimilarityDataLoader:
    """Load and combine similarity data from all experiments."""

    def __init__(self, base_dir: str = "dry_run_output"):
        self.base_dir = Path(base_dir)
        self.similarity_dir = self.base_dir / "similarity_analysis" / "pairwise_within_temperature"

    def load_all_data(self) -> pd.DataFrame:
        """
        Load all similarity files into a single DataFrame.
        Automatically excludes non-compilable iterations.

        Returns:
            DataFrame with columns: challenge, model, temperature, i, j, and all metrics
        """
        # Get list of non-compilable iterations to exclude
        non_compilable = get_non_compilable_iterations()

        if non_compilable:
            summary = get_exclusion_summary(non_compilable)
            print(f"Excluding {summary['total_excluded']} non-compilable iterations ({summary['percentage']:.2f}%)")
            for model, challenge, temp, iteration in summary['details']:
                print(f"  - {model}/{challenge}/temp_{temp}/iteration_{iteration}")
            print()

        all_data = []

        # Find all JSON files
        for json_file in self.similarity_dir.glob("*/*/*.json"):
            if json_file.name.endswith("_error.json"):
                continue

            # Load file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract metadata
            metadata = data['metadata']
            challenge = metadata['challenge']
            model = metadata['model']
            temperature = metadata['temperature']

            # Convert similarities array to DataFrame
            similarities_df = pd.DataFrame(data['similarities'])

            # Filter out comparisons involving non-compilable iterations
            if non_compilable:
                for nc_model, nc_challenge, nc_temp, nc_iteration in non_compilable:
                    if model == nc_model and challenge == nc_challenge and temperature == nc_temp:
                        # Exclude rows where i or j equals the non-compilable iteration
                        similarities_df = similarities_df[
                            (similarities_df['i'] != nc_iteration) &
                            (similarities_df['j'] != nc_iteration)
                        ]

            # Add metadata columns
            similarities_df['challenge'] = challenge
            similarities_df['model'] = model
            similarities_df['temperature'] = temperature

            all_data.append(similarities_df)

        # Combine all data
        if not all_data:
            raise ValueError(f"No similarity data found in {self.similarity_dir}")

        combined_df = pd.concat(all_data, ignore_index=True)

        # Reorder columns: metadata first, then indices, then metrics
        metadata_cols = ['challenge', 'model', 'temperature', 'i', 'j']
        metric_cols = [col for col in combined_df.columns if col not in metadata_cols]
        combined_df = combined_df[metadata_cols + metric_cols]

        return combined_df

    def get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics about the loaded data."""
        return {
            'total_comparisons': len(df),
            'challenges': sorted(df['challenge'].unique().tolist()),
            'models': sorted(df['model'].unique().tolist()),
            'temperatures': sorted(df['temperature'].unique().tolist()),
            'metrics': [col for col in df.columns if col not in ['challenge', 'model', 'temperature', 'i', 'j']],
            'comparisons_per_temperature': len(df[df['temperature'] == df['temperature'].iloc[0]]),
        }


if __name__ == "__main__":
    # Test loading
    loader = SimilarityDataLoader()
    df = loader.load_all_data()

    print("Loaded similarity data:")
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())

    print(f"\nSummary:")
    summary = loader.get_summary(df)
    for key, value in summary.items():
        print(f"  {key}: {value}")
