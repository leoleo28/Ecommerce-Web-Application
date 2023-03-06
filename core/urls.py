from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('filter',views.filter,name='filter'),
    path('account',views.account,name='account'),
    path('category',views.category,name='category'),
    path('afterpayment',views.afterpayment,name='afterpayment'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    path('cart',views.cart,name='cart'),
    path('heart', views.heart, name='heart'),
    path('heart_remove',views.heart_remove,name='heart_remove'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('addtocart',views.addtocart, name='addtocart'),
    path('likeditem',views.likeditem, name='likeditem'),
    path('updatecart_add',views.updatecart_add,name='updatecart_add'),
    path('updatecart_minus',views.updatecart_minus,name='updatecart_minus'),
    path('updatecart_remove',views.updatecart_remove,name='updatecart_remove'),
    path('item/<str:pk>', views.item, name='item'),
]