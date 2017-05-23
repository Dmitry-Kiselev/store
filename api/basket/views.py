from rest_framework import viewsets

from api.order.permissions import IsOwner
from basket.models import Basket, Line
from .serializers import BasketSerializer, LineSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return LineSerializer.objects.filter(user=self.request.user)
