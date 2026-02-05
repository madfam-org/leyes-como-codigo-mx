from rest_framework import serializers


class CalculationRequestSerializer(serializers.Serializer):
    period = serializers.CharField(max_length=7, help_text="YYYY-MM")
    income_cash = serializers.FloatField(required=False, default=0.0)
    income_goods = serializers.FloatField(required=False, default=0.0)
    is_resident = serializers.BooleanField(required=False, default=True)
    has_mexican_income_source = serializers.BooleanField(required=False, default=False)


class CalculationResultSerializer(serializers.Serializer):
    gross_income = serializers.FloatField()
    isr_obligation = serializers.BooleanField()
