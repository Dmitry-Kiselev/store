from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.HyperlinkedRelatedField(
        view_name='api_root:order-detail',
        read_only=True, )

    class Meta:
        model = Payment
        fields = '__all__'
