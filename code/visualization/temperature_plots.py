"""
Temperature effect visualization.
Generates publication-ready plots for LaTeX documents.
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple

# Configure matplotlib for LaTeX-compatible output
matplotlib.use('Agg')  # Non-interactive backend
matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 12,
    'lines.linewidth': 1.5,
    'lines.markersize': 6,
})

# Okabe-Ito colorblind-safe palette
COLORS = {
    'claude': '#E69F00',    # Orange
    'chatgpt': '#56B4E9',   # Sky Blue
    'gemini': '#009E73',    # Blueish Green
}


class TemperaturePlotter:
    """Generate temperature effect visualizations."""

    def __init__(self, df: pd.DataFrame, output_dir: str = "figures/similarity"):
        """
        Initialize plotter.

        Args:
            df: DataFrame from SimilarityDataLoader
            output_dir: Directory to save figures
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_temperature_effect_combined(
        self,
        metrics: List[str] = ['codebleu', 'ast_edit_distance', 'tsed'],
        challenge: Optional[str] = None,
        figsize: Tuple[float, float] = (8, 10)
    ) -> str:
        """
        Create combined plot with 3 subplots for primary metrics.

        Args:
            metrics: List of metrics to plot (max 3)
            challenge: Optional challenge filter
            figsize: Figure size (width, height)

        Returns:
            Path to saved figure
        """
        df_filtered = self.df.copy()
        if challenge:
            df_filtered = df_filtered[df_filtered['challenge'] == challenge]

        # Create figure with subplots
        fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
        if len(metrics) == 1:
            axes = [axes]

        temperatures = sorted(df_filtered['temperature'].unique())
        models = sorted(df_filtered['model'].unique())

        for idx, metric in enumerate(metrics):
            ax = axes[idx]

            for model in models:
                df_model = df_filtered[df_filtered['model'] == model]

                # Filter out inf and nan values for this metric
                df_model = df_model[np.isfinite(df_model[metric])]

                # Calculate mean and std per temperature
                grouped = df_model.groupby('temperature')[metric]
                means = grouped.mean()
                stds = grouped.std()

                # Plot line with error band
                ax.plot(temperatures, means, label=model.capitalize(),
                       color=COLORS.get(model, 'gray'), marker='o')
                ax.fill_between(temperatures,
                               means - stds,
                               means + stds,
                               alpha=0.2,
                               color=COLORS.get(model, 'gray'))

            # Formatting
            ax.set_ylabel(self._get_metric_label(metric))
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(loc='best')

            # Only show legend on first subplot
            if idx > 0:
                ax.legend().set_visible(False)

        axes[-1].set_xlabel('Temperature')
        axes[0].legend(loc='upper right')

        # Overall title
        title = "Temperature Effect on Code Similarity"
        if challenge:
            title += f" ({challenge.replace('_', ' ').title()})"
        fig.suptitle(title, fontsize=12, fontweight='bold')

        plt.tight_layout()

        # Save
        filename = f"temperature_effect"
        if challenge:
            filename += f"_{challenge}"
        filepath = self.output_dir / f"{filename}.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_single_metric_per_challenge(
        self,
        metric: str,
        figsize: Tuple[float, float] = (12, 4)
    ) -> str:
        """
        Create faceted plot showing one metric across all challenges.

        Args:
            metric: Metric to plot
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        challenges = sorted(self.df['challenge'].unique())
        models = sorted(self.df['model'].unique())
        temperatures = sorted(self.df['temperature'].unique())

        fig, axes = plt.subplots(1, len(challenges), figsize=figsize, sharey=True)
        if len(challenges) == 1:
            axes = [axes]

        for idx, challenge in enumerate(challenges):
            ax = axes[idx]
            df_challenge = self.df[self.df['challenge'] == challenge]

            for model in models:
                df_model = df_challenge[df_challenge['model'] == model]

                # Filter out inf and nan values for this metric
                df_model = df_model[np.isfinite(df_model[metric])]

                grouped = df_model.groupby('temperature')[metric]
                means = grouped.mean()
                stds = grouped.std()

                ax.plot(temperatures, means, label=model.capitalize(),
                       color=COLORS.get(model, 'gray'), marker='o')
                ax.fill_between(temperatures,
                               means - stds,
                               means + stds,
                               alpha=0.2,
                               color=COLORS.get(model, 'gray'))

            ax.set_title(challenge.replace('_', ' ').title())
            ax.set_xlabel('Temperature')
            ax.grid(True, alpha=0.3, linestyle='--')

            if idx == 0:
                ax.set_ylabel(self._get_metric_label(metric))
            if idx == len(challenges) - 1:
                ax.legend(loc='best')

        plt.tight_layout()

        filename = f"{metric}_by_challenge.pdf"
        filepath = self.output_dir / filename
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_consistency(
        self,
        metric: str,
        figsize: Tuple[float, float] = (8, 5)
    ) -> str:
        """
        Plot coefficient of variation (CV) across temperatures.
        Lower CV = more consistent.

        Args:
            metric: Metric to analyze
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        models = sorted(self.df['model'].unique())
        temperatures = sorted(self.df['temperature'].unique())

        fig, ax = plt.subplots(figsize=figsize)

        for model in models:
            df_model = self.df[self.df['model'] == model]

            # Filter out inf and nan values for this metric
            df_model = df_model[np.isfinite(df_model[metric])]

            cvs = []

            for temp in temperatures:
                df_temp = df_model[df_model['temperature'] == temp]
                std = df_temp[metric].std()
                mean = df_temp[metric].mean()
                cv = (std / mean) * 100  # as percentage
                cvs.append(cv)

            ax.plot(temperatures, cvs, label=model.capitalize(),
                   color=COLORS.get(model, 'gray'), marker='o')

        ax.set_xlabel('Temperature')
        ax.set_ylabel('Coefficient of Variation (%)')
        ax.set_title(f'Consistency Analysis: {self._get_metric_label(metric)}')
        ax.legend()
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        filename = f"consistency_{metric}.pdf"
        filepath = self.output_dir / filename
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def _get_metric_label(self, metric: str) -> str:
        """Get human-readable label for metric."""
        labels = {
            'codebleu': 'CodeBLEU Score',
            'bleu': 'BLEU Score',
            'ast_edit_distance': 'AST Edit Distance',
            'tsed': 'TSED',
            'syntax_match': 'Syntax Match Score',
            'jaccard_tokens': 'Jaccard Similarity (Tokens)',
        }
        return labels.get(metric, metric.replace('_', ' ').title())


if __name__ == "__main__":
    from .data_loader import SimilarityDataLoader

    # Test plotting
    loader = SimilarityDataLoader()
    df = loader.load_all_data()
    plotter = TemperaturePlotter(df)

    print("Generating plots...")

    # Combined 3-metric plot
    print("1. Combined temperature effect plot...")
    path1 = plotter.plot_temperature_effect_combined()
    print(f"   Saved to: {path1}")

    # Single metric by challenge
    print("2. CodeBLEU by challenge plot...")
    path2 = plotter.plot_single_metric_per_challenge('codebleu')
    print(f"   Saved to: {path2}")

    # Consistency
    print("3. Consistency plot...")
    path3 = plotter.plot_consistency('codebleu')
    print(f"   Saved to: {path3}")

    print("\nDone!")
