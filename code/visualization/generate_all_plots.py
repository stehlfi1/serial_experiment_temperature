"""
Generate all visualization plots for similarity analysis.
Run this script to create all publication-ready figures.
"""

from data_loader import SimilarityDataLoader
from statistics import TemperatureStatistics
from temperature_plots import TemperaturePlotter


def main():
    print("="*60)
    print("Similarity Analysis Visualization Generator")
    print("="*60)
    print()

    # Load data
    print("Loading data...")
    loader = SimilarityDataLoader()
    df = loader.load_all_data()
    summary = loader.get_summary(df)

    print(f"✓ Loaded {summary['total_comparisons']} comparisons")
    print(f"  Models: {', '.join(summary['models'])}")
    print(f"  Challenges: {', '.join(summary['challenges'])}")
    print(f"  Temperatures: {summary['temperatures']}")
    print()

    # Calculate statistics
    print("Calculating statistics...")
    stats = TemperatureStatistics(df)
    print("✓ Statistics calculated")
    print()

    # Generate plots
    print("Generating plots...")
    plotter = TemperaturePlotter(df)

    plots_generated = []

    # 1. Combined 3-metric plot (all challenges combined)
    print("  1. Combined temperature effect (3 metrics)...")
    path = plotter.plot_temperature_effect_combined(
        metrics=['codebleu', 'ast_edit_distance', 'tsed']
    )
    plots_generated.append(path)

    # 2. Per-challenge plots for each primary metric
    for metric in ['codebleu', 'ast_edit_distance', 'tsed']:
        print(f"  2. {metric.upper()} by challenge...")
        path = plotter.plot_single_metric_per_challenge(metric)
        plots_generated.append(path)

    # 3. Consistency plots for primary metrics
    for metric in ['codebleu', 'ast_edit_distance', 'tsed']:
        print(f"  3. Consistency analysis for {metric.upper()}...")
        path = plotter.plot_consistency(metric)
        plots_generated.append(path)

    print()
    print("="*60)
    print(f"✅ Generated {len(plots_generated)} plots")
    print("="*60)
    print()
    print("Files saved to figures/similarity/:")
    for path in plots_generated:
        filename = path.split('/')[-1]
        print(f"  - {filename}")

    print()
    print("Plots are ready for LaTeX inclusion!")
    print()
    print("Example LaTeX usage:")
    print("  \\includegraphics[width=0.8\\textwidth]{figures/similarity/temperature_effect.pdf}")


if __name__ == "__main__":
    main()
