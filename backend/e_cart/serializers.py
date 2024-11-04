from rest_framework import serializers
from .models import Item, Image, Review, Cart

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_path']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'date']

class ItemSerializer(serializers.ModelSerializer):
    first_image = ImageSerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField(method_name='get_first_image') 
    discount_price = serializers.SerializerMethodField(method_name = 'get_discount_price')
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'type','rating', 'price', 'reviews_count', 'discount', 'first_image' , 'discount_price'
        ]
    def get_first_image(self, obj):
        first_image = obj.images.first()  
        if first_image:
            return first_image.image_path
        return None
    
    def get_discount_price(self, obj):
        discount_price = obj.price - ((obj.discount/100)*obj.price)
        
        if discount_price:
            return discount_price
        return None



class SingleItemSerializer(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField(method_name = 'get_discount_price')
    images = ImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'type', 'price', 'description', 'features',
            'rating', 'reviews_count', 'discount', 'dimensions',
            'warranty', 'package_details', 'material', 'images', 'reviews' , "discount_price"
        ]
    def get_discount_price(self, obj):
        discount_price = obj.price - ((obj.discount/100)*obj.price)
        
        if discount_price:
            return discount_price
        return None

class CartSerializer(serializers.ModelSerializer):
    item = SingleItemSerializer(read_only=True) 
    class Meta:
            model = Cart
            fields = ['id', 'user', 'item', 'item_id', 'quantity', 'added_at']  


