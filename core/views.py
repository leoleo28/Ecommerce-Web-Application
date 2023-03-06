from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode

    
@login_required(login_url='signin')
def index(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items1 = Ordereditem.objects.filter(user=user_model)
    num_cart=0
    for item in items1:
        num_cart+=item.quantity
    items2 = Likeditem.objects.filter(user=user_model)
    num_heart=len(items2)
    arrival=Product.objects.filter(category='New Arrival')
    trend=Product.objects.filter(category='Trend')
    sell=Product.objects.filter(category='Sell')

    if request.method == 'POST':
        name = request.POST['search']
        base_url = '/filter'  
        query_string =  urlencode({'selecteditem': name})  
        query_string_2 =  urlencode({'page': 1})  
        url = '{}?{}&{}'.format(base_url, query_string,query_string_2)  
        return redirect(url)  
    
    else:
        products=Product.objects.filter(category='New')
        context={
            'products':products,
            'num_cart':num_cart,
            'num_heart':num_heart,
            'arrival':arrival,
            'trend':trend,
            'sell':sell,
        }
        return render(request,'index.html', context)

@login_required(login_url='signin')
def filter(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items1 = Ordereditem.objects.filter(user=user_model)
    num_cart=0
    for item in items1:
        num_cart+=item.quantity
    items2 = Likeditem.objects.filter(user=user_model)
    num_heart=len(items2)
    arrival=Product.objects.filter(category='New Arrival')
    trend=Product.objects.filter(category='Trend')
    sell=Product.objects.filter(category='Sell')
    item=request.GET.get('selecteditem')
    selected_list=Product.objects.filter(name__icontains=item)
    pagesize=12
    paginator=Paginator(selected_list, pagesize)
    page_number=request.GET.get('page')
    
    try:
        products = paginator.page(page_number) 
        page_number=int(page_number)
    except PageNotAnInteger:
        products = paginator.page(1) 
        page_number=1
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 
        page_number=paginator.num_pages
    
    left = []
    right = []
    left_has_more, right_has_more, first, last = [False]*4
    total_pages = paginator.num_pages
    page_range = paginator.page_range

    if len(selected_list)<=pagesize:
        context={
        'products':products,
        'item':item,
        'num_cart':num_cart,
        'num_heart':num_heart,
        'arrival':arrival,
        'trend':trend,
        'sell':sell,
        'multipage':False,
        }
        return render(request,'filter.html', context)

    if page_number == 1:
        right = page_range[page_number:page_number + 4]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        left = page_range[(page_number - 5) if (page_number - 5) > 0 else 0:page_number - 1]
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    else:
        left = page_range[(page_number - 5) if (page_number - 5) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 4]
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    
    context={
        'products':products,
        'item':item,
        'num_cart':num_cart,
        'num_heart':num_heart,
        'arrival':arrival,
        'trend':trend,
        'sell':sell,
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
        'page_number':page_number,
        'total_pages':total_pages,
        'multipage':True,
    }
    return render(request,'filter.html', context)

@login_required(login_url='signin')
def cart(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items = Ordereditem.objects.filter(user=user_model)
    total=0
    for item in items:
        total+=item.get_total
    return render(request,'cart.html',{'items':items,'total':total})

@login_required(login_url='signin')
def heart(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items = Likeditem.objects.filter(user=user_model)
    return render(request,'likeditem.html',{'items':items})

@login_required(login_url='signin')
def category(request):
    item=request.GET.get('type')
    paginator=Paginator(Product.objects.filter(category=item),12)
    page=request.GET.get('page')

    try:
        products = paginator.page(page) 
        page=int(page)
    except PageNotAnInteger:
        products = paginator.page(1) 
        page=1
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 
        page=paginator.num_pages

    nums="a"*products.paginator.num_pages
    username = request.user.username
    user_model = User.objects.get(username=username)
    items1 = Ordereditem.objects.filter(user=user_model)
    num_cart=0
    for item in items1:
        num_cart+=item.quantity
    items2 = Likeditem.objects.filter(user=user_model)
    num_heart=len(items2)
    arrival=Product.objects.filter(category='New Arrival')
    trend=Product.objects.filter(category='Trend')
    sell=Product.objects.filter(category='Sell')

    context={
        'item':item,
        'products':products,
        'nums':nums,
        'page':page,
        'num_cart':num_cart,
        'num_heart':num_heart,
        'arrival':arrival,
        'trend':trend,
        'sell':sell,
    }
    return render(request,'index.html', context)

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('account')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('account')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('account')
        
    else:
        return render(request, 'account.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('account')
    else:
        return render(request, 'account.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('account')

@login_required(login_url='signin')
def addtocart(request):
    if request.method=='POST':
        number=request.POST['number']
        username = request.user.username
        user_model = User.objects.get(username=username)
        id = request.GET.get('id') 
        added_item = Ordereditem.objects.filter(item_id=id, user=user_model).first()
        if added_item == None:
            product=Product.objects.get(id=id)
            new_added_item = Ordereditem.objects.create(item_id=id, user=user_model, item_name=product.name,item_img=product.img, item_price=product.price, item_category=product.category,quantity=number)
            new_added_item.save()
            return redirect('/')
        else:
            added_item.quantity+=int(number)
            added_item.save()
            return redirect('/')
    else:
        username = request.user.username
        user_model = User.objects.get(username=username)
        id = request.GET.get('id') 
        added_item = Ordereditem.objects.filter(item_id=id, user=user_model).first()
        if added_item == None:
            product=Product.objects.get(id=id)
            new_added_item = Ordereditem.objects.create(item_id=id, user=user_model, item_name=product.name,item_img=product.img, item_price=product.price, item_category=product.category)
            new_added_item.save()
            return redirect('/')
        else:
            added_item.delete()
            return redirect('/')
    
@login_required(login_url='signin')
def likeditem(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    id = request.GET.get('id') 
    liked_item = Likeditem.objects.filter(item_id=id, user=user_model).first()

    if liked_item == None:
        product=Product.objects.get(id=id)
        new_added_item = Likeditem.objects.create(item_id=id, user=user_model, item_name=product.name,item_img=product.img, item_price=product.price, item_category=product.category)
        new_added_item.save()
        return redirect('/')
    else:
        liked_item.delete()
        return redirect('/')

@login_required(login_url='signin')
def updatecart_add(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    id = request.GET.get('id') 
    item = Ordereditem.objects.get(item_id=id, user=user_model)
    item.quantity+=1
    item.save()
    return redirect('cart')

@login_required(login_url='signin')
def updatecart_minus(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    id = request.GET.get('id') 
    item = Ordereditem.objects.get(item_id=id, user=user_model)
    item.quantity-=1
    if item.quantity<=0:
        item.delete()
    else:
        item.save()
    return redirect('cart')

@login_required(login_url='signin')
def updatecart_remove(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    id = request.GET.get('id') 
    item = Ordereditem.objects.get(item_id=id, user=user_model)
    item.delete()
    return redirect('cart')

@login_required(login_url='signin')
def heart_remove(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    id = request.GET.get('id') 
    item = Likeditem.objects.get(item_id=id, user=user_model)
    item.delete()
    return redirect('heart')
    
@login_required(login_url='signin')
def item(request, pk):
    product = Product.objects.get(id=pk)
    category=product.category
    product_list=Product.objects.filter(category=category)
    L=[]
    for p in product_list:
        if p.name!=product.name:
            L.append(p)
    random.shuffle(L)
    L=L[:10]
    if category=='NEW':
        category='#'
    context={
        'product':product,
        'list':L,
        'category':category
    }
    return render(request,'product.html',context)

@csrf_exempt
def afterpayment(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items = Ordereditem.objects.filter(user=user_model)
    items.delete()
    return JsonResponse('Payment Success',safe=False)

@login_required(login_url='signin')
def apply_coupon(request):
    username = request.user.username
    user_model = User.objects.get(username=username)
    items = Ordereditem.objects.filter(user=user_model)
    total_1=0
    for item in items:
        total_1+=item.get_total
    total_2=total_1
    if total_2>=100:
        total_2-=30
    return render(request,'coupon.html',{'items':items,'total_1':total_1,'total_2':total_2})

def account(request):
    return render(request,'account.html')