from pathlib import Path
from typing import Optional

from .similarity_storage import SimilarityStorage
from .data_exporter import CleanVizExporter


def run_similarity_analysis(input_dir: str = "dry_run_output", force_recompute: bool = False, 
                          export_viz: bool = False) -> None:
    """
    Run similarity analysis on generated code.
    
    Args:
        input_dir: Directory containing generated code
        force_recompute: Whether to recompute existing analyses
        export_viz: Whether to export visualization data
    """
    print(f"🔍 Running similarity analysis on: {input_dir}")
    print(f"🔄 Force recompute: {force_recompute}")
    print(f"📊 Export visualization: {export_viz}")
    print("-" * 50)
    
    try:
        # Initialize clean storage (ensure absolute path)
        if not Path(input_dir).is_absolute():
            input_dir = str(Path(__file__).parent.parent.parent / input_dir)
        storage = SimilarityStorage(input_dir)
        
        # Run batch analysis
        print("🚀 Starting clean similarity analysis...")
        results = storage.batch_analyze_all(force_recompute=force_recompute)
        
        # Report results
        files_created = len(results.get("files_created", []))
        files_skipped = len(results.get("files_skipped", []))
        error_count = len(results.get("errors", []))
        
        print(f"✅ Created {files_created} similarity data files")
        if files_skipped > 0:
            print(f"⏭️  Skipped {files_skipped} existing files (use --force-recompute to rebuild)")
        
        if files_created == 0 and files_skipped == 0 and error_count == 0:
            print("📭 No data to analyze - ensure generated code exists with multiple iterations")
        
        if error_count > 0:
            print(f"⚠️  {error_count} errors occurred:")
            for error in results["errors"][:3]:  # Show first 3 errors
                print(f"   - {error}")
            if error_count > 3:
                print(f"   ... and {error_count - 3} more errors")
        
        # Export visualization data if requested
        if export_viz:
            print("\\n📊 Exporting clean visualization data...")
            exporter = CleanVizExporter(input_dir)
            viz_results = exporter.export_all_visualizations()
            
            for viz_type, files in viz_results.items():
                if viz_type != "errors" and files:
                    print(f"   📈 {viz_type}: {len(files)} files")
            
            viz_errors = len(viz_results.get("errors", []))
            if viz_errors > 0:
                print(f"   ⚠️  {viz_errors} visualization export errors")
        
        print(f"\\n💾 Results stored in: {storage.similarity_dir}")
        print("🎉 Clean similarity analysis completed!")
        
    except Exception as e:
        print(f"❌ Error during similarity analysis: {str(e)}")
        raise