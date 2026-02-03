#!/usr/bin/env python3
"""
Convert state law .doc files to plain text using textutil (Mac).
Processes in parallel with progress tracking.

Usage:
    # Test on single state
    python scripts/state_laws/convert_docs.py --state colima
    
    # Run on all states
    python scripts/state_laws/convert_docs.py --all
    
    # Control parallelism
    python scripts/state_laws/convert_docs.py --all --workers 12
"""

import subprocess
import argparse
import json
from pathlib import Path
from multiprocessing import Pool
from datetime import datetime
import sys


def convert_doc_to_text(doc_path: Path) -> dict:
    """Convert single .doc to .txt using textutil.
    
    Args:
        doc_path: Path to .doc file
        
    Returns:
        dict with conversion results
    """
    # Create output directory structure
    # Input: data/state_laws/colima/law_123.doc
    # Output: data/state_laws_processed/colima/law_123.txt
    
    relative_path = doc_path.relative_to(Path('data/state_laws'))
    txt_path = Path('data/state_laws_processed') / relative_path.with_suffix('.txt')
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Convert using textutil
        result = subprocess.run([
            'textutil',
            '-convert', 'txt',
            '-output', str(txt_path),
            str(doc_path)
        ], check=True, capture_output=True, timeout=30)
        
        # Read and get stats
        text = txt_path.read_text(encoding='utf-8', errors='ignore')
        
        # Basic validation
        if len(text.strip()) < 100:
            return {
                'success': False,
                'doc_path': str(doc_path),
                'txt_path': str(txt_path),
                'error': 'Text too short (likely empty document)'
            }
        
        return {
            'success': True,
            'doc_path': str(doc_path),
            'txt_path': str(txt_path),
            'char_count': len(text),
            'word_count': len(text.split())
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'doc_path': str(doc_path),
            'error': 'Conversion timeout (30s)'
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'doc_path': str(doc_path),
            'error': f'textutil error: {e.stderr.decode()}'
        }
    except Exception as e:
        return {
            'success': False,
            'doc_path': str(doc_path),
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Convert state law .doc files to text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true',
                      help='Process all state law .doc files')
    group.add_argument('--state', type=str,
                      help='Process specific state (e.g., colima)')
    
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of parallel workers (default: 8)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of files to process (for testing)')
    parser.add_argument('--output', type=str, default='data/conversion_results.json',
                       help='Output JSON file for results')
    
    args = parser.parse_args()
    
    # Find .doc files
    if args.all:
        doc_files = list(Path('data/state_laws').rglob('*.doc'))
        selection_desc = "all states"
    elif args.state:
        state_dir = Path('data/state_laws') / args.state.lower().replace(' ', '_')
        if not state_dir.exists():
            print(f"❌ State directory not found: {state_dir}")
            return 1
        doc_files = list(state_dir.glob('*.doc'))
        selection_desc = f"state: {args.state}"
    else:
        print("Error: Must specify --all or --state")
        return 1
    
    # Exclude metadata files
    doc_files = [f for f in doc_files if not f.name.endswith('_metadata.json')]
    
    if args.limit:
        doc_files = doc_files[:args.limit]
    
    if not doc_files:
        print(f"❌ No .doc files found for {selection_desc}")
        return 1
    
    # Display plan
    print("=" * 70)
    print("DOCUMENT CONVERSION PLAN")
    print("=" * 70)
    print(f"Selection: {selection_desc}")
    print(f"Files to convert: {len(doc_files):,}")
    print(f"Workers: {args.workers}")
    print(f"Output: {args.output}")
    print("=" * 70)
    print()
    
    # Create output directory
    Path('data/state_laws_processed').mkdir(exist_ok=True)
    
    # Process files
    start_time = datetime.now()
    print(f"🚀 Starting conversion...")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Use multiprocessing pool
    if args.workers > 1:
        with Pool(processes=args.workers) as pool:
            # Use imap for progress tracking
            results = []
            for i, result in enumerate(pool.imap(convert_doc_to_text, doc_files), 1):
                results.append(result)
                
                # Progress indicator every 100 files
                if i % 100 == 0:
                    success_so_far = sum(1 for r in results if r['success'])
                    print(f"  Processed: {i:,}/{len(doc_files):,} "
                          f"({success_so_far}/{i} successful)")
    else:
        # Single-threaded for debugging
        results = []
        for i, doc_file in enumerate(doc_files, 1):
            result = convert_doc_to_text(doc_file)
            results.append(result)
            
            if i % 100 == 0:
                success_so_far = sum(1 for r in results if r['success'])
                print(f"  Processed: {i:,}/{len(doc_files):,} "
                      f"({success_so_far}/{i} successful)")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Analyze results
    success_count = sum(1 for r in results if r['success'])
    failed = [r for r in results if not r['success']]
    
    # Calculate statistics
    total_chars = sum(r.get('char_count', 0) for r in results if r['success'])
    total_words = sum(r.get('word_count', 0) for r in results if r['success'])
    
    # Print summary
    print()
    print("=" * 70)
    print("CONVERSION SUMMARY")
    print("=" * 70)
    print(f"Start time:     {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time:       {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration:       {duration:.1f}s ({duration/60:.1f} min)")
    print(f"Total files:    {len(results):,}")
    print(f"Success:        {success_count:,} ({success_count/len(results)*100:.1f}%)")
    print(f"Failed:         {len(failed):,}")
    print(f"Avg time:       {duration/len(results):.2f}s per file")
    print()
    print(f"Total chars:    {total_chars:,}")
    print(f"Total words:    {total_words:,}")
    print(f"Avg per file:   {total_words/success_count if success_count > 0 else 0:.0f} words")
    
    # Failed files detail
    if failed and len(failed) <= 20:
        print(f"\n❌ Failed files ({len(failed)}):")
        for result in failed[:20]:
            doc_name = Path(result['doc_path']).name
            print(f"  • {doc_name}: {result['error']}")
    elif failed:
        print(f"\n❌ {len(failed)} files failed")
        print(f"   (First 20 errors saved to {args.output})")
    
    print("=" * 70)
    
    # Save results to JSON
    output_data = {
        'timestamp': start_time.isoformat(),
        'duration_seconds': duration,
        'total_files': len(results),
        'success_count': success_count,
        'failed_count': len(failed),
        'total_chars': total_chars,
        'total_words': total_words,
        'selection': selection_desc,
        'results': results
    }
    
    output_path = Path(args.output)
    output_path.write_text(json.dumps(output_data, indent=2))
    print(f"\n💾 Results saved to: {output_path}")
    
    # Return error code if any failures
    return 0 if len(failed) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
