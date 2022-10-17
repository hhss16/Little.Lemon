from django.shortcuts import  get_object_or_404
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework import status
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from .throttles import GetAnononymousRateThrottle, FivePerMinuteThrottle
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute

# Create your views here. 

@api_view(['GET','POST']) 
def menu_items(request): 
    #return Response('list of books', status=status.HTTP_200_OK) 
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
            for ordering_field in ordering_fields:
                items = items.order_by(ordering_field)


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

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def roles(request):
    isdelivery = request.user.groups.filter(name='Delivery').exists()
    return Response(isdelivery)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager Should See This"})
    else:
        return Response({"message":"You are not authorized"}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})