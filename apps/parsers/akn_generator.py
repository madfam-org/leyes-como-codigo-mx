"""
Akoma Ntoso XML generator for Mexican federal laws.

Converts extracted text from legal documents into Akoma Ntoso 3.0 XML format.
"""

import re
from pathlib import Path
from datetime import date
from lxml import etree
from typing import List, Dict, Any


class AkomaNtosoGenerator:
    """
    Generates Akoma Ntoso XML from Mexican legal document text.
    """
    
    # Akoma Ntoso namespaces
    NS = {
        'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'
    }
    
    def __init__(self):
        self.nsmap = {None: self.NS['akn']}
    
    def create_frbr_metadata(
        self,
        law_type: str,
        date_str: str,
        slug: str,
        title: str
    ) -> Dict[str, Any]:
        """Create FRBR metadata for the law."""
        return {
            'work_uri': f"/mx/fed/{law_type}/{date_str}/{slug}/main",
            'expression_uri': f"/mx/fed/{law_type}/{date_str}/{slug}/spa@/main",
            'manifestation_uri': f"/mx/fed/{law_type}/{date_str}/{slug}/spa@/main.xml",
            'date': date_str,
            'title': title,
            'country': 'mx',
            'language': 'spa'
        }
    
    def parse_structure(self, text: str) -> List[Dict]:
        """
        Parse Mexican legal document structure.
        
        Returns list of structural elements with hierarchy.
        """
        elements = []
        current_title = None
        current_chapter = None
        
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Match TÍTULO
            if re.match(r'^TÍTULO\s+[IVX]+', line, re.IGNORECASE):
                current_title = line
                # Get title content (next line usually)
                if i + 1 < len(lines):
                    title_content = lines[i + 1].strip()
                    if title_content and not re.match(r'^CAP[ÍI]TULO', title_content):
                        current_title += f" - {title_content}"
                
                elements.append({
                    'type': 'title',
                    'id': f"titulo-{len([e for e in elements if e['type'] == 'title']) + 1}",
                    'number': line,
                    'content': current_title
                })
            
            # Match CAPÍTULO
            elif re.match(r'^CAP[ÍI]TULO\s+[IVX]+', line, re.IGNORECASE):
                current_chapter = line
                if i + 1 < len(lines):
                    chapter_content = lines[i + 1].strip()
                    if chapter_content and not re.match(r'^Artículo', chapter_content):
                        current_chapter += f" - {chapter_content}"
                
                elements.append({
                    'type': 'chapter',
                    'id': f"capitulo-{len([e for e in elements if e['type'] == 'chapter']) + 1}",
                    'number': line,
                    'content': current_chapter
                })
            
            # Match Artículo
            elif re.match(r'^Artículo\s+\d+[a-z]?\.?', line, re.IGNORECASE):
                # Extract article number
                art_match = re.match(r'^Artículo\s+(\d+[a-z]?)', line, re.IGNORECASE)
                if art_match:
                    art_num = art_match.group(1)
                    
                    # Collect content until next article
                    content_lines = [line]
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if re.match(r'^(Artículo|CAP[ÍI]TULO|TÍTULO|TRANSITORIO)', next_line, re.IGNORECASE):
                            break
                        if next_line:
                            content_lines.append(next_line)
                        j += 1
                    
                    elements.append({
                        'type': 'article',
                        'id': f"art-{art_num}",
                        'number': art_num,
                        'content': '\n'.join(content_lines),
                        'parent_title': current_title,
                        'parent_chapter': current_chapter
                    })
                    
                    i = j - 1  # Skip processed lines
            
            i += 1
        
        return elements
    
    def generate_xml(
        self,
        text: str,
        metadata: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Generate Akoma Ntoso XML from text.
        """
        # Parse structure
        elements = self.parse_structure(text)
        
        print(f"📊 Parsed {len(elements)} structural elements:")
        print(f"   - Titles: {len([e for e in elements if e['type'] == 'title'])}")
        print(f"   - Chapters: {len([e for e in elements if e['type'] == 'chapter'])}")
        print(f"   - Articles: {len([e for e in elements if e['type'] == 'article'])}")
        
        # Create XML structure
        root = etree.Element('akomaNtoso', nsmap=self.nsmap)
        act = etree.SubElement(root, 'act', name='law')
        
        # Meta section
        meta = etree.SubElement(act, 'meta')
        identification = etree.SubElement(meta, 'identification', source='#antigravity')
        
        # FRBR Work
        work = etree.SubElement(identification, 'FRBRWork')
        etree.SubElement(work, 'FRBRthis', value=metadata['work_uri'])
        etree.SubElement(work, 'FRBRuri', value=metadata['work_uri'].rsplit('/', 1)[0])
        etree.SubElement(work, 'FRBRdate', date=metadata['date'], name='Generation')
        etree.SubElement(work, 'FRBRauthor', href='#congress')
        etree.SubElement(work, 'FRBRcountry', value=metadata['country'])
        
        # FRBR Expression
        expression = etree.SubElement(identification, 'FRBRExpression')
        etree.SubElement(expression, 'FRBRthis', value=metadata['expression_uri'])
        etree.SubElement(expression, 'FRBRuri', value=metadata['expression_uri'].rsplit('/', 1)[0])
        etree.SubElement(expression, 'FRBRdate', date=metadata['date'], name='Generation')
        etree.SubElement(expression, 'FRBRauthor', href='#antigravity')
        etree.SubElement(expression, 'FRBRlanguage', language=metadata['language'])
        
        # FRBR Manifestation
        manifestation = etree.SubElement(identification, 'FRBRManifestation')
        etree.SubElement(manifestation, 'FRBRthis', value=metadata['manifestation_uri'])
        etree.SubElement(manifestation, 'FRBRuri', value=metadata['manifestation_uri'].replace('.xml', '.akn'))
        etree.SubElement(manifestation, 'FRBRdate', date=str(date.today()), name='Generation')
        etree.SubElement(manifestation, 'FRBRauthor', href='#antigravity')
        
        # Body
        body = etree.SubElement(act, 'body')
        
        # Build hierarchical structure
        current_title_elem = None
        current_chapter_elem = None
        
        for elem in elements:
            if elem['type'] == 'title':
                current_title_elem = etree.SubElement(body, 'title', id=elem['id'])
                num_elem = etree.SubElement(current_title_elem, 'num')
                num_elem.text = elem['number']
                current_chapter_elem = None
            
            elif elem['type'] == 'chapter':
                parent = current_title_elem if current_title_elem is not None else body
                current_chapter_elem = etree.SubElement(parent, 'chapter', id=elem['id'])
                num_elem = etree.SubElement(current_chapter_elem, 'num')
                num_elem.text = elem['number']
            
            elif elem['type'] == 'article':
                # Determine parent
                if current_chapter_elem is not None:
                    parent = current_chapter_elem
                elif current_title_elem is not None:
                    parent = current_title_elem
                else:
                    parent = body
                
                article_elem = etree.SubElement(parent, 'article', id=elem['id'])
                num_elem = etree.SubElement(article_elem, 'num')
                num_elem.text = f"Artículo {elem['number']}"
                
                # Content
                para = etree.SubElement(article_elem, 'paragraph', id=f"{elem['id']}-para-1")
                content = etree.SubElement(para, 'content')
                p = etree.SubElement(content, 'p')
                p.text = elem['content']
        
        # Write to file
        tree = etree.ElementTree(root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(
            str(output_path),
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )
        
        print(f"\n✅ Generated Akoma Ntoso XML: {output_path}")
        return output_path


def main():
    """Generate Akoma Ntoso XML for Ley de Amparo."""
    
    # Load extracted text
    text_file = Path("data/raw/ley_amparo_extracted.txt")
    if not text_file.exists():
        print(f"❌ Text file not found: {text_file}")
        print("   Run analyze_pdf.py first")
        return
    
    print("📖 Loading extracted text...")
    text = text_file.read_text(encoding='utf-8')
    
    # Create generator
    generator = AkomaNtosoGenerator()
    
    # Metadata
    metadata = generator.create_frbr_metadata(
        law_type='ley',
        date_str='2013-04-02',
        slug='amparo',
        title='Ley de Amparo, Reglamentaria de los Artículos 103 y 107 de la Constitución Política de los Estados Unidos Mexicanos'
    )
    
    # Generate XML
    output_path = Path("data/federal/mx-fed-amparo.xml")
    generator.generate_xml(text, metadata, output_path)
    
    print(f"\n🎉 Akoma Ntoso generation complete!")
    print(f"   Output: {output_path}")


if __name__ == "__main__":
    main()
