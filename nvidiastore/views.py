from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from nvidiastore.forms import RegForm
from nvidiastore.models import Product, Order, Customer


def signup(request):
    form = RegForm()

    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            Customer.objects.create(username=username)
            return redirect('login')

    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Incorrect Login')

    return render(request, 'signin.html', {})


def signout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required(login_url='login')
def order(request, product_url):
    username = request.user.username
    customer = Customer.objects.get(username=username)
    product = Product.objects.get(url=product_url)
    user_order = Order.objects.filter(customer__username=username, product__name=product.name).first()

    if user_order:
        user_order.quantity += 1
        user_order.save()
    else:
        Order.objects.create(customer=customer, product=product, quantity=1)

    return redirect('home')


@login_required(login_url='login')
def cart(request):
    username = request.user.username
    orders = Order.objects.filter(customer__username=username)
    user_cart = []
    total = 0

    for user_order in orders:
        total += user_order.product.price * user_order.quantity
        user_cart.append((user_order.product.name, user_order.quantity, int(user_order.product.price)))

    context = {'cart': user_cart, 'total': int(total)}
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def checkout(request):
    username = request.user.username
    Order.objects.filter(customer__username=username).delete()
    messages.info(request, 'Purchases complete')
    return redirect('cart')
