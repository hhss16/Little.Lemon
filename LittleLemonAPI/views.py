from django.shortcuts import  get_object_or_404
from rest_framework.response import Response 
from rest_framework.decorators import api_view, renderer_classes
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import status
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage

from rest_framework import viewsets
# from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework import pagination

@api_view(['GET','POST']) 
def menu_items(request): 
    if(request.method=='GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    elif request.method=='POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
    
@api_view() 
def single_item(request, id):
    # item = MenuItem.objects.get(pk=id)
    item = get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

class MenuItemFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    title = filters.CharFilter(field_name='title',lookup_expr='contains')
    class Meta:
        model = MenuItem
        fields = ['price', 'inventory', 'title']

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(data)
        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            # 'count': self.page.paginator.count,
            'results': data
        })

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['inventory','price', 'title']
    ordering_fields = ['price', 'inventory']
    # filterset_fields = ['price', 'inventory']
    # filterset_class = MenuItemFilter
    # pagination_class = CustomPagination

    # def list(self, request):
    #     qs = self.filter_queryset(qs)
    #     menu_items = MenuItem.objects.all()
    #     menu_filter = MenuItemFilter(request.GET,menu_items)
    #     menu_items_qs = menu_filter.qs
    #     paginator = Paginator(menu_items_qs,1)
    #     page = request.GET.get('page',1)
    #     items = paginator.page(page)
    #     serialized_item = MenuItemSerializer(items, many=True)
    #     return Response(serialized_item.data)

    # def get_queryset(self):
    #     return MenuItem.objects.all()