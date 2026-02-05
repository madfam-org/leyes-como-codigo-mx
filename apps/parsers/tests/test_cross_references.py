"""
Unit tests for cross-reference detection.
"""

import unittest

from apps.parsers.cross_references import CrossReferenceDetector, detect_references


class TestCrossReferenceDetector(unittest.TestCase):
    """Test suite for cross-reference detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = CrossReferenceDetector()

    def test_article_with_law_name(self):
        """Test detection of 'artículo X de la Ley...' pattern."""
        text = "según el artículo 5 de la Ley de Amparo"
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].article_num, "5")
        self.assertIn("Ley de Amparo", refs[0].law_name)
        self.assertGreater(refs[0].confidence, 0.5)

    def test_law_name_with_article(self):
        """Test detection of 'Ley..., artículo X' pattern."""
        text = "La Ley Federal de Telecomunicaciones, artículo 107"
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].article_num, "107")
        self.assertIn("Telecomunicaciones", refs[0].law_name)

    def test_fraction_reference(self):
        """Test detection of fraction references."""
        text = "conforme a la fracción III del artículo 27"
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].article_num, "27")
        self.assertEqual(refs[0].fraction, "III")

    def test_codigo_reference(self):
        """Test detection of Código references."""
        text = "El Código Civil Federal, artículo 1792 establece"
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 1)
        self.assertIn("Código Civil", refs[0].law_name)
        self.assertEqual(refs[0].article_num, "1792")

    def test_lettered_article(self):
        """Test detection of articles with letters (27-A)."""
        text = "de acuerdo al artículo 27-A de la Ley de Aguas"
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].article_num, "27-A")

    def test_multiple_references(self):
        """Test detection of multiple references in same text."""
        text = """
        El artículo 5 de la Ley de Amparo establece lo siguiente.
        Ver también la Ley Federal de Telecomunicaciones, artículo 107.
        """
        refs = self.detector.detect(text)

        self.assertEqual(len(refs), 2)
        self.assertEqual(refs[0].article_num, "5")
        self.assertEqual(refs[1].article_num, "107")

    def test_overlapping_patterns(self):
        """Test that overlapping matches are deduplicated."""
        text = "artículo 5 de la Ley de Amparo"
        refs = self.detector.detect(text)

        # Should only return one reference even if multiple patterns match
        self.assertEqual(len(refs), 1)

    def test_no_false_positives(self):
        """Test that non-references are not detected."""
        text = "El artículo habla sobre la ley en general sin especificar."
        refs = self.detector.detect(text)

        # Should not detect vague references
        self.assertEqual(len(refs), 0)

    def test_normalize_law_name(self):
        """Test law name normalization."""
        normalized = self.detector._normalize_law_name("Ley de Amparo, Reglamentaria")

        self.assertEqual(normalized, "ley de amparo, reglamentaria")

    def test_confidence_scoring(self):
        """Test that confidence scores are reasonable."""
        # High confidence: has both law name and article
        text1 = "artículo 5 de la Ley de Amparo"
        refs1 = self.detector.detect(text1)

        # Lower confidence: only law name
        text2 = "La Ley General de Salud"
        refs2 = self.detector.detect(text2)

        if refs1 and refs2:
            self.assertGreater(refs1[0].confidence, refs2[0].confidence)

    def test_convenience_function(self):
        """Test the convenience detect_references function."""
        text = "según el artículo 5 de la Ley de Amparo"
        refs = detect_references(text)

        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].article_num, "5")


if __name__ == "__main__":
    unittest.main()
