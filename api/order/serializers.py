from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    basket = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='baskets-detail'
    )

    def save(self):
        super(OrderSerializer, self).save()

    class Meta:
        model = Order
        fields = '__all__'