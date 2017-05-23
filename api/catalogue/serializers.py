from rest_framework import serializers

from catalogue.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =  '__all__'

