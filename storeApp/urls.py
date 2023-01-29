from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all-categories/', views.categories, name='categories'),
    path('product-detail/<slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-cart/<id>/', views.remove_cart, name='remove_cart'),
    path('plus-cart/<int:cart_id>', views.plus_cart, name='plus_cart'),
    path('minus-cart/<int:cart_id>', views.minus_cart, name='minus_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    
    # Categories
    path('category-product/<slug>/', views.category_product, name='category_product'),
    path('search/', views.search, name='search'),
    
    
    # Profile
    path('profile/', views.profile, name="profile"),
    path('address/', views.address, name="address"),
    path('address/<id>/', views.trash_address, name="trash_address"),
    
]