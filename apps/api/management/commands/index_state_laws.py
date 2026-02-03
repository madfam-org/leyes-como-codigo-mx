"""
Management command to index state laws in Elasticsearch.
Extracts articles from text and bulk indexes them.

Usage:
    # Index specific state
    docker-compose exec api python /app/manage.py index_state_laws --state colima
    
    # Index all states
    docker-compose exec api python /app/manage.py index_state_laws --all
    
    # Dry run
    docker-compose exec api python /app/manage.py index_state_laws --all --dry-run
"""

import re
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch, helpers
from apps.api.models import Law, LawVersion

# Elasticsearch config
ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "articles"


class Command(BaseCommand):
    help = 'Index state laws in Elasticsearch'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--all', action='store_true',
                          help='Index all state laws')
        group.add_argument('--state', type=str,
                          help='Index specific state')
        
        parser.add_argument('--dry-run', action='store_true',
                           help='Dry run (no Elasticsearch writes)')
        parser.add_argument('--batch-size', type=int, default=500,
                           help='Batch size for ES bulk indexing (default: 500)')
        parser.add_argument('--limit', type=int,
                           help='Limit number of laws to process (for testing)')

    def extract_articles(self, text, law_official_id):
        """Extract articles from law text.
        
        Returns list of article dictionaries.
        """
        articles = []
        
        # Patterns to detect article markers
        article_patterns = [
            r'ART[ÍI]CULO\s+(\d+)[\.°º\s-]',
            r'Art[ií]\.\s*(\d+)[\.°º\s-]',
            r'ARTÍCULO\s+(PRIMERO|SEGUNDO|TERCERO|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO)',
        ]
        
        # Try to split by articles
        combined_pattern = '|'.join(article_patterns)
        matches = list(re.finditer(combined_pattern, text, re.IGNORECASE))
        
        if len(matches) < 2:
            # No clear article structure, treat entire text as one article
            return [{
                'article_id': 'texto_completo',
                'text': text[:10000],  # Limit to 10K chars
                'has_structure': False
            }]
        
        # Extract articles
        for i, match in enumerate(matches):
            article_num = match.group(1) if match.group(1) else match.group(2)
            start_pos = match.start()
            
            # Get text until next article or end
            if i + 1 < len(matches):
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(text)
            
            article_text = text[start_pos:end_pos].strip()
            
            # Limit article text to 5000 chars for ES
            if len(article_text) > 5000:
                article_text = article_text[:5000] + "..."
            
            articles.append({
                'article_id': str(article_num),
                'text': article_text,
                'has_structure': True
            })
        
        return articles

    def index_law(self, law, dry_run=False):
        """Index a single law's articles into Elasticsearch.
        
        Returns list of ES documents to index.
        """
        try:
            # Get latest version
            version = law.versions.first()
            if not version:
                return {
                    'success': False,
                    'law_id': law.official_id,
                    'error': 'No version found'
                }
            
            # Read text file
            if not version.xml_file_path:
                return {
                    'success': False,
                    'law_id': law.official_id,
                    'error': 'No text file path'
                }
            
            text_file = Path('/app/' + version.xml_file_path)
            if not text_file.exists():
                return {
                    'success': False,
                    'law_id': law.official_id,
                    'error': f'Text file not found: {version.xml_file_path}'
                }
            
            text = text_file.read_text(encoding='utf-8', errors='ignore')
            
            # Extract articles
            articles = self.extract_articles(text, law.official_id)
            
            if dry_run:
                return {
                    'success': True,
                    'law_id': law.official_id,
                    'article_count': len(articles),
                    'action': 'dry_run'
                }
            
            # Create ES documents
            es_docs = []
            for article in articles:
                doc = {
                    '_index': INDEX_NAME,
                    '_source': {
                        'law_id': law.official_id,
                        'law_name': law.name,
                        'article': article['article_id'],
                        'text': article['text'],
                        'category': law.category,
                        'tier': law.tier,
                        'jurisdiction': 'Estatal',
                        'publication_date': version.publication_date.isoformat() if version.publication_date else None,
                        'tags': [law.tier, law.category.lower(), 'estatal'],
                        'has_structure': article['has_structure']
                    }
                }
                es_docs.append(doc)
            
            return {
                'success': True,
                'law_id': law.official_id,
                'article_count': len(articles),
                'es_docs': es_docs
            }
            
        except Exception as e:
            return {
                'success': False,
                'law_id': law.official_id,
                'error': str(e)
            }

    def handle(self, *args, **options):
        # Connect to Elasticsearch
        if not options['dry_run']:
            self.stdout.write("🔌 Connecting to Elasticsearch...")
            try:
                es = Elasticsearch([ES_HOST])
                if not es.ping():
                    self.stdout.write(self.style.ERROR("Cannot connect to Elasticsearch"))
                    return
                self.stdout.write(self.style.SUCCESS("✓ Connected to Elasticsearch"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Elasticsearch connection failed: {e}"))
                return
        
        # Get laws to process
        self.stdout.write("📚 Loading state laws from database...")
        
        if options['state']:
            state_name = options['state'].replace('_', ' ').title()
            # Filter by official_id prefix
            state_prefix = options['state'].lower().replace(' ', '_')
            laws = Law.objects.filter(
                tier='state',
                official_id__startswith=state_prefix
            ).prefetch_related('versions')
            selection_desc = f"state: {options['state']}"
        else:
            laws = Law.objects.filter(tier='state').prefetch_related('versions')
            selection_desc = "all states"
        
        if options['limit']:
            laws = laws[:options['limit']]
        
        law_list = list(laws)
        
        if not law_list:
            self.stdout.write(self.style.ERROR(f"No laws found for {selection_desc}"))
            return
        
        # Display plan
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("ELASTICSEARCH INDEXING PLAN")
        self.stdout.write("=" * 70)
        self.stdout.write(f"Selection: {selection_desc}")
        self.stdout.write(f"Laws to index: {len(law_list):,}")
        self.stdout.write(f"Batch size: {options['batch_size']}")
        self.stdout.write(f"Dry run: {options['dry_run']}")
        self.stdout.write("=" * 70)
        self.stdout.write("")
        
        # Process laws
        self.stdout.write("🚀 Starting Elasticsearch indexing...\n")
        
        results = []
        all_es_docs = []
        
        for i, law in enumerate(law_list, 1):
            result = self.index_law(law, options['dry_run'])
            results.append(result)
            
            if result['success'] and not options['dry_run']:
                all_es_docs.extend(result.get('es_docs', []))
            
            # Progress every 100 laws
            if i % 100 == 0:
                success_so_far = sum(1 for r in results if r['success'])
                self.stdout.write(f"  Processed: {i:,}/{len(law_list):,} "
                                f"({success_so_far}/{i} successful)")
        
        # Bulk index to Elasticsearch
        if not options['dry_run'] and all_es_docs:
            self.stdout.write(f"\n📤 Bulk indexing {len(all_es_docs):,} articles to Elasticsearch...")
            
            try:
                # Use bulk helper for efficient indexing
                success_count, errors = helpers.bulk(
                    es,
                    all_es_docs,
                    chunk_size=options['batch_size'],
                    raise_on_error=False
                )
                
                self.stdout.write(self.style.SUCCESS(f"✓ Indexed {success_count:,} articles"))
                
                if errors:
                    self.stdout.write(self.style.WARNING(f"⚠ {len(errors)} errors during indexing"))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Bulk indexing failed: {e}"))
        
        # Analyze results
        success_count = sum(1 for r in results if r['success'])
        failed = [r for r in results if not r['success']]
        total_articles = sum(r.get('article_count', 0) for r in results if r['success'])
        
        # Print summary
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("INDEXING SUMMARY")
        self.stdout.write("=" * 70)
        self.stdout.write(f"Total laws:     {len(results):,}")
        self.stdout.write(f"Success:        {success_count:,} ({success_count/len(results)*100:.1f}%)")
        self.stdout.write(f"Failed:         {len(failed):,}")
        self.stdout.write(f"Total articles: {total_articles:,}")
        self.stdout.write("")
        
        # Failed laws detail
        if failed and len(failed) <= 20:
            self.stdout.write(f"❌ Failed laws ({len(failed)}):")
            for result in failed[:20]:
                self.stdout.write(f"  • {result['law_id']}: {result['error']}")
        elif failed:
            self.stdout.write(f"❌ {len(failed)} laws failed")
        
        self.stdout.write("=" * 70)
        
        if not options['dry_run']:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Successfully indexed {total_articles:,} articles from {success_count:,} state laws!"
            ))
