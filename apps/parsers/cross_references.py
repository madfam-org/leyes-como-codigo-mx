"""
Cross-reference detection for Mexican legal documents.

Automatically detects references to other laws and articles within legal text,
enabling intelligent linking between related legal content.
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class LegalReference:
    """Represents a detected legal reference in text."""
    text: str  # Original matched text
    law_name: Optional[str]  # Extracted law name
    article_num: Optional[str]  # Article number
    fraction: Optional[str]  # Fraction (I, II, III, etc.)
    confidence: float  # 0-1 confidence score
    start_pos: int  # Start position in text
    end_pos: int  # End position in text


class CrossReferenceDetector:
    """
    Detects cross-references to other laws and articles in legal text.
    
    Example usage:
        detector = CrossReferenceDetector()
        refs = detector.detect("según el artículo 5 de la Ley de Amparo")
        # Returns: [LegalReference(text='artículo 5 de la Ley de Amparo', ...)]
    """
    
    # Regex patterns for different reference formats
    PATTERNS = [
        # "artículo 5 de la/el [Law Name]"
        (r'art[íi]culo\s+(\d+[A-Z]?(?:-[A-Z])?)\s+de\s+(?:la|el)\s+([Ll]ey\s+[^,\.\;]+|C[óo]digo\s+[^,\.\;]+|Reglamento\s+[^,\.\;]+)', 2.0),
        
        # "[Law Name], artículo 5"
        (r'([Ll]ey\s+[^,\.]{5,}|C[óo]digo\s+[^,\.]{5,}|Reglamento\s+[^,\.]{5,}),\s+art[íi]culo\s+(\d+[A-Z]?(?:-[A-Z])?)', 2.0),
        
        # "fracción III del artículo 107"
        (r'fracci[óo]n\s+([IVXLCDM]+)\s+del\s+art[íi]culo\s+(\d+[A-Z]?(?:-[A-Z])?)', 1.8),
        
        # "artículo 5, fracción III"
        (r'art[íi]culo\s+(\d+[A-Z]?(?:-[A-Z])?),\s+fracci[óo]n\s+([IVXLCDM]+)', 1.5),
        
        # Just law name (lower confidence)
        (r'([Ll]ey\s+(?:Federal|General|Org[áa]nica)\s+de\s+[^,\.\;]+)', 1.0),
        
        # Full formal references: "Ley Federal de..."
        (r'((?:[Ll]ey|C[óo]digo|Reglamento)\s+(?:Federal|General|Estatal|Municipal|Org[áa]nic[oa])\s+[^,\.\;]{10,})', 1.2),
    ]
    
    def __init__(self):
        """Initialize detector with compiled regex patterns."""
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE | re.MULTILINE), weight)
            for pattern, weight in self.PATTERNS
        ]
    
    def detect(self, text: str) -> List[LegalReference]:
        """
        Find all legal references in the given text.
        
        Args:
            text: The legal text to analyze
            
        Returns:
            List of LegalReference objects, sorted by position
        """
        references = []
        
        for pattern, weight in self.compiled_patterns:
            for match in pattern.finditer(text):
                ref = self._extract_reference(match, text, weight)
                if ref:
                    references.append(ref)
        
        # Deduplicate overlapping references
        return self._deduplicate(references)
    
    def _extract_reference(
        self, 
        match: re.Match, 
        text: str,
        pattern_weight: float
    ) -> Optional[LegalReference]:
        """Extract reference details from regex match."""
        groups = match.groups()
        if not groups:
            return None
        
        # Initialize fields
        law_name = None
        article_num = None
        fraction = None
        
        # Extract based on what we matched
        for group in groups:
            if not group:
                continue
                
            # Check if it's an article number (digits, possibly with letter)
            if re.match(r'^\d+[A-Z]?(?:-[A-Z])?$', group):
                article_num = group
            # Check if it's a fraction (Roman numerals)
            elif re.match(r'^[IVXLCDM]+$', group.upper()):
                fraction = group.upper()
            # Otherwise, it's likely a law name
            elif len(group) > 5:  # Avoid short strings
                law_name = group.strip()
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            law_name, article_num, fraction, pattern_weight
        )
        
        return LegalReference(
            text=match.group(0),
            law_name=law_name,
            article_num=article_num,
            fraction=fraction,
            confidence=confidence,
            start_pos=match.start(),
            end_pos=match.end()
        )
    
    def _calculate_confidence(
        self,
        law_name: Optional[str],
        article_num: Optional[str],
        fraction: Optional[str],
        pattern_weight: float
    ) -> float:
        """
        Calculate confidence score for a reference.
        
        Factors:
        - Pattern weight (different patterns have different reliability)
        - Presence of law name
        - Presence of article number
        - Length of law name (longer is more specific)
        """
        base_score = 0.0
        
        # Law name contributes most
        if law_name:
            base_score += 0.4
            # Bonus for longer, more specific names
            if len(law_name) > 20:
                base_score += 0.1
        
        # Article number is very specific
        if article_num:
            base_score += 0.4
        
        # Fraction adds detail
        if fraction:
            base_score += 0.1
        
        # Apply pattern weight
        weighted_score = base_score * (pattern_weight / 2.0)
        
        # Cap at 1.0
        return min(1.0, weighted_score)
    
    def _deduplicate(self, references: List[LegalReference]) -> List[LegalReference]:
        """
        Remove overlapping references, keeping highest confidence.
        
        When multiple patterns match the same text, we keep only the
        reference with the highest confidence score.
        """
        if not references:
            return []
        
        # Sort by position
        sorted_refs = sorted(references, key=lambda r: r.start_pos)
        
        result = [sorted_refs[0]]
        
        for ref in sorted_refs[1:]:
            last_ref = result[-1]
            
            # Check for overlap
            if ref.start_pos < last_ref.end_pos:
                # Overlaps - keep higher confidence
                if ref.confidence > last_ref.confidence:
                    result[-1] = ref
            else:
                # No overlap - keep both
                result.append(ref)
        
        return result
    
    def resolve_law_slug(self, law_name: str, law_slugs: Dict[str, str]) -> Optional[str]:
        """
        Resolve a law name to its slug using fuzzy matching.
        
        Args:
            law_name: The law name to resolve
            law_slugs: Dict mapping normalized names to slugs
            
        Returns:
            The matching slug, or None if no match found
        """
        if not law_name:
            return None
        
        # Normalize the law name
        normalized = self._normalize_law_name(law_name)
        
        # Try exact match first
        if normalized in law_slugs:
            return law_slugs[normalized]
        
        # Try partial matching
        for known_name, slug in law_slugs.items():
            # If either contains the other, it's a match
            if normalized in known_name or known_name in normalized:
                return slug
        
        return None
    
    def _normalize_law_name(self, name: str) -> str:
        """Normalize law name for matching."""
        # Lowercase
        normalized = name.lower()
        
        # Remove accents
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n'
        }
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        return normalized


# Convenience function for quick detection
def detect_references(text: str) -> List[LegalReference]:
    """
    Convenience function to detect references in text.
    
    Args:
        text: Legal text to analyze
        
    Returns:
        List of detected legal references
    """
    detector = CrossReferenceDetector()
    return detector.detect(text)
