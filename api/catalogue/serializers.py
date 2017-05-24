from rest_framework import serializers

from catalogue.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.HyperlinkedRelatedField(
        view_name='api_root:category-detail', read_only=True, )

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(
        view_name='api_root:category-detail', read_only=True, )

    class Meta:
        model = Category
        fields = '__all__'
