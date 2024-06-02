from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import requests

from .forms import RegistrationForm, ResetPasswordForm, ForgotPasswordForm1, LoginForm, ChangePasswordForm
from accounts.models import Account
from carts.models import Cart, CartItem
from carts.views import _cart_id


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user_name = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=user_name,
                password=password,
            )
            print('user created')
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate Your Account"
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #return redirect('accounts:login''/?command=verification&email='+email)

            return redirect('accounts:verification_sent', email)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        # email = request.POST['email']
        # password = request.POST['password']
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                try:
                    cart_obj = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart_obj).exists()
                    if is_cart_item_exists:
                        # Filter by cart_id
                        cart_items = CartItem.objects.filter(cart=cart_obj)
                        product_variations_list = []
                        for item in cart_items:
                            product_variation = item.variations.all()
                            product_variations_list.append(list(product_variation))
                        # Filter by logged in user
                        cart_items_user = CartItem.objects.filter(user=user)
                        existing_variations_list = []
                        id = []
                        for item in cart_items_user:
                            existing_variations = item.variations.all()
                            existing_variations_list.append(list(existing_variations))
                            id.append(item.id)
                        for pr in product_variations_list:
                            if pr in existing_variations_list:
                                index = existing_variations_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                for item in cart_items:
                                    item.user = user
                                    item.save()
                except ObjectDoesNotExist:
                    pass
                auth.login(request, user)
                messages.success(request, 'login successful')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    print(params)
                    if 'next' in params:
                        next_page = params['next']
                        print(next_page)
                        return redirect(next_page)
                except:
                    return redirect("accounts:dashboard")
            else:
                messages.error(request, 'Invalid login credentials!')
                return redirect('accounts:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You're logged out")
    return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email activated, please login')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:register')


def verification_sent(request, email):
    context = {
        'email': email,
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgot_password(request):
    if request.method == "POST":
        #email = request.POST['email']
        form = ForgotPasswordForm1(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Account.objects.filter(email__exact=email).exists():
                user = Account.objects.get(email=email)
                current_site = get_current_site(request)
                mail_subject = "Reset Password"
                message = render_to_string('accounts/reset_password_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Reset password link has been sent to your account')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Account Does not exist')
                return redirect('accounts:forgot_password')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ForgotPasswordForm1()
    context = {'form': form}
    return render(request, 'accounts/forgot_password.html', context)


def reset_password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Reset your password")
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has expired')
        return redirect("accounts:login")


def reset_password(request):
    if request.method == "POST":
        # password = request.POST['password']
        # confirm_password = request.POST['confirm_password']
        # if password == confirm_password:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            #confirm_password = form.cleaned_data['confirm_password']
            print(f'UID: {request.session.get("uid")}')
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)

            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('accounts:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('accounts:reset_password')
    else:
        form = ResetPasswordForm()
    context = {'form': form}
    return render(request, 'accounts/reset_password.html', context)


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            print('form is valid')
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            try:
                user = request.user
            except ObjectDoesNotExist:
                print('ObjectDoesNotExist')
                messages.error(request, "You're logged out, login to change your password.")
                return redirect('accounts:login')
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset was successful!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Current password is incorrect')
                return redirect('accounts:change_password')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm()
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)