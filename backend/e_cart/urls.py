from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.PopularItem),
    path('item/<int:id>/', views.SingleMenuItem,),
    path('category/<str:cat>/', views.FindByCategory),
    path('cart/', views.GetCart),
]