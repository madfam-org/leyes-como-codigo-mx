from typing import List, Dict, Optional
from .base import MunicipalScraper
from bs4 import BeautifulSoup
import re
import urllib.parse
import os

class CDMXScraper(MunicipalScraper):
    def __init__(self):
        super().__init__("Ciudad de México", "https://data.consejeria.cdmx.gob.mx/index.php/leyes/leyes")
        # CDMX uses relative URLs often
        self.base_domain = "https://data.consejeria.cdmx.gob.mx"

    def scrape(self) -> List[Dict]:
        """
        Scrapes the CDMX laws portal for PDF links.
        Returns a list of dictionaries with metadata.
        """
        html = self.fetch_page(self.base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        laws = []
        
        # Find all PDF links
        pdf_links = soup.find_all('a', href=lambda href: href and href.lower().endswith('.pdf'))
        
        for a in pdf_links:
            href = a['href']
            # Resolve relative URL
            full_url = urllib.parse.urljoin(self.base_domain, href)
            
            # Extract Title from Row or Fallback to Filename
            row = a.find_parent('tr')
            title = None
            date_published = None
            
            if row:
                row_text = row.get_text(separator=' ', strip=True)
                # Heuristic: Find the substring starting with "LEY"
                # This regex looks for LEY followed by uppercase letters and spaces
                title_match = re.search(r'(LEY\s+(?:DE\s+|LA\s+|PARA\s+|DEL\s+|QUE\s+|[A-ZÁÉÍÓÚÑ"“”,])+(?:CDMX|MÉXICO|DISTRITO FEDERAL|DF|[A-ZÁÉÍÓÚÑ]+))', row_text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
            
            # Fallback 1: Previous Row (sometimes title is above)
            if not title and row:
                prev_row = row.find_previous_sibling('tr')
                if prev_row:
                    prev_text = prev_row.get_text(separator=' ', strip=True)
                    title_match = re.search(r'(LEY\s+(?:DE\s+|LA\s+|PARA\s+|DEL\s+|QUE\s+|[A-ZÁÉÍÓÚÑ"“”,])+(?:CDMX|MÉXICO|DISTRITO FEDERAL|DF|[A-ZÁÉÍÓÚÑ]+))', prev_text, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1).strip()

            # Fallback 2: Parse Filename
            if not title:
                filename = os.path.basename(urllib.parse.unquote(full_url))
                # Remove extension
                name_body = os.path.splitext(filename)[0]
                # Replace underscores and formatting
                clean_name = name_body.replace('_', ' ').replace('-', ' ')
                # If it looks like a law title (starts with LEY), use it
                if clean_name.upper().startswith('LEY'):
                    title = clean_name.upper()
                else:
                    title = clean_name # Better than nothing

            # Clean up title
            if title:
                # Remove extra spaces
                title = re.sub(r'\s+', ' ', title).strip()

            law_entry = {
                'title': title,
                'municipality': self.municipality,
                'file_url': full_url,
                'status': 'Discovered',
                'category': 'Municipal' # or State for CDMX
            }
            laws.append(law_entry)
            
        return laws

if __name__ == "__main__":
    # Test execution
    scraper = CDMXScraper()
    results = scraper.scrape()
    print(f"Found {len(results)} laws.")
    for l in results[:5]:
        print(l)
