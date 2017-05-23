from rest_framework import viewsets

from payment.models import Payment
from .permissions import IsStuff
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsStuff,)
