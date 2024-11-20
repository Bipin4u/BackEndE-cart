from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Item(models.Model):
    TYPE_CHOICES = [
        ('sofa', 'Sofa'),
        ('recliner', 'Recliner'),
        ('dining', 'Dining'),
        ('bed', 'Bed'),
        ('office_study_table', 'Office & Study Table'),
        ('chair', 'Chair'),
        ('center_table', 'Center Table'),
        ('office_chair',"Office Chair")
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default='')
    features = models.JSONField(default=list)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])    
    reviews_count = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dimensions = models.CharField(max_length=255, default='')
    warranty = models.CharField(max_length=255, default='')
    package_details = models.CharField(max_length=255, default='')
    material = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

class Image(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image_path = models.URLField()  
    def __str__(self):
        return f'Image for {self.item.name}'

class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_review')
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    rating = models.FloatField()
    comment = models.TextField()
    date = models.DateField(default=timezone.now)
    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f'Review by {self.username} for {self.item.name}'
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_entries')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')  

    def __str__(self):
        return f"{self.quantity} of {self.item.name} for {self.user.username}"
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items') 
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlist_entries')  
    class Meta:
        unique_together = ('user', 'item') 

    def __str__(self):
        return f"{self.item.name} for {self.user.username}"
    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Order_items')  
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='Order_entries')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} for {self.user.username}"
