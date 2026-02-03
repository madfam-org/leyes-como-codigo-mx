from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from engines.openfisca.system import MexicanTaxSystem
from .serializers import CalculationRequestSerializer, CalculationResultSerializer

class CalculationView(APIView):
    """
    Executes a tax calculation using the OpenFisca Engine.
    """
    
    def post(self, request):
        serializer = CalculationRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Initialize Engine
            system = MexicanTaxSystem()
            sim = system.new_simulation()
            
            # Map Inputs
            sim.add_person(
                name="citizen",
                period=data['period'],
                income_cash=data['income_cash'],
                income_goods=data['income_goods'],
                is_resident=data['is_resident'],
                has_mexican_income_source=data['has_mexican_income_source']
            )
            
            # Run Calculation
            # Note: In a real app we'd map output variables more dynamically
            gross_income = sim.calculate("gross_income", data['period'])
            isr_obligation = sim.calculate("isr_obligation", data['period'])
            
            result = {
                "gross_income": gross_income["citizen"],
                "isr_obligation": isr_obligation["citizen"]
            }
            
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
