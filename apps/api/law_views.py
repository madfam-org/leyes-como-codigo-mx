from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Law, LawVersion
from django.shortcuts import get_object_or_404

class LawDetailView(APIView):
    def get(self, request, law_id):
        # 1. Get Law
        law = get_object_or_404(Law, official_id=law_id)
        
        # 2. Get Versions
        versions = law.versions.all().order_by('-publication_date')
        
        # 3. Format Response
        data = {
            "id": law.official_id,
            "name": law.name,
            "short_name": law.short_name,
            "category": law.category,
            "tier": law.tier,
            "versions": [
                {
                    "publication_date": v.publication_date,
                    "valid_from": v.valid_from,
                    "dof_url": v.dof_url,
                    "xml_file": v.xml_file_path.split('/')[-1] if v.xml_file_path else None
                }
                for v in versions
            ],
             # Fallback stats for UI compatibility
            "articles": 0, # To be filled by ES count ideally
            "grade": "A",
            "score": 100
        }
        
        return Response(data)

class LawListView(APIView):
    def get(self, request):
        laws = Law.objects.all().order_by('official_id')
        data = [
            {
                "id": law.official_id,
                "name": law.short_name or law.name,
                "versions": law.versions.count()
            }
            for law in laws
        ]
        return Response(data)
