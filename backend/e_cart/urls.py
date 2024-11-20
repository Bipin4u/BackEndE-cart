from django.urls import path
from . import views

urlpatterns = [
    path('popular/', views.PopularItem),
    path('discount/', views.BestOffers),
    path('trending/', views.Trending),
    path('item/<int:id>/', views.SingleMenuItem,),
    path('category/<str:cat>/', views.FindByCategory),
    path('cart/', views.PostCart),
    path('getcart/', views.GetCart),
    path('wish-list/', views.AddWishList),
    path('review/<int:id>', views.ReviewItem),
    path('review/', views.ReviewAddItem),
    path('orders/', views.OrderItem),
    path('my-review/<int:id>', views.MyReview),
    path('update-review/<int:id>', views.UpdateMyReview),




]