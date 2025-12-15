"""
LaTeX table export utilities for similarity analysis.
Generates publication-ready tables for thesis document.
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from pathlib import Path


class LaTeXTableExporter:
    """Export similarity statistics as LaTeX tables."""

    def __init__(self, df: pd.DataFrame, output_dir: str = "tables"):
        """
        Initialize exporter.

        Args:
            df: DataFrame from SimilarityDataLoader
            output_dir: Directory to save LaTeX tables
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_temperature_summary(
        self,
        metrics: List[str] = ['codebleu', 'ast_edit_distance', 'tsed'],
        filename: str = "temperature_summary.tex"
    ) -> str:
        """
        Export summary table of metric means across temperatures.

        Args:
            metrics: List of metrics to include
            filename: Output filename

        Returns:
            Path to saved table
        """
        # Calculate means per temperature for each metric
        results = None

        for metric in metrics:
            # Filter out inf and nan values for this metric
            df_clean = self.df[np.isfinite(self.df[metric])].copy()
            grouped = df_clean.groupby('temperature')[metric]
            stats = pd.DataFrame({
                'Temperature': grouped.mean().index,
                metric: grouped.mean().values
            })

            if results is None:
                results = stats
            else:
                results = results.merge(stats, on='Temperature')

        # Format for LaTeX
        latex_table = self._dataframe_to_latex(
            results,
            caption=f"Mean similarity scores across temperatures",
            label="tab:temperature_summary",
            float_format="%.4f"
        )

        # Save
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            f.write(latex_table)

        return str(filepath)

    def export_model_comparison(
        self,
        metric: str,
        temperatures: Optional[List[float]] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Export model comparison table for a specific metric.

        Args:
            metric: Metric to analyze
            temperatures: List of temperatures to include (None = all)
            filename: Output filename (auto-generated if None)

        Returns:
            Path to saved table
        """
        df_filtered = self.df.copy()

        if temperatures:
            df_filtered = df_filtered[df_filtered['temperature'].isin(temperatures)]

        # Filter out inf and nan values for this metric
        df_filtered = df_filtered[np.isfinite(df_filtered[metric])]

        # Pivot table: rows=models, columns=temperatures
        pivot = df_filtered.pivot_table(
            values=metric,
            index='model',
            columns='temperature',
            aggfunc='mean'
        )

        # Format model names
        pivot.index = pivot.index.str.capitalize()
        pivot.columns.name = 'Temperature'

        # Generate LaTeX
        latex_table = self._dataframe_to_latex(
            pivot.reset_index(),
            caption=f"{metric.replace('_', ' ').title()} comparison across models and temperatures",
            label=f"tab:model_comparison_{metric}",
            float_format="%.4f"
        )

        # Save
        if filename is None:
            filename = f"model_comparison_{metric}.tex"
        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            f.write(latex_table)

        return str(filepath)

    def export_consistency_analysis(
        self,
        metrics: List[str] = ['codebleu', 'ast_edit_distance', 'tsed'],
        filename: str = "consistency_analysis.tex"
    ) -> str:
        """
        Export consistency (CV) analysis table.

        Args:
            metrics: List of metrics to analyze
            filename: Output filename

        Returns:
            Path to saved table
        """
        results = []

        for metric in metrics:
            # Filter out inf and nan values for this metric
            df_clean = self.df[np.isfinite(self.df[metric])].copy()

            for model in sorted(df_clean['model'].unique()):
                df_model = df_clean[df_clean['model'] == model]

                for temp in sorted(df_model['temperature'].unique()):
                    df_temp = df_model[df_model['temperature'] == temp]

                    mean = df_temp[metric].mean()
                    std = df_temp[metric].std()
                    cv = (std / mean) * 100

                    results.append({
                        'Model': model.capitalize(),
                        'Temperature': temp,
                        'Metric': metric.replace('_', ' ').title(),
                        'Mean': mean,
                        'Std': std,
                        'CV (%)': cv
                    })

        result_df = pd.DataFrame(results)

        # Generate LaTeX
        latex_table = self._dataframe_to_latex(
            result_df,
            caption="Consistency analysis: Coefficient of Variation (CV) for similarity metrics",
            label="tab:consistency_analysis",
            float_format="%.4f"
        )

        # Save
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            f.write(latex_table)

        return str(filepath)

    def export_challenge_breakdown(
        self,
        metric: str,
        filename: Optional[str] = None
    ) -> str:
        """
        Export breakdown by challenge for a specific metric.

        Args:
            metric: Metric to analyze
            filename: Output filename (auto-generated if None)

        Returns:
            Path to saved table
        """
        # Filter out inf and nan values for this metric
        df_clean = self.df[np.isfinite(self.df[metric])].copy()

        # Pivot: rows=challenges, columns=temperatures
        pivot = df_clean.pivot_table(
            values=metric,
            index='challenge',
            columns='temperature',
            aggfunc='mean'
        )

        # Format challenge names
        pivot.index = pivot.index.str.replace('_', ' ').str.title()
        pivot.columns.name = 'Temperature'

        # Generate LaTeX
        latex_table = self._dataframe_to_latex(
            pivot.reset_index(),
            caption=f"{metric.replace('_', ' ').title()} by challenge across temperatures",
            label=f"tab:challenge_breakdown_{metric}",
            float_format="%.4f"
        )

        # Save
        if filename is None:
            filename = f"challenge_breakdown_{metric}.tex"
        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            f.write(latex_table)

        return str(filepath)

    def _dataframe_to_latex(
        self,
        df: pd.DataFrame,
        caption: str,
        label: str,
        float_format: str = "%.4f"
    ) -> str:
        """
        Convert DataFrame to LaTeX table with proper formatting.

        Args:
            df: DataFrame to convert
            caption: Table caption
            label: LaTeX label for referencing
            float_format: Format string for float values

        Returns:
            LaTeX table string
        """
        # Generate base LaTeX
        latex = df.to_latex(
            index=False,
            float_format=float_format,
            escape=False,
            column_format='l' + 'r' * (len(df.columns) - 1)
        )

        # Wrap in table environment with caption and label
        wrapped = f"""\\begin{{table}}[htbp]
    \\centering
    \\caption{{{caption}}}
    \\label{{{label}}}
    {latex.strip()}
\\end{{table}}"""

        return wrapped


if __name__ == "__main__":
    from data_loader import SimilarityDataLoader

    # Test LaTeX export
    loader = SimilarityDataLoader()
    df = loader.load_all_data()
    exporter = LaTeXTableExporter(df)

    print("Generating LaTeX tables...")
    print()

    # 1. Temperature summary
    print("1. Temperature summary table...")
    path1 = exporter.export_temperature_summary()
    print(f"   Saved to: {path1}")

    # 2. Model comparison (CodeBLEU)
    print("2. Model comparison table (CodeBLEU)...")
    path2 = exporter.export_model_comparison('codebleu')
    print(f"   Saved to: {path2}")

    # 3. Consistency analysis
    print("3. Consistency analysis table...")
    path3 = exporter.export_consistency_analysis()
    print(f"   Saved to: {path3}")

    # 4. Challenge breakdown (CodeBLEU)
    print("4. Challenge breakdown table (CodeBLEU)...")
    path4 = exporter.export_challenge_breakdown('codebleu')
    print(f"   Saved to: {path4}")

    print()
    print("Done! Tables ready for LaTeX inclusion.")
