from .models import Cart, Category


def categories_menu(request):
    all_categories = Category.objects.filter(is_active=True)
    context = {'all_categories':all_categories}
    
    return context



def cart_count(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        print(cart_items)
        context = {'cart_items':cart_items}
        
    else:
        context = {}
    
    return context
    