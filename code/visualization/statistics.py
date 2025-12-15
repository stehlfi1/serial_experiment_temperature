"""
Statistical analysis of similarity data.
Calculates aggregated metrics per temperature/model/challenge.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


class TemperatureStatistics:
    """Calculate statistics for temperature effect analysis."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with loaded similarity data.

        Args:
            df: DataFrame from SimilarityDataLoader
        """
        self.df = df

    def aggregate_by_temperature(
        self,
        metrics: List[str],
        groupby: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Aggregate metrics by temperature (and optionally other groupings).

        Args:
            metrics: List of metric names to aggregate
            groupby: Additional grouping columns (e.g., ['model', 'challenge'])

        Returns:
            DataFrame with mean, std, and CV for each metric
        """
        if groupby is None:
            groupby = ['temperature']
        elif 'temperature' not in groupby:
            groupby = ['temperature'] + groupby

        results = []

        for metric in metrics:
            # Filter out inf and nan values for this metric
            df_clean = self.df[np.isfinite(self.df[metric])].copy()
            grouped = df_clean.groupby(groupby)[metric]

            stats = pd.DataFrame({
                'metric': metric,
                'mean': grouped.mean(),
                'std': grouped.std(),
                'min': grouped.min(),
                'max': grouped.max(),
                'count': grouped.count()
            })

            # Coefficient of Variation (CV) = std / mean
            stats['cv'] = stats['std'] / stats['mean']

            # Standard Error
            stats['se'] = stats['std'] / np.sqrt(stats['count'])

            results.append(stats.reset_index())

        return pd.concat(results, ignore_index=True)

    def get_temperature_effect(
        self,
        metric: str,
        model: Optional[str] = None,
        challenge: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get mean and std for a metric across temperatures.

        Args:
            metric: Metric name (e.g., 'codebleu')
            model: Optional model filter
            challenge: Optional challenge filter

        Returns:
            DataFrame with temperature, mean, std, se
        """
        df_filtered = self.df.copy()

        if model:
            df_filtered = df_filtered[df_filtered['model'] == model]
        if challenge:
            df_filtered = df_filtered[df_filtered['challenge'] == challenge]

        # Filter out inf and nan values
        df_filtered = df_filtered[np.isfinite(df_filtered[metric])]

        grouped = df_filtered.groupby('temperature')[metric]

        return pd.DataFrame({
            'temperature': grouped.mean().index,
            'mean': grouped.mean().values,
            'std': grouped.std().values,
            'se': grouped.std().values / np.sqrt(grouped.count().values),
            'count': grouped.count().values
        })

    def get_model_comparison(
        self,
        metric: str,
        temperature: Optional[float] = None,
        challenge: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Compare models at a specific temperature.

        Args:
            metric: Metric name
            temperature: Optional temperature filter
            challenge: Optional challenge filter

        Returns:
            DataFrame with model, mean, std, cv
        """
        df_filtered = self.df.copy()

        if temperature is not None:
            df_filtered = df_filtered[df_filtered['temperature'] == temperature]
        if challenge:
            df_filtered = df_filtered[df_filtered['challenge'] == challenge]

        # Filter out inf and nan values
        df_filtered = df_filtered[np.isfinite(df_filtered[metric])]

        grouped = df_filtered.groupby('model')[metric]

        result = pd.DataFrame({
            'model': grouped.mean().index,
            'mean': grouped.mean().values,
            'std': grouped.std().values,
            'count': grouped.count().values
        })
        result['cv'] = result['std'] / result['mean']

        return result

    def get_consistency_scores(
        self,
        metric: str,
        groupby: List[str] = ['model', 'temperature', 'challenge']
    ) -> pd.DataFrame:
        """
        Calculate consistency (inverse of CV) for each group.
        Higher consistency = lower variance = more deterministic.

        Args:
            metric: Metric name
            groupby: Grouping columns

        Returns:
            DataFrame with consistency scores (1 - CV)
        """
        # Filter out inf and nan values
        df_clean = self.df[np.isfinite(self.df[metric])].copy()
        grouped = df_clean.groupby(groupby)[metric]

        result = pd.DataFrame({
            'mean': grouped.mean(),
            'std': grouped.std(),
            'count': grouped.count()
        }).reset_index()

        result['cv'] = result['std'] / result['mean']
        result['consistency'] = 1 - result['cv']  # Higher = more consistent

        return result


if __name__ == "__main__":
    from .data_loader import SimilarityDataLoader

    # Test statistics
    loader = SimilarityDataLoader()
    df = loader.load_all_data()
    stats = TemperatureStatistics(df)

    print("Temperature Effect for CodeBLEU (all models, all challenges):")
    temp_effect = stats.get_temperature_effect('codebleu')
    print(temp_effect)
    print()

    print("Model Comparison at T=1.0 for CodeBLEU:")
    model_comp = stats.get_model_comparison('codebleu', temperature=1.0)
    print(model_comp)
    print()

    print("Consistency Scores (CodeBLEU):")
    consistency = stats.get_consistency_scores('codebleu')
    print(consistency.head(10))
