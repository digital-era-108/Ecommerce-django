from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, Address, Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import decimal
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q



def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[0:4]
    data_product = Product.objects.filter(is_active=True,  is_featured=True)[0:4]
    context = {'products':data_product, 'categories':categories}
    return render(request, 'index.html', context)


def categories(request):
    categories_data = Category.objects.filter(is_active=True,  is_featured=True)
    context = {'categories':categories_data}
    return render(request, 'categories.html', context)



def product_detail(request, slug):
    one_product = Product.objects.get(slug=slug)
    related_products = Product.objects.exclude(id=one_product.id).filter(is_active=True, category=one_product.category)
    
    context = {'item':one_product, 'related_products':related_products}
    return render(request, 'product_detail.html', context)




@login_required(login_url='signin')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Check Whether the Product is Already in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
        
    else:
        Cart(user=user, product=product).save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


@login_required(login_url='signin')
def cart(request):
    user = request.user
    cart_product = Cart.objects.filter(user=user)
    
    amount = decimal.Decimal(0)
    shipping_charges = decimal.Decimal(100)
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
    
    # Customer Address
    address = Address.objects.filter(user=user)
    
    context = {
        'cart_products':cart_product,
        'amount':amount,
        'shipping_charges':shipping_charges,
        'address':address,
        'total':amount + shipping_charges,
    }
    
    return render(request, 'cart.html', context)


@login_required(login_url='signin')
def remove_cart(request, id):
    cd = Cart.objects.get(id=id)
    cd.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='signin')
def profile(request):
    orders = Order.objects.filter(user=request.user)
    user = User.objects.get(username=request.user)
    address = Address.objects.filter(user=request.user)
    context = {'user':user, 'useraddress':address, 'orders':orders}
    
    return render(request, 'profile.html', context)



@login_required(login_url='signin')
def address(request):
    
    if request.GET.get('q'):
        mycheck = request.GET.get('q')
        
        if mycheck:
            if request.method == 'POST':
                locality = request.POST['locality']
                city = request.POST['city']
                state = request.POST['state']
                
                get_address = Address(user=request.user, locality=locality, city=city, state=state)
                get_address.save()
                messages.success(request, 'Address has been Added.')
                return redirect('checkout')
    
    else:
        
        if request.method == 'POST':
                locality = request.POST['locality']
                city = request.POST['city']
                state = request.POST['state']
                
                get_address = Address(user=request.user, locality=locality, city=city, state=state)
                get_address.save()
                messages.success(request, 'Address has been Added.')
                return redirect('profile')
        
        
    return render(request, 'address.html')



def trash_address(request, id):
    del_address = Address.objects.get(id=id)
    del_address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def plus_cart(request, cart_id):
    cp = get_object_or_404(Cart, id=cart_id)
    cp.quantity += 1
    cp.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def minus_cart(request, cart_id):
    cp = get_object_or_404(Cart, id=cart_id)
    if cp.quantity == 1:
        cp.delete()
    else:
        cp.quantity -= 1
        cp.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='signin')
def checkout(request):

    if request.method == 'POST':
        try:
            radioAddress = request.POST['radioAddress']
            order_address = Address.objects.get(user=request.user, id=radioAddress)
    
            cart_items = Cart.objects.filter(user=request.user)
            for cart in cart_items:
                price = cart.quantity * cart.product.price
                orders = Order(user=request.user, address=order_address, product=cart.product, quantity=cart.quantity, total_price=price)
                orders.save()
                cart.delete()
            
            return redirect('orders')

        except Exception as error:
            print(error)
            messages.error(request, 'Add Shipping Address.')
    
    check_address = Address.objects.filter(user=request.user)
    total_cart_amount = Cart.objects.filter(user=request.user)
    total_amount = decimal.Decimal(0)
    shipping_charges = decimal.Decimal(100)
    for cart in total_cart_amount:
        carts = cart.quantity * cart.product.price
        total_amount += carts
        
    context = {
        'address':check_address, 
        'price_amount':total_amount,
        'shipping_charges':shipping_charges,
        'total_amount':total_amount + shipping_charges
        
        }
    
    return render(request, 'checkout.html', context)


@login_required(login_url='signin')
def orders(request):    
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    context = {'all_orders':all_orders}
    return render(request, 'orders.html', context)


# Categories

def category_product(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    
    context = {'products':products, 'category':category}
    
    return render(request, 'search.html', context)


def search(request):
    search_query = request.GET.get('q')
    
    if len(search_query) > 80:
        products = Product.objects.none()
        
    else:
        
        # product_title = Product.objects.filter(is_active=True, title__icontains=search_query)
        # product_category = Product.objects.filter(is_active=True, category__icontains=search_query)
        # product_short_desc = Product.objects.filter(is_active=True, short_description__icontains=search_query)
        # product_long_desc = Product.objects.filter(is_active=True, detail_description__icontains=search_query)
        # products = product_title.values_list().union(product_short_desc.values_list(), product_long_desc.values_list())
        
        
        products = Product.objects.filter(is_active=True, title__icontains=search_query)
    
    
    # if products.count() == 0:
    #     messages.warning(request, 'Query Not Found.')
    
    context = {'products':products, 'query':search_query}
    
    return render(request, 'search.html', context)