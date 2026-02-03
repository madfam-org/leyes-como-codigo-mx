from django.db import models

class Law(models.Model):
    OFFICIAL_ID_MAX_LENGTH = 50
    
    official_id = models.CharField(max_length=OFFICIAL_ID_MAX_LENGTH, unique=True, help_text="Slug identifier (e.g., 'cpeum')")
    name = models.CharField(max_length=500, help_text="Full name of the law")
    short_name = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tier = models.CharField(max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.official_id} - {self.short_name or self.name}"

class LawVersion(models.Model):
    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name='versions')
    publication_date = models.DateField(help_text="Date of publication in DOF")
    
    # Validity range
    valid_from = models.DateField(null=True, blank=True, help_text="Date this version became effective")
    valid_to = models.DateField(null=True, blank=True, help_text="Date this version was superseded (null if current)")
    
    # Content
    dof_url = models.URLField(max_length=500, blank=True, null=True)
    xml_file_path = models.CharField(max_length=500, blank=True, null=True)
    
    # Metadata
    change_summary = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['law', 'valid_from', 'valid_to']),
        ]

    def __str__(self):
        return f"{self.law.official_id} ({self.publication_date})"
