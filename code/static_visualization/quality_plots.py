"""
Quality metrics visualization for static analysis.
Generates publication-ready plots for LaTeX documents.
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple

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


class QualityPlotter:
    """Generate quality metrics visualizations."""

    def __init__(self, df: pd.DataFrame, output_dir: str = "figures/static_analysis"):
        """
        Initialize plotter.

        Args:
            df: DataFrame from StaticAnalysisDataLoader
            output_dir: Directory to save figures
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_pass_rate_by_temperature(
        self,
        figsize: Tuple[float, float] = (8, 5)
    ) -> str:
        """
        Plot test pass rate across temperatures.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        # Filter to only rows with temperature data
        df_temp = self.df[self.df['temperature'].notna()].copy()

        fig, ax = plt.subplots(figsize=figsize)

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        for model in models:
            df_model = df_temp[df_temp['model'] == model]
            grouped = df_model.groupby('temperature')['pass_rate']
            means = grouped.mean()
            stds = grouped.std()

            ax.plot(temperatures, means, label=model.capitalize(),
                   color=COLORS.get(model, 'gray'), marker='o')
            ax.fill_between(temperatures,
                           means - stds,
                           means + stds,
                           alpha=0.2,
                           color=COLORS.get(model, 'gray'))

        ax.set_xlabel('Temperature')
        ax.set_ylabel('Test Pass Rate')
        ax.set_title('Functional Correctness vs Temperature')
        ax.set_ylim(0, 1.05)
        ax.legend()
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        filepath = self.output_dir / "pass_rate_by_temperature.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_compilation_rate_comparison(
        self,
        figsize: Tuple[float, float] = (12, 6)
    ) -> str:
        """
        Plot bar chart comparing error categories by temperature:
        1. Syntax Errors only (compilability failures)
        2. Syntax + Pattern A Errors (pytest-incompatible code)

        Shows absolute counts to avoid misleading percentages.

        IMPORTANT: This method requires RAW data (loaded with exclude_mode="none")
        to properly show error rates before filtering.

        Args:
            figsize: Figure size for plot

        Returns:
            Path to saved figure
        """
        from pathlib import Path
        import sys
        import numpy as np
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from utils.data_filtering import get_pattern_a_errors, get_non_compilable_iterations

        # Get errors
        pattern_a = get_pattern_a_errors()
        syntax_errors = get_non_compilable_iterations()

        df_temp = self.df[self.df['temperature'].notna()].copy()
        temperatures = sorted(df_temp['temperature'].unique())

        # Prepare data for stacked bar chart by temperature and model
        models = ['chatgpt', 'claude', 'gemini']

        # Structure: error_data[temp][error_type][model] = count
        error_data = {
            temp: {
                'syntax': {model: 0 for model in models},
                'combined': {model: 0 for model in models}
            } for temp in temperatures
        }
        total_per_temp = {temp: 0 for temp in temperatures}

        # Count total iterations per temperature
        for temp in temperatures:
            df_t = df_temp[df_temp['temperature'] == temp]
            total_per_temp[temp] = len(df_t)

        # Count syntax errors by model
        for model, challenge, temp, iteration in syntax_errors:
            if temp in error_data and model in models:
                error_data[temp]['syntax'][model] += 1

        # Count syntax + Pattern A errors by model
        all_errors = syntax_errors | pattern_a
        for model, challenge, temp, iteration in all_errors:
            if temp in error_data and model in models:
                error_data[temp]['combined'][model] += 1

        # Prepare data for stacked bars
        syntax_by_model = {model: [error_data[t]['syntax'][model] for t in temperatures] for model in models}
        combined_by_model = {model: [error_data[t]['combined'][model] for t in temperatures] for model in models}

        # Create bar chart with stacked bars
        fig, ax = plt.subplots(figsize=figsize)

        x = np.arange(len(temperatures))
        width = 0.35

        # Plot syntax errors (stacked by model)
        bottom_syntax = np.zeros(len(temperatures))
        bars_syntax = {}
        for model in models:
            bars_syntax[model] = ax.bar(
                x - width/2, syntax_by_model[model], width,
                bottom=bottom_syntax,
                label=f'{model.capitalize()} (Syntax)' if sum(syntax_by_model[model]) > 0 else '',
                color=COLORS.get(model, 'gray'),
                alpha=0.6,
                edgecolor='white',
                linewidth=1.5
            )
            bottom_syntax += np.array(syntax_by_model[model])

        # Plot combined errors (stacked by model)
        bottom_combined = np.zeros(len(temperatures))
        bars_combined = {}
        for model in models:
            bars_combined[model] = ax.bar(
                x + width/2, combined_by_model[model], width,
                bottom=bottom_combined,
                label=f'{model.capitalize()} (Combined)' if sum(combined_by_model[model]) > 0 else '',
                color=COLORS.get(model, 'gray'),
                alpha=0.9,
                edgecolor='white',
                linewidth=1.5
            )
            bottom_combined += np.array(combined_by_model[model])

        # Add total count labels on top of bars
        total_files = total_per_temp[temperatures[0]]  # Same for all temps
        for i, temp in enumerate(temperatures):
            # Syntax total
            syntax_total = sum(syntax_by_model[m][i] for m in models)
            if syntax_total > 0:
                ax.text(i - width/2, syntax_total + 0.1,
                       f'{int(syntax_total)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

            # Combined total
            combined_total = sum(combined_by_model[m][i] for m in models)
            if combined_total > 0:
                ax.text(i + width/2, combined_total + 0.1,
                       f'{int(combined_total)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Temperature', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Errors', fontsize=12, fontweight='bold')
        ax.set_title(f'Code Quality Issues by Temperature and Model\n(Total: {len(df_temp)} generated files)',
                    fontsize=13, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([f'{t:.1f}' for t in temperatures], fontsize=11)

        # Custom legend to show models clearly
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['chatgpt'], alpha=0.75, edgecolor='white', linewidth=1.5, label='ChatGPT'),
            Patch(facecolor=COLORS['claude'], alpha=0.75, edgecolor='white', linewidth=1.5, label='Claude'),
            Patch(facecolor=COLORS['gemini'], alpha=0.75, edgecolor='white', linewidth=1.5, label='Gemini'),
        ]
        legend1 = ax.legend(handles=legend_elements, loc='upper left', title='Model', fontsize=9)
        ax.add_artist(legend1)

        # Add second legend for bar types
        from matplotlib.lines import Line2D
        legend_elements2 = [
            Patch(facecolor='gray', alpha=0.6, label='Syntax Errors Only'),
            Patch(facecolor='gray', alpha=0.9, label='Syntax + Pattern A'),
        ]
        ax.legend(handles=legend_elements2, loc='upper right', title='Error Type', fontsize=9)

        # Set y-axis limit with some headroom
        max_count = max([sum(combined_by_model[m][i] for m in models) for i in range(len(temperatures))])
        ax.set_ylim(0, max_count * 1.4 if max_count > 0 else 5)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')

        # Add note with explanation
        note_text = (
            f"Na teplotu: {total_files} souborů (3 modely × 3 úlohy × 20 iterací)\n"
            "Rozšířené: kód se zkompiluje, ale selže při spuštění testů (import-time execution)\n"
            "Barvy ukazují, který LLM udělal chybu"
        )
        ax.text(0.5, 0.98, note_text,
               transform=ax.transAxes,
               fontsize=8,
               verticalalignment='top',
               horizontalalignment='center',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        plt.tight_layout()

        filepath = self.output_dir / "compilation_rate_comparison.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_complexity_metrics(
        self,
        figsize: Tuple[float, float] = (8, 10)
    ) -> str:
        """
        Plot complexity metrics (cyclomatic, cognitive) by temperature.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.df[self.df['temperature'].notna()].copy()

        fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        metrics = ['cyclomatic_complexity', 'cognitive_complexity']
        titles = ['Cyclomatic Complexity', 'Cognitive Complexity']

        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx]

            for model in models:
                df_model = df_temp[df_temp['model'] == model]

                # Filter out invalid values
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

            ax.set_ylabel(title)
            ax.grid(True, alpha=0.3, linestyle='--')

            if idx == 0:
                ax.legend()

        axes[-1].set_xlabel('Temperature')
        fig.suptitle('Code Complexity vs Temperature', fontsize=12, fontweight='bold')

        plt.tight_layout()

        filepath = self.output_dir / "complexity_by_temperature.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_maintainability_by_temperature(
        self,
        figsize: Tuple[float, float] = (8, 5)
    ) -> str:
        """
        Plot maintainability index across temperatures.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.df[self.df['temperature'].notna()].copy()

        fig, ax = plt.subplots(figsize=figsize)

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        for model in models:
            df_model = df_temp[df_temp['model'] == model]

            # Filter out invalid values
            df_model = df_model[np.isfinite(df_model['maintainability_index'])]

            grouped = df_model.groupby('temperature')['maintainability_index']
            means = grouped.mean()
            stds = grouped.std()

            ax.plot(temperatures, means, label=model.capitalize(),
                   color=COLORS.get(model, 'gray'), marker='o')
            ax.fill_between(temperatures,
                           means - stds,
                           means + stds,
                           alpha=0.2,
                           color=COLORS.get(model, 'gray'))

        ax.set_xlabel('Temperature')
        ax.set_ylabel('Maintainability Index')
        ax.set_title('Code Maintainability vs Temperature')
        ax.legend()
        ax.grid(True, alpha=0.3, linestyle='--')

        # Add quality threshold lines
        ax.axhline(y=20, color='red', linestyle='--', alpha=0.3, label='Poor')
        ax.axhline(y=50, color='orange', linestyle='--', alpha=0.3, label='Fair')
        ax.axhline(y=70, color='green', linestyle='--', alpha=0.3, label='Good')

        plt.tight_layout()

        filepath = self.output_dir / "maintainability_by_temperature.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_quality_overview(
        self,
        figsize: Tuple[float, float] = (12, 10)
    ) -> str:
        """
        Create overview plot with multiple quality metrics.

        Args:
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.df[self.df['temperature'].notna()].copy()

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()

        temperatures = sorted(df_temp['temperature'].unique())
        models = sorted(df_temp['model'].unique())

        # Define metrics to plot
        metrics = [
            ('pass_rate', 'Test Pass Rate', (0, 1.05)),
            ('maintainability_index', 'Maintainability Index', None),
            ('cyclomatic_complexity', 'Cyclomatic Complexity', None),
            ('halstead_difficulty', 'Halstead Difficulty', None),
        ]

        for idx, (metric, ylabel, ylim) in enumerate(metrics):
            ax = axes[idx]

            for model in models:
                df_model = df_temp[df_temp['model'] == model]

                # Filter out invalid values
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

            ax.set_xlabel('Temperature')
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3, linestyle='--')

            if ylim:
                ax.set_ylim(ylim)

            if idx == 0:
                ax.legend(loc='best')

        fig.suptitle('Code Quality Overview vs Temperature', fontsize=14, fontweight='bold')
        plt.tight_layout()

        filepath = self.output_dir / "quality_overview.pdf"
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)

    def plot_by_challenge(
        self,
        metric: str,
        ylabel: str,
        figsize: Tuple[float, float] = (12, 4)
    ) -> str:
        """
        Plot metric across challenges.

        Args:
            metric: Metric name
            ylabel: Y-axis label
            figsize: Figure size

        Returns:
            Path to saved figure
        """
        df_temp = self.df[self.df['temperature'].notna()].copy()

        challenges = sorted(df_temp['challenge'].unique())
        models = sorted(df_temp['model'].unique())
        temperatures = sorted(df_temp['temperature'].unique())

        fig, axes = plt.subplots(1, len(challenges), figsize=figsize, sharey=True)
        if len(challenges) == 1:
            axes = [axes]

        for idx, challenge in enumerate(challenges):
            ax = axes[idx]
            df_challenge = df_temp[df_temp['challenge'] == challenge]

            for model in models:
                df_model = df_challenge[df_challenge['model'] == model]

                # Filter out invalid values
                df_model = df_model[np.isfinite(df_model[metric])]

                grouped = df_model.groupby('temperature')[metric]
                means = grouped.mean()

                ax.plot(temperatures, means, label=model.capitalize(),
                       color=COLORS.get(model, 'gray'), marker='o')

            ax.set_title(challenge.replace('_', ' ').title())
            ax.set_xlabel('Temperature')
            ax.grid(True, alpha=0.3, linestyle='--')

            if idx == 0:
                ax.set_ylabel(ylabel)
            if idx == len(challenges) - 1:
                ax.legend(loc='best')

        plt.tight_layout()

        filename = f"{metric}_by_challenge.pdf"
        filepath = self.output_dir / filename
        plt.savefig(filepath, bbox_inches='tight', dpi=300)
        plt.close()

        return str(filepath)


if __name__ == "__main__":
    from data_loader import StaticAnalysisDataLoader

    # Test plotting
    loader = StaticAnalysisDataLoader()
    df = loader.load_all_experiments()
    plotter = QualityPlotter(df)

    print("Generating static analysis plots...")
    print()

    print("1. Pass rate by temperature...")
    path1 = plotter.plot_pass_rate_by_temperature()
    print(f"   Saved to: {path1}")

    print("2. Compilation rate by temperature...")
    path2 = plotter.plot_compilation_rate_by_temperature()
    print(f"   Saved to: {path2}")

    print("3. Complexity metrics...")
    path3 = plotter.plot_complexity_metrics()
    print(f"   Saved to: {path3}")

    print("4. Maintainability index...")
    path4 = plotter.plot_maintainability_by_temperature()
    print(f"   Saved to: {path4}")

    print("5. Quality overview...")
    path5 = plotter.plot_quality_overview()
    print(f"   Saved to: {path5}")

    print("\nDone!")
