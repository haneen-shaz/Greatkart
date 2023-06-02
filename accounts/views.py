from django.shortcuts import render,redirect,get_object_or_404

from accounts.forms import UserForm, UserProfileForm
# from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile,Address
from orders.models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.contrib import  messages,auth


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
from store.models import Product
# import requests




# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        username = email.split("@")[0]
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone  = phone
        user.save()

        # Create a user profile
        profile = UserProfile()
        profile.user_id = user.id
        profile.profile_picture = 'default/default-user.png'
        profile.save()

    # USER ACTIVATION
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account'
        message = render_to_string('accounts/account_email_verification.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
        return redirect('/accounts/login/?command=verification&email='+email)
    return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                print('entering try block')
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
            
                  cart_item = CartItem.objects.filter(cart=cart)
                  print(cart_item)
                for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('home')
        else:
            messages.error(request,'invalid login credientials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
     'orders_count': orders_count,
    'userprofile': userprofile,
     }
    return render(request, 'accounts/dashboard.html',context)
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')
    l
           
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    # orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')
def addr(request):
    if request.user.is_authenticated:
        address=Address.objects.filter(user = request.user.id)
        return render(request,"accounts/address.html",{'address':address})

def add_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = Account.objects.get(id=request.user.id)
            print(user)
            first_name   = request.POST['first_name']
            last_name   = request.POST['last_name']
            email   = request.POST['email']
            state = request.POST['state']
            phone = request.POST['phone']
            address_line_1  = request.POST['address_line_1']
            address_line_2 = request.POST['address_line_2']
            type_address = request.POST['type_address']
            country= request.POST['country']
            state = request.POST['state']
            city = request.POST['city']

            address =Address.objects.create(user=user,first_name = first_name ,last_name= last_name,email= email, state=state,phone=phone,address_line_1 =address_line_1 ,address_line_2 =address_line_2 ,type_address=type_address,country=country,city=city )
            address.save()

            return redirect(addr)
        return redirect(edit_profile)

def address_add_page(request):
    if request.user.is_authenticated:
        return render(request,"accounts/add_address.html")
    
def returnItem(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            number = request.POST['order_number']
            order = Order.objects.get(order_number = number)
            order.status = "Cancelled"
            order.save()
            print(order.status) 
            return render(request, 'Success.html')
        return render(request,'accounts/returnItem.html')
