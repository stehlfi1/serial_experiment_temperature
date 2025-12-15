"""
Generate all LaTeX tables for similarity analysis.
Run this script to create all publication-ready tables.
"""

from data_loader import SimilarityDataLoader
from latex_export import LaTeXTableExporter


def main():
    print("="*60)
    print("Similarity Analysis LaTeX Table Generator")
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

    # Initialize exporter
    print("Generating LaTeX tables...")
    exporter = LaTeXTableExporter(df)

    tables_generated = []

    # 1. Temperature summary (all metrics)
    print("  1. Temperature summary table...")
    path = exporter.export_temperature_summary(
        metrics=['codebleu', 'ast_edit_distance', 'tsed']
    )
    tables_generated.append(path)

    # 2. Model comparison for each primary metric
    for metric in ['codebleu', 'ast_edit_distance', 'tsed']:
        print(f"  2. Model comparison for {metric.upper()}...")
        path = exporter.export_model_comparison(metric)
        tables_generated.append(path)

    # 3. Challenge breakdown for each primary metric
    for metric in ['codebleu', 'ast_edit_distance', 'tsed']:
        print(f"  3. Challenge breakdown for {metric.upper()}...")
        path = exporter.export_challenge_breakdown(metric)
        tables_generated.append(path)

    # 4. Consistency analysis
    print("  4. Consistency analysis table...")
    path = exporter.export_consistency_analysis(
        metrics=['codebleu', 'ast_edit_distance', 'tsed']
    )
    tables_generated.append(path)

    print()
    print("="*60)
    print(f"✅ Generated {len(tables_generated)} LaTeX tables")
    print("="*60)
    print()
    print("Files saved to tables/:")
    for path in tables_generated:
        filename = path.split('/')[-1]
        print(f"  - {filename}")

    print()
    print("Tables are ready for LaTeX inclusion!")
    print()
    print("Example LaTeX usage:")
    print("  \\input{tables/temperature_summary.tex}")
    print("  \\input{tables/model_comparison_codebleu.tex}")


if __name__ == "__main__":
    main()
