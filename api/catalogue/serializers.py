from rest_framework import serializers

from catalogue.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ['name', 'product_category', 'description', 'price', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'image',]

