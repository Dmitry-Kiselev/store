from catalogue.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .permissions import IsStuffOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsStuffOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStuffOrReadOnly,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product_list', request=request, format=format),
        'categories': reverse('category_list', request=request, format=format)
    })