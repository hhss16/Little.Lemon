from typing import Collection
from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem 
from .models import Category 

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock =  serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock', 'price_after_tax','category','category_id']
        extra_kwargs = {
            'price':{'min_value':1,'max_value':20},
            'stock':{'min_value':10}
        }

    
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)

