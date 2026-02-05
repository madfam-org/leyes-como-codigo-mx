from typing import List, Dict, Optional
from .base import MunicipalScraper

class MonterreyScraper(MunicipalScraper):
    def __init__(self):
        # Confirmed Transparency Microsite
        super().__init__("Monterrey", "https://www.monterrey.gob.mx/transparencia/")

    def scrape_catalog(self) -> List[Dict]:
        return [] # To be implemented once URL is verified

    def scrape_law_content(self, url: str) -> Optional[Dict]:
        return None
