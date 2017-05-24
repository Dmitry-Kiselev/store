from rest_framework import serializers

from basket.models import Basket, Line


class BasketSerializer(serializers.ModelSerializer):
    lines = serializers.HyperlinkedRelatedField(
        view_name='api_root:line-detail', read_only=True, many=True)
    user = serializers.HyperlinkedRelatedField(
        view_name='api_root:user-detail', read_only=True)

    class Meta:
        model = Basket
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    basket = serializers.HyperlinkedRelatedField(
        view_name='api_root:basket-detail', read_only=True, )
    product = serializers.HyperlinkedRelatedField(
        view_name='api_root:product-detail', read_only=True, )

    class Meta:
        model = Line
        fields = '__all__'
