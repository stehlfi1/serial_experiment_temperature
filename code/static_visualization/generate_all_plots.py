"""
Generate all static analysis visualization plots.
Run this script to create all publication-ready figures.
"""

from data_loader import StaticAnalysisDataLoader
from quality_plots import QualityPlotter


def main():
    print("="*60)
    print("Static Analysis Visualization Generator")
    print("="*60)
    print()

    # Load filtered data for quality metrics
    print("Loading filtered data (for quality metrics)...")
    loader = StaticAnalysisDataLoader()
    df_filtered = loader.load_all_experiments(exclude_mode="all")
    summary = loader.get_summary(df_filtered)

    print(f"✓ Loaded {summary['total_results']} test results")
    print(f"  Models: {', '.join(summary['models'])}")
    print(f"  Challenges: {', '.join(summary['challenges'])}")
    print(f"  Temperatures: {summary['temperatures']}")
    print(f"  Avg compilation rate: {summary['compilation_rate']:.1%}")
    print(f"  Avg test pass rate: {summary['avg_pass_rate']:.1%}")
    print()

    # Load raw data for compilation graphs (no filtering!)
    print("Loading raw data (for compilation graphs)...")
    df_raw = loader.load_all_experiments(exclude_mode="none")
    print()

    # Generate plots
    print("Generating plots...")
    plots_generated = []

    # 1. Pass rate (using filtered data)
    print("  1. Test pass rate by temperature...")
    plotter = QualityPlotter(df_filtered)
    path = plotter.plot_pass_rate_by_temperature()
    plots_generated.append(path)

    # 2. Compilation rate comparison (using RAW data)
    print("  2. Compilation rate comparison (syntax vs pytest-compatible)...")
    plotter_raw = QualityPlotter(df_raw)
    path = plotter_raw.plot_compilation_rate_comparison()
    plots_generated.append(path)

    # 3. Complexity metrics
    print("  3. Complexity metrics (cyclomatic, cognitive)...")
    path = plotter.plot_complexity_metrics()
    plots_generated.append(path)

    # 4. Maintainability
    print("  4. Maintainability index by temperature...")
    path = plotter.plot_maintainability_by_temperature()
    plots_generated.append(path)

    # 5. Quality overview
    print("  5. Quality overview (4 metrics)...")
    path = plotter.plot_quality_overview()
    plots_generated.append(path)

    # 6. Per-challenge plots
    print("  6. Pass rate by challenge...")
    path = plotter.plot_by_challenge('pass_rate', 'Test Pass Rate')
    plots_generated.append(path)

    print("  7. Maintainability by challenge...")
    path = plotter.plot_by_challenge('maintainability_index', 'Maintainability Index')
    plots_generated.append(path)

    print()
    print("="*60)
    print(f"✅ Generated {len(plots_generated)} plots")
    print("="*60)
    print()
    print("Files saved to figures/static_analysis/:")
    for path in plots_generated:
        filename = path.split('/')[-1]
        print(f"  - {filename}")

    print()
    print("Plots are ready for LaTeX inclusion!")
    print()
    print("Example LaTeX usage:")
    print("  \\includegraphics[width=0.8\\textwidth]{figures/static_analysis/quality_overview.pdf}")


if __name__ == "__main__":
    main()
