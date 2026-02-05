from typing import List, Dict, Optional
from .base import MunicipalScraper
from bs4 import BeautifulSoup
import re

class GuadalajaraScraper(MunicipalScraper):
    def __init__(self):
        # Official Transparency Portal - Article 8 (General Regulations)
        # Dynamic portal, scraper needs to handle JS or specific sub-paths
        super().__init__("Guadalajara", "https://transparencia.guadalajara.gob.mx/")

    def scrape_catalog(self) -> List[Dict]:
        html = self.fetch_page(self.base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        laws = []
        
        # This selector is a guess based on standard lists, needs adjustment
        # Look for links that contain 'Reglamentos' or are inside a list
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            
            if "reglamento" in text.lower() or "reglamento" in href.lower():
                # Clean up URL
                if not href.startswith('http'):
                    href = self.base_url + href # Simplified join
                    
                laws.append({
                    'name': text,
                    'url': href,
                    'municipality': self.municipality,
                    'tier': 'municipal'
                })
                
        return laws

    def scrape_law_content(self, url: str) -> Optional[Dict]:
        # Most likely PDFs
        return {
            'url': url,
            'file_type': 'pdf' if url.lower().endswith('.pdf') else 'html'
        }
