from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Category Title')
    slug = models.SlugField(verbose_name='Category Slug')
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='categories', verbose_name='Category Image')
    is_active = models.BooleanField(verbose_name='Is Active')
    is_featured = models.BooleanField(verbose_name='Is Featured?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated Date')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)
        
    
    def __str__(self) -> str:
        return self.title
    


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Product Title')
    slug = models.SlugField(max_length=255, verbose_name='Product Slug')
    sku = models.CharField(max_length=255, unique=True, verbose_name='Unique Product ID (SKU)')
    short_description = models.TextField(verbose_name='Short Description')
    detail_description = models.TextField(verbose_name='Detail Description')
    product_image = models.ImageField(upload_to='products', verbose_name='Product Image')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Product Category')
    is_active = models.BooleanField(verbose_name='Is Active')
    is_featured = models.BooleanField(verbose_name='Is Featured?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated Date')
    
    
    class Meta:
        verbose_name_plural = 'Product'
        ordering = ('-created_at',)
        
    def __str__(self) -> str:
        return self.title
    
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cart User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Cart Product')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Updated Date')
        
    def __str__(self) -> str:
        return str(self.user)
    
    def get_cart_count(self):
        return Cart.objects.filter(user=self.user)
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    locality = models.CharField(max_length=255, verbose_name='Location')
    city = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255, verbose_name='State')
    
    def __str__(self) -> str:
        return self.locality
    
    
    
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Address')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    total_price = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='Total Price')
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name='Order Date')
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')
    
    
    