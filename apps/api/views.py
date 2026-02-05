from elasticsearch import Elasticsearch
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Law

# from engines.openfisca.system import MexicanTaxSystem
from .serializers import CalculationRequestSerializer

# Elasticsearch config
ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "articles"


class CalculationView(APIView):
    def post(self, request):
        serializer = CalculationRequestSerializer(data=request.data)
        if serializer.is_valid():
            inputs = serializer.validated_data

            # Initialize System
            # system = MexicanTaxSystem()
            # sim = system.new_simulation()

            # ... (Calculation disabled for Stability)
            return Response(
                {
                    "message": "Calculation temporarily disabled due to missing engine dependencies",
                    "data": inputs,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .ingestion_manager import IngestionManager


class IngestionView(APIView):
    def post(self, request):
        params = request.data
        success, message = IngestionManager.start_ingestion(params)
        if success:
            return Response(
                {"status": "started", "message": message},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"status": "error", "message": message}, status=status.HTTP_409_CONFLICT
        )

    def get(self, request):
        status_data = IngestionManager.get_status()
        return Response(status_data)
