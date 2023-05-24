from django.urls import path
from .import views


urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('wishlist/',views.wishlist),
    path('AddToWishlist/<int:prod_id>/', views.AddToWishlist, name = "AddToWishlist"),
    path('wishlistitem/',views.wishitems),
    path('remove/<int:id>/',views.remove_from_wishlist),
    ]