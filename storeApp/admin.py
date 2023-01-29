from django.contrib import admin
from .models import Address, Category, Product, Cart, Order


@admin.register(Category)
class CateogryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'created_at')
    list_editable = ('slug', 'is_active', 'is_featured',)
    list_filter = ('is_active', 'is_featured',)
    list_per_page = 10
    search_fields = ('title', 'description',)
    prepopulated_fields = {'slug':('title',)}
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'product_image', 'price', 'is_active', 'is_featured')
    list_editable = ('slug', 'price', 'is_active', 'is_featured',)
    list_filter = ('is_active', 'is_featured',)
    list_per_page = 10
    search_fields = ('title','category__recategory')
    prepopulated_fields = {'slug':('title',)}
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'product', 'quantity', 'total_price', 'ordered_date', 'status')
    list_editable = ('quantity', 'status',)
    list_filter = ('status', 'ordered_date',)
    list_per_page = 20
    search_fields = ('user', 'product',)
    
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state',)
    list_per_page = 10
    search_fields = ('locality', 'city', 'state',)
    