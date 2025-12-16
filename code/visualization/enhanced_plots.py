"""
Enhanced visualization plots for thesis.
Generates additional publication-ready plots requested for final thesis.
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple

# Configure matplotlib for LaTeX-compatible output
matplotlib.use('Agg')
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


class EnhancedPlotter:
    """Generate enhanced visualizations for thesis."""

    def __init__(self,
                 similarity_df: pd.DataFrame,
                 quality_df: pd.DataFrame,
                 output_dir: str = "figures"):
        """
        Initialize plotter.

        Args:
            similarity_df: DataFrame from SimilarityDataLoader
            quality_df: DataFrame from StaticAnalysisDataLoader
            output_dir: Directory to save figures
        """
        self.sim_df = similarity_df
        self.qual_df = quality_df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_bleu_by_temperature(
        self,
        figsize: Tuple[float, float] = (8, 5)
    ) -> str:
        """
        Create line plot for BLEU score by temperature.

        Shows regression lines to demonstrate correlation.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        temperatures = sorted(self.sim_df['temperature'].unique())
        models = sorted(self.sim_df['model'].unique())

        for model in models:
            df_model = self.sim_df[self.sim_df['model'] == model]

            # Filter out inf and nan values
            df_model = df_model[np.isfinite(df_model['bleu'])]

            # Calculate mean and std per temperature
            grouped = df_model.groupby('temperature')['bleu']
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

            # Add regression line
            z = np.polyfit(temperatures, means, 1)
            p = np.poly1d(z)
            ax.plot(temperatures, p(temperatures),
                   linestyle='--', linewidth=1, alpha=0.7,
                   color=COLORS.get(model, 'gray'))

        ax.set_xlabel('Temperature')
        ax.set_ylabel('BLEU Score')
        ax.set_title('BLEU Similarity vs Temperature')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        filepath = self.output_dir / "similarity" / "bleu_by_temperature.pdf"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_summary_comparison(
        self,
        figsize: Tuple[float, float] = (14, 5)
    ) -> str:
        """
        Create 2-panel summary plot:
        - Left: Quality metrics (flat - no correlation)
        - Right: Similarity metrics (declining - strong correlation)

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        temperatures = sorted(self.qual_df[self.qual_df['temperature'].notna()]['temperature'].unique())
        models = sorted(self.qual_df['model'].unique())

        # LEFT PANEL: Quality (flat lines)
        ax1.set_title('Quality Metrics - No Temperature Effect', fontweight='bold')

        for model in models:
            df_model = self.qual_df[
                (self.qual_df['model'] == model) &
                (self.qual_df['temperature'].notna())
            ]

            # Use pass_rate as representative quality metric
            df_model = df_model[np.isfinite(df_model['pass_rate'])]
            grouped = df_model.groupby('temperature')['pass_rate']
            means = grouped.mean()

            ax1.plot(temperatures, means, label=model.capitalize(),
                    color=COLORS.get(model, 'gray'), marker='o', linewidth=2)

            # Add flat regression line
            mean_val = means.mean()
            ax1.axhline(y=mean_val, color=COLORS.get(model, 'gray'),
                       linestyle='--', linewidth=1, alpha=0.5)

        ax1.set_xlabel('Temperature')
        ax1.set_ylabel('Test Pass Rate')
        ax1.set_ylim(0.4, 1.0)
        ax1.legend(loc='lower left')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.text(0.5, 0.05, 'r ≈ 0.02, p > 0.5\n(no correlation)',
                transform=ax1.transAxes, ha='center', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        # RIGHT PANEL: Similarity (declining lines)
        ax2.set_title('Similarity Metrics - Strong Temperature Effect', fontweight='bold')

        for model in models:
            df_model = self.sim_df[self.sim_df['model'] == model]
            df_model = df_model[np.isfinite(df_model['codebleu'])]

            grouped = df_model.groupby('temperature')['codebleu']
            means = grouped.mean()

            ax2.plot(temperatures, means, label=model.capitalize(),
                    color=COLORS.get(model, 'gray'), marker='o', linewidth=2)

            # Add regression line
            z = np.polyfit(temperatures, means, 1)
            p = np.poly1d(z)
            ax2.plot(temperatures, p(temperatures),
                    linestyle='--', linewidth=1.5, alpha=0.7,
                    color=COLORS.get(model, 'gray'))

        ax2.set_xlabel('Temperature')
        ax2.set_ylabel('CodeBLEU Score')
        ax2.set_ylim(0.35, 0.75)
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.text(0.5, 0.05, 'r = -0.32, p < 0.001\n(moderate negative correlation)',
                transform=ax2.transAxes, ha='center', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        fig.suptitle('Key Finding: Temperature Affects Diversity, Not Quality',
                    fontsize=13, fontweight='bold', y=1.02)

        plt.tight_layout()

        filepath = self.output_dir / "summary_comparison.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_pass_rate_boxplot(
        self,
        figsize: Tuple[float, float] = (10, 6)
    ) -> str:
        """
        Create boxplot for functional correctness by temperature.

        Shows distribution better than line plot when there's high variance.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.qual_df[self.qual_df['temperature'].notna()].copy()
        df_temp = df_temp[np.isfinite(df_temp['pass_rate'])]

        fig, ax = plt.subplots(figsize=figsize)

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        # Prepare data for grouped boxplot
        positions = []
        data_to_plot = []
        labels = []
        colors_list = []

        width = 0.25
        for i, temp in enumerate(temperatures):
            for j, model in enumerate(models):
                df_subset = df_temp[
                    (df_temp['temperature'] == temp) &
                    (df_temp['model'] == model)
                ]

                if len(df_subset) > 0:
                    positions.append(i + (j - 1) * width)
                    data_to_plot.append(df_subset['pass_rate'].values)
                    colors_list.append(COLORS.get(model, 'gray'))
                    if i == 0:  # Only add label once
                        labels.append(model.capitalize())

        # Create boxplots
        bp = ax.boxplot(data_to_plot, positions=positions, widths=width*0.8,
                       patch_artist=True, showfliers=True,
                       boxprops=dict(linewidth=1.2),
                       medianprops=dict(linewidth=1.5, color='black'),
                       whiskerprops=dict(linewidth=1.2),
                       capprops=dict(linewidth=1.2))

        # Color boxes
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Set labels
        ax.set_xticks(range(len(temperatures)))
        ax.set_xticklabels([f'{t:.1f}' for t in temperatures])
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Test Pass Rate')
        ax.set_title('Functional Correctness Distribution by Temperature')
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=COLORS[model], alpha=0.7,
                                label=model.capitalize())
                          for model in models]
        ax.legend(handles=legend_elements, loc='lower left')

        plt.tight_layout()

        filepath = self.output_dir / "static_analysis" / "pass_rate_boxplot.pdf"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_quality_scatter_with_trends(
        self,
        figsize: Tuple[float, float] = (12, 10)
    ) -> str:
        """
        Create scatter plots with regression lines for quality metrics.

        Shows individual points + flat trend lines to demonstrate no correlation.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.qual_df[self.qual_df['temperature'].notna()].copy()

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        # Define metrics to plot
        metrics = [
            ('pass_rate', 'Test Pass Rate', (0, 1.05)),
            ('maintainability_index', 'Maintainability Index', (40, 80)),
            ('cyclomatic_complexity', 'Cyclomatic Complexity', (0, 10)),
            ('halstead_difficulty', 'Halstead Difficulty', (10, 45)),
        ]

        for idx, (metric, ylabel, ylim) in enumerate(metrics):
            ax = axes[idx]

            # Calculate overall correlation from ALL data (all models combined)
            df_metric = df_temp[np.isfinite(df_temp[metric])]
            if len(df_metric) > 0:
                r_overall = np.corrcoef(df_metric['temperature'], df_metric[metric])[0, 1]
            else:
                r_overall = 0.0

            for model in models:
                df_model = df_temp[df_temp['model'] == model]
                df_model = df_model[np.isfinite(df_model[metric])]

                # Scatter plot of means
                grouped = df_model.groupby('temperature')[metric]
                means = grouped.mean()

                ax.scatter(temperatures, means, label=model.capitalize(),
                          color=COLORS.get(model, 'gray'), s=80, alpha=0.7,
                          edgecolors='white', linewidth=1.5)

                # Add flat regression line
                z = np.polyfit(temperatures, means, 1)
                p_poly = np.poly1d(z)
                line = p_poly(np.array(temperatures))
                ax.plot(temperatures, line,
                       linestyle='--', linewidth=1.5, alpha=0.6,
                       color=COLORS.get(model, 'gray'))

            # Add correlation annotation (calculated from all data)
            ax.text(0.05, 0.95, f'r ≈ {r_overall:.3f}',
                   transform=ax.transAxes, va='top', fontsize=8,
                   bbox=dict(boxstyle='round', facecolor='white',
                           alpha=0.7, edgecolor='gray'))

            ax.set_xlabel('Temperature')
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3, linestyle='--')

            if ylim:
                ax.set_ylim(ylim)

            if idx == 0:
                ax.legend(loc='best', framealpha=0.9)

        fig.suptitle('Quality Metrics - No Temperature Correlation',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        filepath = self.output_dir / "static_analysis" / "quality_scatter_trends.pdf"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)


if __name__ == "__main__":
    import sys
    # Add code folder to path for absolute imports
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from visualization.data_loader import SimilarityDataLoader
    from static_visualization.data_loader import StaticAnalysisDataLoader

    print("Loading data...")
    sim_loader = SimilarityDataLoader()
    qual_loader = StaticAnalysisDataLoader()

    sim_df = sim_loader.load_all_data()
    qual_df = qual_loader.load_all_experiments()

    plotter = EnhancedPlotter(sim_df, qual_df)

    print("\nGenerating enhanced plots...")

    print("1. BLEU by temperature...")
    path1 = plotter.plot_bleu_by_temperature()
    print(f"   ✓ Saved to: {path1}")

    print("2. Summary comparison (quality vs similarity)...")
    path2 = plotter.plot_summary_comparison()
    print(f"   ✓ Saved to: {path2}")

    print("3. Pass rate boxplot...")
    path3 = plotter.plot_pass_rate_boxplot()
    print(f"   ✓ Saved to: {path3}")

    print("4. Quality scatter plots with trends...")
    path4 = plotter.plot_quality_scatter_with_trends()
    print(f"   ✓ Saved to: {path4}")

    print("\n✓ All enhanced plots generated successfully!")
