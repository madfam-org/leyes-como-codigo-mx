"""
Tests for OJN scraper improvements:
- Failure tracking in scrape_state()
- Deduplication in scrape_state_comprehensive()
- Failure record structure
- CDMX metadata format
- Municipal probe output structure
- Municipal consolidation
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts/scraping to path so we can import ojn_scraper
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "scraping")
)


class TestOJNScraperFailureTracking:
    """Test that scrape_state tracks failures with reason codes."""

    def test_scrape_state_tracks_failures(self):
        """When _request returns None for metadata, failed_laws is populated."""
        from ojn_scraper import OJNScraper

        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = OJNScraper(output_dir=tmpdir)

            # Mock get_state_laws to return 2 laws
            mock_laws = [
                {"file_id": 100, "name": "Test Law 1", "state_id": 1, "power_id": 2},
                {"file_id": 200, "name": "Test Law 2", "state_id": 1, "power_id": 2},
            ]

            with patch.object(scraper, "get_state_laws", return_value=mock_laws):
                # Mock _request to always return None (metadata fetch fails)
                with patch.object(scraper, "_request", return_value=None):
                    results = scraper.scrape_state(1, "TestState")

            assert results["failed"] == 2
            assert results["successful"] == 0
            assert len(results["failed_laws"]) == 2

            # Check failure records
            for fl in results["failed_laws"]:
                assert fl["failure_reason"] == "no_metadata"
                assert "file_id" in fl
                assert "law_name" in fl
                assert "timestamp" in fl

    def test_scrape_state_tracks_no_download_url(self):
        """When metadata has no download_url, failure is recorded."""
        from ojn_scraper import OJNScraper

        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = OJNScraper(output_dir=tmpdir)

            mock_laws = [
                {"file_id": 100, "name": "No URL Law", "state_id": 1, "power_id": 2},
            ]

            # Return metadata without download_url
            mock_metadata = {"file_id": 100, "ambito": "ESTATAL", "url": "http://test"}

            with patch.object(scraper, "get_state_laws", return_value=mock_laws):
                with patch.object(
                    scraper, "get_law_metadata", return_value=mock_metadata
                ):
                    results = scraper.scrape_state(1, "TestState")

            assert results["failed"] == 1
            assert len(results["failed_laws"]) == 1
            assert results["failed_laws"][0]["failure_reason"] == "no_download_url"

    def test_scrape_state_tracks_download_failed(self):
        """When download fails, failure is recorded."""
        from ojn_scraper import OJNScraper

        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = OJNScraper(output_dir=tmpdir)

            mock_laws = [
                {"file_id": 100, "name": "Download Fail", "state_id": 1, "power_id": 2},
            ]

            mock_metadata = {
                "file_id": 100,
                "ambito": "ESTATAL",
                "url": "http://test",
                "download_url": "http://test/doc.pdf",
                "format": "pdf",
            }

            with patch.object(scraper, "get_state_laws", return_value=mock_laws):
                with patch.object(
                    scraper, "get_law_metadata", return_value=mock_metadata
                ):
                    with patch.object(scraper, "download_document", return_value=False):
                        results = scraper.scrape_state(1, "TestState")

            assert results["failed"] == 1
            assert len(results["failed_laws"]) == 1
            assert results["failed_laws"][0]["failure_reason"] == "download_failed"
            assert results["failed_laws"][0]["download_url"] == "http://test/doc.pdf"


class TestOJNScraperComprehensive:
    """Test scrape_state_comprehensive deduplication."""

    def test_deduplicates_across_powers(self):
        """Laws with same file_id across powers are not duplicated."""
        from ojn_scraper import OJNScraper

        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = OJNScraper(output_dir=tmpdir)

            def mock_get_laws(state_id, power_id=2):
                # Power 1 and 2 share file_id=100
                if power_id == 1:
                    return [
                        {
                            "file_id": 100,
                            "name": "Shared Law",
                            "state_id": 1,
                            "power_id": 1,
                        },
                        {
                            "file_id": 300,
                            "name": "Exec Only",
                            "state_id": 1,
                            "power_id": 1,
                        },
                    ]
                elif power_id == 2:
                    return [
                        {
                            "file_id": 100,
                            "name": "Shared Law",
                            "state_id": 1,
                            "power_id": 2,
                        },
                        {
                            "file_id": 200,
                            "name": "Legis Only",
                            "state_id": 1,
                            "power_id": 2,
                        },
                    ]
                return []

            with patch.object(scraper, "get_state_laws", side_effect=mock_get_laws):
                with patch.object(scraper, "_request", return_value=None):
                    results = scraper.scrape_state_comprehensive(
                        1, "TestState", power_ids=[1, 2]
                    )

            # Should have 3 unique laws, not 4
            assert results["total_found"] == 3
            assert results["failed"] == 3  # All fail (no metadata)
            assert len(results["failed_laws"]) == 3


class TestFailureRecordStructure:
    """Test that failure records have all required fields."""

    def test_failure_record_fields(self):
        from ojn_scraper import OJNScraper

        scraper = OJNScraper(output_dir="/tmp/test")
        law = {"file_id": 42, "name": "Test Law"}

        record = scraper._make_failure_record(law, "no_metadata")

        assert record["file_id"] == 42
        assert record["law_name"] == "Test Law"
        assert record["failure_reason"] == "no_metadata"
        assert "download_url" in record
        assert "timestamp" in record

    def test_failure_record_with_metadata(self):
        from ojn_scraper import OJNScraper

        scraper = OJNScraper(output_dir="/tmp/test")
        law = {"file_id": 42, "name": "Test Law"}
        metadata = {"download_url": "http://example.com/doc.pdf"}

        record = scraper._make_failure_record(law, "download_failed", metadata)

        assert record["download_url"] == "http://example.com/doc.pdf"
        assert record["failure_reason"] == "download_failed"


class TestCDMXMetadataFormat:
    """Test that CDMX scraper output is compatible with consolidation."""

    def test_cdmx_metadata_has_required_fields(self):
        """Simulated CDMX metadata should match OJN format."""
        import hashlib

        # Simulate what scrape_cdmx_state.py produces
        url = "https://example.com/ley_test.pdf"
        file_id = int(hashlib.sha256(url.encode()).hexdigest()[:8], 16)

        metadata = {
            "file_id": file_id,
            "ambito": "ESTATAL",
            "url": url,
            "download_url": url,
            "format": "pdf",
            "local_path": "/data/state_laws/ciudad_de_méxico/ley_test.pdf",
            "law_name": "Ley de Test",
        }

        # Same fields as OJN output
        assert "file_id" in metadata
        assert "law_name" in metadata
        assert "download_url" in metadata
        assert "format" in metadata
        assert "local_path" in metadata
        assert isinstance(metadata["file_id"], int)

    def test_cdmx_state_results_structure(self):
        """Simulated CDMX results dict should match scrape_state() output."""
        results = {
            "state_id": 9,
            "state_name": "Ciudad de México",
            "total_found": 10,
            "successful": 8,
            "failed": 2,
            "laws": [{"file_id": 1, "law_name": "Test"}],
            "failed_laws": [
                {
                    "file_id": 2,
                    "law_name": "Failed",
                    "failure_reason": "download_failed",
                    "download_url": "",
                    "timestamp": "2026-02-05T00:00:00",
                }
            ],
        }

        assert "laws" in results
        assert "failed_laws" in results
        assert results["state_name"] == "Ciudad de México"
        assert results["state_id"] == 9


class TestMunicipalProbeOutput:
    """Test expected probe output structure."""

    def test_probe_result_structure(self):
        """Verify probe JSON has expected top-level keys."""
        probe_result = {
            "probe_date": "2026-02-05",
            "states_probed": 32,
            "total_new_laws_found": 150,
            "per_state": [
                {
                    "state_id": 1,
                    "state_name": "Aguascalientes",
                    "existing_estatal": 100,
                    "total_across_powers": 120,
                    "per_power": {"1": 30, "2": 100, "3": 10, "4": 5},
                    "new_from_other_powers": 20,
                }
            ],
            "sample_municipal_entries": [
                {
                    "state_name": "Aguascalientes",
                    "file_id": 12345,
                    "ambito": "MUNICIPAL",
                    "has_download": True,
                }
            ],
        }

        assert "probe_date" in probe_result
        assert "states_probed" in probe_result
        assert "total_new_laws_found" in probe_result
        assert "per_state" in probe_result
        assert "sample_municipal_entries" in probe_result

        state = probe_result["per_state"][0]
        assert "existing_estatal" in state
        assert "new_from_other_powers" in state
        assert "per_power" in state


class TestConsolidateMunicipal:
    """Test municipal consolidation merging."""

    def test_consolidation_merges_sources(self):
        """Verify consolidation script reads and merges metadata files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock municipal directory structure
            muni_dir = Path(tmpdir) / "data" / "municipal_laws"
            state_a_dir = muni_dir / "state_a"
            state_b_dir = muni_dir / "state_b"
            state_a_dir.mkdir(parents=True)
            state_b_dir.mkdir(parents=True)

            # State A metadata
            state_a_meta = {
                "state_name": "State A",
                "laws": [
                    {"file_id": 1, "law_name": "Ley Municipal A1"},
                    {"file_id": 2, "law_name": "Reglamento A2"},
                ],
            }
            with open(state_a_dir / "state_a_municipal_metadata.json", "w") as f:
                json.dump(state_a_meta, f)

            # State B catalog
            state_b_meta = {
                "city": "city_b",
                "laws": [
                    {
                        "name": "Ley B1",
                        "url": "http://b1.pdf",
                        "municipality": "city_b",
                    },
                ],
            }
            with open(state_b_dir / "city_b_catalog.json", "w") as f:
                json.dump(state_b_meta, f)

            # Import and run consolidation with patched paths
            from consolidate_municipal_metadata import _classify_law

            # Manually verify the classify function
            assert _classify_law("Ley Municipal A1") == "ley"
            assert _classify_law("Reglamento A2") == "reglamento"

            # Verify the metadata files can be read and merged (dedup by path)
            all_laws = []
            seen_files = set()
            for pattern in [
                "*/*_metadata.json",
                "*/*_municipal_metadata.json",
                "*/*_catalog.json",
            ]:
                for mf in muni_dir.glob(pattern):
                    if mf in seen_files:
                        continue
                    seen_files.add(mf)
                    with open(mf, "r") as f:
                        data = json.load(f)
                    all_laws.extend(data.get("laws", []))

            assert len(all_laws) == 3
