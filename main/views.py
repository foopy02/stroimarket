from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, Comment
import sqlite3
from .forms import AuthUserForm, RegisterUserForm
import json
import os
import random

ROOT_OF_DATABASE = f"{os.path.dirname(__file__)}/database.json"
CART_OF_USERS = f"{os.path.dirname(__file__)}/cart.json"
ORDERS_OF_USERS = f"{os.path.dirname(__file__)}/orders.json"
database = json.load(open(ROOT_OF_DATABASE, encoding="utf8"))
orders = json.load(open(ORDERS_OF_USERS, encoding="utf8"))

random.shuffle(database)


def get_info_about_product(id):
    for product in database:
        if product["id"] == id:
            return product


def index(request):
    amount = 0
    if request.user.is_authenticated:
        amount = _get_amount_of_items(request.user.username)
    new_products = database[12:24]
    recomended = random.sample(database, 20)
    return render(
        request,
        "main/index.html",
        {
            "new_products": new_products,
            "recomended": recomended,
            "amount": amount,
            "all_products": database,
        },
    )


def product(request, id):
    amount = 0
    if request.user.is_authenticated:
        amount = _get_amount_of_items(request.user.username)
    product = get_info_about_product(id)
    comments = Comment.objects.filter(product_id=id)
    return render(
        request,
        "main/product.html",
        {
            "product": product,
            "amount": amount,
            "all_products": database,
            "comments": comments,
        },
    )


def payment(request, sum):
    return render(request, "main/payment.html", {"sum": sum})

def create_order(request):
    orders = json.load(open(ORDERS_OF_USERS, encoding="utf8"))
    username = request.user.username
    amount_of_cart = _get_amount_of_items(username)
    cart_of_user = Cart.objects.filter(username=username)
    list_of_products = []
    amount_of_products = 0
    total_sum = 0
    checked_ids = []
    for item in cart_of_user:
        if item.product_id not in checked_ids:
            product = list(filter(lambda x: x["id"] == item.product_id, database))
            amount = cart_of_user.filter(product_id=item.product_id)
            amount = amount.count()
            list_of_products.append([product[0], amount])
            amount_of_products = amount
            total_sum += product[0]["price"] * amount
            checked_ids.append(item.product_id)
            
    now = datetime.now()
    order = {
        'id':len(orders)+1,
        'username':username,
        'products':[int(x.product_id) for x in cart_of_user],
        'amount':cart_of_user.count(),
        'total':total_sum,
        'datetime':now.strftime("%d/%m/%Y %H:%M:%S"),
        'status':"НЕ ОПЛАЧЕНО"
    }
    order['id'] = len(orders)
    if order not in orders:
        order['id'] = len(orders)+1
        orders.append(order)
        json.dump(orders,open(ORDERS_OF_USERS,'w',encoding='utf-8'), indent=2, ensure_ascii=False)
    return render(request, "main/payment.html", {"sum": total_sum})

def all_orders(request):
    orders = json.load(open(ORDERS_OF_USERS, encoding="utf8"))
    total_sum = 0
    for order in orders:
        total_sum += int(order['total'])
    amount_of_cart = _get_amount_of_items(request.user.username)
    
    return render(request, "main/orders.html", {"orders": orders,'total_sum':total_sum,'amount':amount_of_cart})
def confirm(request):
    amount_of_cart = _get_amount_of_items(request.user.username)
    return render(request, "main/confirm.html", {"orders": orders,'amount':amount_of_cart})

def delete_order(request, id):
    orders = json.load(open(ORDERS_OF_USERS, encoding="utf8"))
    counter = 0
    for order in orders:
        if int(order['id']) == int(id):
            orders.pop(counter)
        counter+=1
    json.dump(orders,open(ORDERS_OF_USERS,'w',encoding='utf-8'), indent=2, ensure_ascii=False)
    return redirect('all_orders')

def cart(request):
    amount = 0
    if request.user.is_authenticated:
        username = request.user.username
        amount_of_cart = _get_amount_of_items(username)

        cart_of_user = Cart.objects.filter(username=username)

        list_of_products = []
        amount_of_products = 0
        total_sum = 0
        checked_ids = []
        for item in cart_of_user:
            if item.product_id not in checked_ids:
                product = list(filter(lambda x: x["id"] == item.product_id, database))
                amount = cart_of_user.filter(product_id=item.product_id)
                amount = amount.count()
                list_of_products.append([product[0], amount])
                amount_of_products = amount
                total_sum += product[0]["price"] * amount
                checked_ids.append(item.product_id)
        print(amount)
        return render(
            request,
            "main/cart.html",
            {
                "amount": amount_of_cart,
                "products": list_of_products,
                "amount_of_products": amount_of_cart,
                "total_sum": total_sum,
                "all_products": database,
            },
        )


def categories(request, category):
    amount = 0
    if request.user.is_authenticated:
        amount = _get_amount_of_items(request.user.username)
    products = filter(lambda x: x["category"] == category, database)
    categories_name = {
        "krovelnye-materialy": "Кровельные материалы",
        "dvp-dsp-plity-osb-fanera-pilomaterialy": "ДВП, ДСП, ПЛИТЫ OSB, ФАНЕРА, ПИЛОМАТЕРИАЛЫ",
        "mebelnye-shity": "Мебельные щиты",
        "stroitelstvo-sten-i-peregorodok": "Строительство стен и перегородок",
        "stroitelnye-smesi-i-gruntovka": "СТРОИТЕЛЬНЫЕ СМЕСИ, ЦЕМЕНТ, ГИПС",
        "gipsokarton-i-komplektuyushie": "ГИПСОКАРТОН И КОМПЛЕКТУЮЩИЕ",
        "paneli-stenovye-i-komplektuyushie": "ПАНЕЛИ СТЕНОВЫЕ И КОМПЛЕКТУЮЩИЕ",
        "stroitelnye-setki": "СТРОИТЕЛЬНЫЕ СЕТКИ",
        "stroitelnaya-izolyaciya": "СТРОИТЕЛЬНАЯ ИЗОЛЯЦИЯ",
        "elementy-dekora": "ЭЛЕМЕНТЫ ДЕКОРА",
        "lestnichnye-elementy": "ЛЕСТНИЧНЫЕ ЭЛЕМЕНТЫ",
        "kovanye-elementy": "КОВАНЫЕ ЭЛЕМЕНТЫ",
    }
    contex = {
        "products": products,
        "category": categories_name[category],
        "amount": amount,
        "all_products": database,
    }
    return render(request, "main/categories.html", contex)


def _update_cart(new_cart):
    json.dump(
        new_cart,
        open(CART_OF_USERS, "w", encoding="utf-8"),
        indent=2,
        ensure_ascii=False,
    )


def _get_amount_of_items(username):
    # carts = json.load(open(CART_OF_USERS, encoding='utf8'))
    carts = Cart.objects.filter(username=username)
    result = 0

    return carts.count


def add_to_cart(request):
    id_of_product = int(request.GET.get("id"))
    username = request.user.username
    price = get_info_about_product(id_of_product)["price"]
    p = Cart(username=username, product_id=id_of_product, price=price, amount=1)
    p.save()
    return JsonResponse({"status": "Succesfully done!"})


def add_to_cart_with_amount(request):
    id_of_product = int(request.GET.get("id"))
    amount = int(request.GET.get("amount"))
    username = request.user.username
    price = get_info_about_product(id_of_product)["price"]
    for i in range(amount):
        p = Cart(
            username=username, product_id=id_of_product, price=price, amount=amount
        )
        p.save()
    return JsonResponse({"status": "Succesfully done!"})

def increment(request, id ):
    id_of_product = int(id)
    username = request.user.username
    price = get_info_about_product(id_of_product)["price"]
    p = Cart(
        username=username, product_id=id_of_product, price=price, amount=1
    )
    p.save()
    return redirect('cart')

def decrement(request, id ):
    id_of_product = int(id)
    username = request.user.username
    print(Cart.objects.filter(username=username,product_id=id_of_product))    
    for i in Cart.objects.filter(username=username,product_id=id_of_product):
        i.delete()
        break
    return redirect('cart')

def delete_all_products_from_cart(request):
    username = request.user.username
    Cart.objects.filter(username=username).delete()
    return redirect("cart")


def delete_single_product(request):
    id = request.POST.get("id")
    username = request.user.username
    Cart.objects.filter(username=username).filter(product_id=id).delete()
    return redirect("cart")


@login_required(login_url="/login/")
def leave_comment(request):
    id = request.POST.get("id")
    name = request.POST.get("name")
    stars = request.POST.get("stars")
    comment = request.POST.get("comment")
    user = request.user
    comment = Comment(user=user, name=name, stars=stars, comment=comment, product_id=id)
    comment.save()
    return redirect("product", id=id)


class MyLoginView(LoginView):
    template_name = "main/login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy("index")


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("index")


class RegisterUserView(CreateView):
    model = User
    template_name = "main/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("login")
    success_msg = "Пользователь успешно создан"
