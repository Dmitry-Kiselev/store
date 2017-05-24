from rest_framework import serializers

from order.models import Order, Discount


class OrderSerializer(serializers.ModelSerializer):
    basket = serializers.HyperlinkedRelatedField(
        view_name='api_root:basket-detail', read_only=True, )
    status = serializers.SerializerMethodField()
    discount = serializers.HyperlinkedRelatedField(
        view_name='api_root:discount-detail', read_only=True, )

    class Meta:
        model = Order
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status()


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'