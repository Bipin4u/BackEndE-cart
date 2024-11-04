from django.contrib import admin
from .models import *

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'rating', 'discount')  # Columns to display in the list view
    search_fields = ('name', 'type', 'description')  # Fields to search
    list_filter = ('type', 'rating', 'discount')  # Filters for the sidebar
    ordering = ('name',)  # Default ordering

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image_path')  # Columns to display in the list view
    search_fields = ('item__name', 'image_path')  # Fields to search
    list_filter = ('item',)  # Filters for the sidebar

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('item', 'username', 'rating', 'date')  # Columns to display in the list view
    search_fields = ('item__name', 'username', 'comment')  # Fields to search
    list_filter = ('rating', 'date')  # Filters for the sidebar
    ordering = ('-date',)  # Default ordering

admin.site.register(Cart)
