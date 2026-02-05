from unittest.mock import patch

import pytest

from apps.scraper.municipal.cdmx import CDMXScraper


class TestCDMXScraper:

    @pytest.fixture
    def scraper(self):
        return CDMXScraper()

    @patch("apps.scraper.municipal.cdmx.CDMXScraper.fetch_page")
    def test_scrape_finds_pdf(self, mock_fetch, scraper):
        mock_fetch.return_value = """
        <html>
            <table>
                <tr>
                    <td>
                        PUBLICADO EN LA GACETA...
                        LEY DE EDUCACIÓN DE LA CIUDAD DE MÉXICO
                        ULTIMA REFORMA...
                        <a href="/laws/educacion.pdf">Descargar</a>
                    </td>
                </tr>
            </table>
        </html>
        """

        results = scraper.scrape_catalog()
        assert len(results) == 1
        assert (
            "educacion" in results[0]["name"].lower()
            or "educación" in results[0]["name"].lower()
        )
        assert (
            results[0]["url"]
            == "https://data.consejeria.cdmx.gob.mx/laws/educacion.pdf"
        )
        assert results[0]["municipality"] == "Ciudad de México"

    @patch("apps.scraper.municipal.cdmx.CDMXScraper.fetch_page")
    def test_scrape_filename_fallback(self, mock_fetch, scraper):
        mock_fetch.return_value = """
        <html>
            <table>
                <tr>
                    <td>
                        Some random text
                        <a href="/laws/LEY_DE_MOVILIDAD_CDMX.pdf">Descargar</a>
                    </td>
                </tr>
            </table>
        </html>
        """

        results = scraper.scrape_catalog()
        assert len(results) == 1
        assert "MOVILIDAD" in results[0]["name"].upper()

    @patch("apps.scraper.municipal.cdmx.CDMXScraper.fetch_page")
    def test_scrape_resolves_relative_urls(self, mock_fetch, scraper):
        mock_fetch.return_value = """
        <html>
            <a href="images/leyes/2025/LEY_TEST.pdf">Link</a>
        </html>
        """
        results = scraper.scrape_catalog()
        assert len(results) == 1
        assert (
            results[0]["url"]
            == "https://data.consejeria.cdmx.gob.mx/images/leyes/2025/LEY_TEST.pdf"
        )
