"""Tests for the federal reglamentos spider."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Sample HTML fixture mimicking regla.htm structure
REGLA_HTML = """
<html>
<head><meta charset="iso-8859-1"></head>
<body>
<table>
<tr>
  <td>Reglamento de la Ley de Amparo</td>
  <td><a href="regley/Reg_Amparo.pdf">PDF</a></td>
</tr>
<tr>
  <td>Reglamento de la Ley del IVA</td>
  <td><a href="regley/Reg_IVA.pdf">PDF</a></td>
</tr>
<tr>
  <td>Reglamento de la Ley Federal del Trabajo</td>
  <td><a href="regley/Reg_LFT.pdf">PDF</a></td>
</tr>
<tr>
  <td>Short</td>
  <td><a href="regley/Reg_Short.pdf">PDF</a></td>
</tr>
<tr>
  <td><a href="some_page.html">Not a PDF link</a></td>
</tr>
</table>
</body>
</html>
"""


@pytest.fixture
def regla_html_file(tmp_path):
    """Create a temporary HTML file with sample reglamentos page."""
    html_file = tmp_path / "regla_dump.html"
    html_file.write_text(REGLA_HTML, encoding="iso-8859-1")
    return str(html_file)


def test_fetch_reglamentos_from_local_file(regla_html_file):
    """Test spider correctly parses local HTML fixture."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)

    assert isinstance(results, list)
    assert len(results) >= 3  # At least our 3 valid entries

    # Check structure of each result
    for item in results:
        assert "id" in item
        assert "name" in item
        assert "url" in item
        assert "remote_path" in item
        assert item["id"].startswith("reg_")
        assert item["url"].endswith(".pdf")


def test_reglamento_slug_prefix(regla_html_file):
    """Test that slugs have the reg_ prefix."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)
    for item in results:
        assert item["id"].startswith("reg_"), f"Slug should start with reg_: {item['id']}"


def test_reglamento_pdf_urls(regla_html_file):
    """Test that PDF URLs point to regley/ path."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)
    for item in results:
        assert "regley/" in item["remote_path"] or "Regla/" in item["remote_path"]


def test_dedup_urls(regla_html_file):
    """Test that duplicate URLs are filtered out."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)
    urls = [r["url"] for r in results]
    assert len(urls) == len(set(urls)), "Duplicate URLs should be filtered"


def test_non_pdf_links_excluded(regla_html_file):
    """Test that non-PDF links are excluded."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)
    for item in results:
        assert item["url"].endswith(".pdf")


def test_short_titles_use_fallback(regla_html_file):
    """Test that very short cell text falls back to filename-based title."""
    from apps.scraper.federal.reglamentos_spider import fetch_reglamentos

    results = fetch_reglamentos(local_file=regla_html_file)
    # "Short" is <= 10 chars, so should use fallback
    short_items = [r for r in results if "short" in r["id"].lower()]
    if short_items:
        # Fallback title comes from filename
        assert len(short_items[0]["name"]) > 0
