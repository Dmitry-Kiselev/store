from rest_framework import viewsets

from order.models import Order, Discount
from .permissions import IsOwner
from .serializers import OrderSerializer, DiscountSerializer
from api.catalogue.permissions import IsStuffOrReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Order.objects.filter(basket__user=self.request.user)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsStuffOrReadOnly,)