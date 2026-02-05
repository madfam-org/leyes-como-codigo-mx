"""
Database models for cross-references.
"""

from django.db import models


class CrossReference(models.Model):
    """
    Stores detected cross-references between articles and laws.

    Examples:
    - Article 5 in Law A references Article 107 in Law B
    - Article 27 references "Ley de Amparo" (general reference)
    """

    # Source (where the reference appears)
    source_law_slug = models.CharField(max_length=255, db_index=True)
    source_article_id = models.CharField(max_length=100, db_index=True)

    # Target (what is being referenced)
    target_law_slug = models.CharField(
        max_length=255, db_index=True, null=True, blank=True
    )
    target_article_num = models.CharField(max_length=100, null=True, blank=True)

    # Reference details
    reference_text = models.TextField(help_text="Original text of the reference")
    fraction = models.CharField(
        max_length=20, null=True, blank=True, help_text="Fraction number if specified"
    )
    confidence = models.FloatField(help_text="Detection confidence score (0-1)")

    # Position in source text
    start_position = models.IntegerField(help_text="Start position in article text")
    end_position = models.IntegerField(help_text="End position in article text")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cross_references"
        indexes = [
            models.Index(fields=["source_law_slug", "source_article_id"]),
            models.Index(fields=["target_law_slug", "target_article_num"]),
            models.Index(fields=["confidence"]),
        ]
        ordering = ["start_position"]

    def __str__(self):
        return (
            f"{self.source_law_slug}:{self.source_article_id} -> {self.reference_text}"
        )

    def target_url(self) -> str:
        """Generate URL for the target reference."""
        if not self.target_law_slug:
            return None

        url = f"/laws/{self.target_law_slug}"
        if self.target_article_num:
            url += f"#article-{self.target_article_num}"

        return url
