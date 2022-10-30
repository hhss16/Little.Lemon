from django.shortcuts import  get_object_or_404
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

  

# Create your views here. 

@api_view() 
def menu_items(request): 
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
    return Response(serialized_item.data)

@api_view() 
def single_item(request, id):
    # item = MenuItem.objects.get(pk=id)
    item = get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)