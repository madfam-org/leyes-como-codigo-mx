#!/usr/bin/env python3
"""
Extract metadata from state law text files.
Classifies laws by category, extracts publication dates, and enriches metadata.

Usage:
    # Process specific state
    python scripts/state_laws/extract_metadata.py --state colima
    
    # Process all states
    python scripts/state_laws/extract_metadata.py --all
"""

import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
import sys


# Category classification patterns
CATEGORY_PATTERNS = {
    'Civil': [
        r'c[oó]digo civil',
        r'procedimientos civiles',
        r'registro civil',
        r'derecho civil',
    ],
    'Penal': [
        r'c[oó]digo penal',
        r'procedimientos penales',
        r'derecho penal',
        r'ejecuci[oó]n de penas',
        r'sistema penitenciario',
    ],
    'Fiscal': [
        r'c[oó]digo fiscal',
        r'ley de hacienda',
        r'ley de ingresos',
        r'presupuesto',
        r'impuesto',
        r'contribuciones',
    ],
    'Electoral': [
        r'c[oó]digo electoral',
        r'ley electoral',
        r'partidos pol[ií]ticos',
        r'proceso electoral',
    ],
    'Laboral': [
        r'derecho del trabajo',
        r'ley del trabajo',
        r'trabajadores',
        r'servicio civil',
        r'burocracia',
    ],
    'Administrativo': [
        r'ley org[aá]nica',
        r'reglamento',
        r'administraci[oó]n p[uú]blica',
        r'procedimiento administrativo',
        r'transparencia',
        r'acceso a la informaci[oó]n',
    ],
    'Constitucional': [
        r'constituci[oó]n',
        r'reforma constitucional',
        r'derechos humanos',
        r'amparo',
    ],
}


def classify_law_category(law_name: str, text: str) -> str:
    """Classify law into a category based on name and content.
    
    Args:
        law_name: Name of the law
        text: Law text content
        
    Returns:
        Category name or 'Otros'
    """
    # Combine name and first 5000 chars for classification
    search_text = (law_name + ' ' + text[:5000]).lower()
    
    # Score each category
    scores = {}
    for category, patterns in CATEGORY_PATTERNS.items():
        score = sum(1 for pattern in patterns if re.search(pattern, search_text, re.IGNORECASE))
        scores[category] = score
    
    # Return category with highest score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    return 'Otros'


def extract_publication_date(text: str) -> Optional[str]:
    """Extract publication date from law text.
    
    Args:
        text: Law text content
        
    Returns:
        ISO format date string (YYYY-MM-DD) or None
    """
    # Common patterns for dates in Mexican legal documents
    date_patterns = [
        # "Publicado en el Periódico Oficial el 15 de marzo de 2023"
        r'publicado.*?(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
        # "Fecha: 15 de marzo de 2023"
        r'fecha:?\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
        # "15 de marzo de 2023"
        r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
    ]
    
    # Spanish months
    months = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }
    
    # Search first 10000 characters
    search_text = text[:10000].lower()
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, search_text, re.IGNORECASE)
        for match in matches:
            try:
                day = int(match.group(1))
                month_name = match.group(2).lower()
                year = int(match.group(3))
                
                # Validate
                if month_name not in months:
                    continue
                if day < 1 or day > 31:
                    continue
                if year < 1900 or year > 2030:
                    continue
                
                month = months[month_name]
                return f"{year}-{month}-{day:02d}"
                
            except (ValueError, IndexError):
                continue
    
    return None


def extract_state_from_path(file_path: Path) -> str:
    """Extract state name from file path.
    
    Args:
        file_path: Path to processed text file
        
    Returns:
        State name (capitalized)
    """
    # Path format: data/state_laws_processed/<state_name>/file.txt
    parts = file_path.parts
    if 'state_laws_processed' in parts:
        idx = parts.index('state_laws_processed')
        if idx + 1 < len(parts):
            state_name = parts[idx + 1]
            # Capitalize and clean
            return state_name.replace('_', ' ').title()
    
    return 'Unknown'


def process_law_file(txt_path: Path, original_metadata: Dict) -> Dict:
    """Process single law file and extract metadata.
    
    Args:
        txt_path: Path to .txt file
        original_metadata: Original metadata from scraping
        
    Returns:
        Enhanced metadata dictionary
    """
    try:
        # Read text
        text = txt_path.read_text(encoding='utf-8', errors='ignore')
        
        # Extract law name from original metadata or filename
        law_name = original_metadata.get('law_name', '')
        if not law_name:
            # Fallback to filename (without file_id)
            law_name = txt_path.stem.rsplit('_', 1)[0].replace('_', ' ').title()
        
        # Extract metadata
        category = classify_law_category(law_name, text)
        publication_date = extract_publication_date(text)
        state = extract_state_from_path(txt_path)
        
        # Create official_id (state_lawname)
        # Example: colima_codigo_civil
        official_id = f"{state.lower().replace(' ', '_')}_{txt_path.stem.rsplit('_', 1)[0]}"
        
        # Enhance metadata
        enhanced = {
            **original_metadata,  # Keep all original fields
            'official_id': official_id,
            'law_name': law_name,
            'category': category,
            'tier': 'state',  # All state laws
            'state': state,
            'jurisdiction': 'Estatal',
            'publication_date': publication_date,
            'text_file': str(txt_path),
            'char_count': len(text),
            'word_count': len(text.split()),
            'has_date': publication_date is not None,
        }
        
        return {
            'success': True,
            'official_id': official_id,
            'metadata': enhanced
        }
        
    except Exception as e:
        return {
            'success': False,
            'txt_path': str(txt_path),
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Extract metadata from state law text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true',
                      help='Process all state laws')
    group.add_argument('--state', type=str,
                      help='Process specific state (e.g., colima)')
    
    parser.add_argument('--output', type=str, default='data/state_laws_metadata.json',
                       help='Output JSON file')
    
    args = parser.parse_args()
    
    # Find text files
    if args.all:
        txt_files = list(Path('data/state_laws_processed').rglob('*.txt'))
        selection_desc = "all states"
    elif args.state:
        state_dir = Path('data/state_laws_processed') / args.state.lower().replace(' ', '_')
        if not state_dir.exists():
            print(f"❌ State directory not found: {state_dir}")
            return 1
        txt_files = list(state_dir.glob('*.txt'))
        selection_desc = f"state: {args.state}"
    else:
        print("Error: Must specify --all or --state")
        return 1
    
    if not txt_files:
        print(f"❌ No text files found for {selection_desc}")
        return 1
    
    # Load original metadata
    print("📚 Loading original metadata...")
    original_metadata_map = {}
    
    for metadata_file in Path('data/state_laws').rglob('*_metadata.json'):
        try:
            data = json.loads(metadata_file.read_text())
            for law in data.get('laws', []):
                file_id = law.get('file_id')
                if file_id:
                    original_metadata_map[str(file_id)] = law
        except Exception as e:
            print(f"⚠️  Warning: Could not load {metadata_file}: {e}")
    
    print(f"Loaded metadata for {len(original_metadata_map):,} laws")
    
    # Display plan
    print()
    print("=" * 70)
    print("METADATA EXTRACTION PLAN")
    print("=" * 70)
    print(f"Selection: {selection_desc}")
    print(f"Files to process: {len(txt_files):,}")
    print(f"Output: {args.output}")
    print("=" * 70)
    print()
    
    # Process files
    start_time = datetime.now()
    print("🚀 Starting metadata extraction...")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    for i, txt_file in enumerate(txt_files, 1):
        # Find original metadata by file_id in filename
        file_id = txt_file.stem.rsplit('_', 1)[-1]
        original = original_metadata_map.get(file_id, {})
        
        # Process
        result = process_law_file(txt_file, original)
        results.append(result)
        
        # Progress
        if i % 500 == 0:
            success_so_far = sum(1 for r in results if r['success'])
            print(f"  Processed: {i:,}/{len(txt_files):,} "
                  f"({success_so_far}/{i} successful)")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Analyze results
    success_count = sum(1 for r in results if r['success'])
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    # Category distribution
    category_counts = {}
    for r in successful:
        cat = r['metadata']['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Date extraction stats
    with_dates = sum(1 for r in successful if r['metadata']['has_date'])
    
    # Print summary
    print()
    print("=" * 70)
    print("METADATA EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Duration:       {duration:.1f}s ({duration/60:.1f} min)")
    print(f"Total files:    {len(results):,}")
    print(f"Success:        {success_count:,} ({success_count/len(results)*100:.1f}%)")
    print(f"Failed:         {len(failed):,}")
    print()
    print(f"With dates:     {with_dates:,} ({with_dates/success_count*100:.1f}%)")
    print()
    print("Category distribution:")
    for cat in sorted(category_counts.keys()):
        count = category_counts[cat]
        print(f"  {cat:20} {count:5,} ({count/success_count*100:5.1f}%)")
    
    print("=" * 70)
    
    # Save results
    output_data = {
        'timestamp': start_time.isoformat(),
        'duration_seconds': duration,
        'total_files': len(results),
        'success_count': success_count,
        'failed_count': len(failed),
        'with_dates_count': with_dates,
        'category_distribution': category_counts,
        'selection': selection_desc,
        'laws': [r['metadata'] for r in results if r['success']]
    }
    
    output_path = Path(args.output)
    output_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False))
    print(f"\n💾 Metadata saved to: {output_path}")
    print(f"   ({success_count:,} law records)")
    
    return 0 if len(failed) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
