from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Wishlist
from carts.models import CartItem

# Create your views here.
def wishlist(request):
    if request.user.is_authenticated:
        prod = Product.objects.all()
        wishlist = Wishlist.objects.filter(user=request.user)
        return render(request,'orders/wishlist.html',{'wishlist':wishlist,'Product':prod})
    return render(request,'accounts/login.html')

def AddToWishlist(request,prod_id):
    user = request.user    
    product = Product.objects.get(id=prod_id)
    wishlist = Wishlist.objects.create(user=user,product=product)
    wishlist.save()   
    try:
        single_product = Product.objects.get(id = product.id)
        in_cart = CartItem.objects.filter(product=single_product).exists()
    except Exception as e:
        raise e

    
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        
    }
    
    return render(request,'store/product_detail.html',context)
def wishitems(request):
    wishlist_items =  Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})
       
# from .models import WishlistItem

def remove_from_wishlist(request, id):
    item = Wishlist.objects.get(id = id)
    item.delete()
    return redirect(wishitems)  
