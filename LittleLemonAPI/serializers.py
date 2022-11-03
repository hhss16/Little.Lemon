from typing import Collection
from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem
from .models import Category
import bleach

from rest_framework.validators import UniqueValidator

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory', min_value=10)
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        return attrs

    # def validate(self, data):
    #     price = data['price']
    #     if (price < 2):
    #         raise serializers.ValidationError('Minimum price is 2')
    #     return data
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock',
                  'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2, 'max_value': 20},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ]
            }
        }

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
