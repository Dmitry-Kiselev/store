from order.models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets
from .permissions import IsOwner


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Order.objects.filter(basket__user=self.request.user)
