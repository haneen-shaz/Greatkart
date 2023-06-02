from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from accounts.models import Account
from store.models import Product
from category.models import category
from orders.models import Order,OrderProduct
from django.views.decorators.cache import never_cache
from django.template.defaultfilters import slugify

# Create your views here.
@never_cache
def admins_log(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    return render(request, 'accounts/admins_login.html')

@never_cache
def admin_home(request):
    if request.user.is_authenticated:
        if 's' in request.POST:
            s = request.POST['s']
            details = Account.objects.filter(username__icontains=s)
        else:
            details = Account.objects.all()
            return render(request, 'adminfiles/DashBoard.html', {'details': details})
    return redirect(admins_log)

@never_cache
def admin_login(request):
      if request.method == 'POST':
        email= request.POST.get('email')
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_superadmin:
          auth.login(request,user)
          messages.success(request,'you are now logged in')
          return redirect(admin_home)
        else:
            messages.error(request,'invalid login credientials')            
      return render(request, 'accounts/admins_login.html')

def Logout(request):
    if request.user:
        auth.logout(request)
    return redirect(admin_login)


def product_details(request):
    if request.user:
        if 's' in request.POST:
            s = request.POST['s']
            product_details = Product.objects.filter(product_name__icontains=s)
        else:
            product_details = Product.objects.all()
        return render(request, 'adminfiles/product_details.html', {'details': product_details})
    return redirect(admins_log)

def product_delete(request, id):
    prod_del = Product.objects.get(id=id)
    prod_del.delete()
    return redirect(product_details)

def edit_products(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        cat = category.objects.all()
        return render(request, 'products_edit.html', {'product': product, "cat": cat})
    return redirect(product_details)

def product_update(request,id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product_name = request.POST['product_name']
        price = request.POST['price']
        try:        
            image = request.FILES['image']
            product.images = image
        except:
            product.images = product.images
        stock = request.POST['stock']
        description = request.POST['description']
        product.product_name = product_name
        product.price = price
        product.stock = stock
        product.description = description
        product.save()
        return redirect(product_details)
    
def pro_update(request,id):
    product = Product.objects.get(id = id)
    return render(request,"adminfiles/product_update.html",{'product':product})

def category_details(request):
    if request.user:
        if 's' in request.POST:
            s = request.POST['s']
            category_details = category.objects.filter(product_name__icontains=s)
        else:
            category_details = category.objects.all()
        return render(request, 'adminfiles/category.html', {'details': category_details})
    return redirect(admins_log)

def category_update(request, id):
    if request.method == 'POST':
        cat = category.objects.get(id=id)
        category_name = request.POST['name']
        slug = cat.slug
        try:
            cat_image = request.FILES['image']
            cat.cat_image = cat_image
        except:
            cat.cat_image = cat.cat_image
        cat.category_name = category_name
        cat.slug = slug
        cat.save()
        return redirect(category_details)
    
def cat_update(request,id):
    categorys = category.objects.get(id = id)
    return render(request,"adminfiles/category_update.html",{'category':categorys})

def add_products(request):
    products =Product.objects.all()
    categorys = category.objects.all()
    return render(request, 'adminfiles/add_product.html', {'details': products,'category':categorys})

def product_delete(request, id):
    prod_del = Product.objects.get(id=id)
    prod_del.delete()
    return redirect(product_details)

def categorys(request):
    if request.user:
        if 's' in request.POST:
            s = request.POST['s']
            cat = category.objects.filter(category_name__icontains=s)
        else:
            cat = category.objects.all()            
        return render(request, 'category.html', {'details': cat})
    return redirect(admins_log)

def add_category(request):
    return render(request, 'adminfiles/add_category.html')

def category_delete(request, id):
    dele = category.objects.get(id=id)
    dele.delete()
    return redirect(category_details)

def new_products(request):
    if request.method == 'POST':
        product_name = request.POST['name']
        price = request.POST.get('price')
        cat1 = request.POST.get('category')
        variation=request.POST.get('variation')
        img = request.FILES['image']
        stock = request.POST['stock']
        slug = slugify(product_name)
        description = request.POST.get('description')
        try:
            cat = category.objects.get(id=cat1)         
        except:
            return redirect(add_products)    
        prod = Product.objects.create(product_name=product_name,slug = slug, price=price, category=cat,variation=variation, images=img,stock=stock, description=description)
        prod.save()
        return redirect(product_details)

def new_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category_name = request.POST['name']
            slug = slugify(category_name)
            cat_image = request.FILES['image']
            cat = category.objects.create(category_name=category_name,slug=slug, cat_image=cat_image)
            cat.save()
        return redirect(category_details)

def order_details(request):
    if request.user:
        if 's' in request.POST:
            s = request.POST['s']
            order_details = Order.objects.filter(product_name__icontains=s)
        else:
            order_details = Order.objects.all()
        return render(request, 'adminfiles/order.html', {'details': order_details})
    return redirect(admins_log)

def order_delete(request, id):
    if request.user:
        order = Order.objects.get(id=id)
        print(order)
        order.delete()
    return redirect(order_details)


def order_update(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        status = request.POST['status']
        order.status=status
        order.save()
        return redirect(order_details)
    
def order_upd(request,id):
    order = Order.objects.get(id = id)
    return render(request,"adminfiles/order_update.html",{'order':order})

def Dashboard(request):
    if request.user:
        cart = Order.objects.all()
        cat = category.objects.all()
        order_count = 0
        revenue = 0
        for i in cart:
            order_count = order_count+1
            revenue = revenue + i.order_total

        product = Product.objects.all()
        product_count = 0
        for i in product:
            product_count = product_count + 1

        cat = category.objects.all()
        cat_count=0
        for i in cat:
            cat_count=cat_count+1 
               
        user_list = Account.objects.all()
        user_count = 0
        for i in user_list:
            user_count = user_count+1
        
        # cat_count = []
        # for c in cat:
        #     cat_count.append(Product.objects.filter(category=c.id).count())
        ord_prod =OrderProduct.objects.all()
        ord_prd_count =0
        for i in ord_prod:
            ord_prd_count=ord_prd_count+1
        
        deliverd_count = Order.objects.filter(status='completed').count()
        return render(request, 'adminfiles/DashBoard.html',{'order_count':order_count, 'revenue':revenue, 'product_count':product_count, 'user_count':user_count,'cat_count':cat_count, 'deliverd_count':deliverd_count, 'cart': cart, 'product': product,'categorys': cat})


def SalesReport(request):
    if request.user:
        order = Order.objects.all()
        return render(request, 'adminfiles/SalesReport.html', {'orders': order})
    return redirect(admins_log)
def sales_date_wise(request):
    start = request.POST['start_date']
    end = request.POST['end_date']
    if len(start) < 1:
        messages.error(request, "choose Date")
        return redirect(SalesReport)
    if len(end) < 1:
        messages.error(request, "choose Date")
        return redirect(SalesReport)

    order = Order.objects.filter(created_at__range=[start, end])

    new_order_list = []
    for i in order:
        old = Order.objects.filter(id=i.id, user=i.user)
        for j in old:
            od = {'id': i.id, 'order_number':i.order_number,'created_at': i.created_at, 'user': i.user,
                  'order_total': j.order_total,  'status': i.status}
            new_order_list.append(od)
            print('order', new_order_list)
    o_count = len(order)
    return render(request, 'adminfiles/SalesReport.html', {'orders': new_order_list, 'o_count': o_count})
def sales_year_wise(request):
    month = request.POST['month']
    year = request.POST['year']
    print('year : ', year)
    if (year == 'Select'):
        messages.info(request, "Select the year")
        return redirect(SalesReport)
    print(month, year)
    if month == 'all':
        order = Order.objects.filter(created_date__year=year)
        new_order_list = []
        for i in order:
            old = Order.objects.filter(id=i.id, user=i.user)
            for j in old:
                od = {'id': i.id,'order_number':i.order_number, 'created_at': i.created_at, 'user': i.user,
                      'order_total': j.order_total, 'status': i.status}
                new_order_list.append(od)
        o_count = len(order)
        return render(request, 'SalesReport.html', {'orders': new_order_list, 'o_count': o_count})
    else:
        print("seperate")
        order = Order.objects.filter(
            created_at__year=year, created_at__month=month)
        new_order_list = []
        for i in order:
            old = Order.objects.filter(id=i.id, user=i.user)
            for j in old:
                od = {'id': i.id,'order_number':i.order_number, 'created_at': i.created_at, 'user': i.user,
                      'order_total': j.order_total,  'status': i.status}
                new_order_list.append(od)
        o_count = len(order)
        return render(request, 'adminfiles/SalesReport.html', {'orders': new_order_list, 'o_count': o_count})