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
def BestOffers(request):
    items = Item.objects.all()
    category_type = request.query_params.get('type',None)
    items = items.filter(type=category_type)
    items = items.order_by('-discount')[:6]
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def Trending(request):
    items = Item.objects.all()
    category_type = request.query_params.get('type',None)
    items = items.filter(type=category_type)
    items = items.order_by('-reviews_count')[:6]
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PostCart(request):
    user = request.user  # Get the authenticated user
    item_id = request.data.get('item')  # Get the item from the request data

    if not item_id:
        return Response({"error": "Item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the item already exists in the user's cart
    existing_cart_item = Cart.objects.filter(user=user, item_id=item_id).first()
    type = request.query_params.get('type')
    
    if existing_cart_item:
        # If item exists, update the quantity
        if type=='increment':
            existing_cart_item.quantity += 1 
            existing_cart_item.save() 
        elif(type=='decrement'):
            existing_cart_item.quantity -= 1 
            existing_cart_item.save()
        else:
            existing_cart_item.delete()        
        return Response(
            {"message": "Item quantity updated successfully."},
            status=status.HTTP_200_OK,
        )
    # If the item doesn't exist, create a new cart entry
    data = request.data.copy()
    data['user'] = user.id  # Ensure user is included
    serializer = CartSerializer(data=data)

    if serializer.is_valid():
        print(data)
        serializer.save(user=user)
        print(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetCart(request):
        # Get the authenticated user's cart items
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # Serialize the cart items
        serializer = GetCartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def AddWishList(request):
    user = request.user 
    item_id = request.data.get('item')  

    print("user",user) 
    if (request.method == 'GET'):
        user = request.user
        cart_items = WishList.objects.filter(user=user)
        serializer = WishListSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Ensure the item is provided in the request data
        if 'item' not in request.data:
            return Response({"error": "Item field is required"}, status=status.HTTP_400_BAD_REQUEST)
        


        existing_cart_item = WishList.objects.filter(user=user, item_id=item_id).first()        
        if existing_cart_item:
            existing_cart_item.delete()        
            return Response(
                {"message": "Item quantity updated successfully."},
                status=status.HTTP_200_OK,)


        # Copy data and set the user
        data = request.data.copy()
        data['user'] = user.id  # Set the user to the authenticated user

        # Serialize and validate the data
        serializer = SetWishListSerializer(data=data)
        print(data)
        if serializer.is_valid():
            print(user)
            serializer.save(user=user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




