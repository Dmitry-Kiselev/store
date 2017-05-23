from rest_framework import serializers

from basket.models import Basket, Line


class BasketSerializer(serializers.ModelSerializer):
    lines = serializers.StringRelatedField(many=True)
    class Meta:
        model = Basket
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'
