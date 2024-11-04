from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from .models import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from.serializers import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage



#http://127.0.0.1:8000/api/items/?type=recliner
@api_view(['GET'])
def PopularItem(request):
    items = Item.objects.all()
    category_type = request.query_params.get('type',None)
    items = items.filter(type=category_type)
    items = items.order_by('-rating')[:6]
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def SingleMenuItem(request, id:int):
    print(f"Fetching item with ID: {id}")  # Debug line
    try:
        item = Item.objects.get(id=id)  # Use get() for a single item
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SingleItemSerializer(item)  # No need for `many=True`
    return Response(serializer.data)


#http://127.0.0.1:8000/api/category/recliner/?page=1&price_to=10000&sort=rating
@api_view(['GET'])
def FindByCategory(request,cat):
    items = Item.objects.filter(type=cat)
    page_number = request.query_params.get('page', 1) # Default to page 1
    price_to = request.query_params.get('price_to', None)
    sort = request.query_params.get('sort', None)

    if price_to:
        items = items.filter(price__lte=price_to)
    if sort:
        print(sort)
        items = items.order_by(sort)
    # items = items.filter(type=category_type)
    total_items = items.count()

    paginator = Paginator(items, 10)
    try:
        paginated_items = paginator.page(page_number)
    except EmptyPage:
        paginated_items = []
    serializer = ItemSerializer(paginated_items, many=True)
    response_data = {
        "items": serializer.data,
        "total_items": total_items,  # Total count of items
    }
    
    return Response(response_data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def GetCart(request):
    user = request.user 
    if request.method == 'GET':
            cart_items = Cart.objects.filter(user=user)  
            serializer = CartSerializer(cart_items, many=True)  
            return Response(serializer.data)
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the item already exists in the user's cart
            item = request.data.get('item')
            # existing_cart_item = Cart.objects.filter(user_id=user, item_id=item).first()

            # if existing_cart_item:
            #     # If item exists, update the quantity
            #     existing_cart_item.quantity += 1
            #     existing_cart_item.save()
            #     return Response(
            #         {"message": "Item quantity updated successfully."},
            #         status=status.HTTP_200_OK,
            #     )

            # # If the item doesn't exist, create a new cart entry
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)