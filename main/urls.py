from django.urls import path
from . import views
# from .views import RegisterUser

urlpatterns  = [
    path('', views.index, name='index'),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('register/', views.RegisterUserView.as_view(), name='register' ),
    path('logout/', views.MyLogoutView.as_view(), name='logout' ),
    path('cart/', views.cart, name='cart'),
    path('cart/increment/<int:id>/', views.increment, name='increment'),
    path('cart/decrement/<int:id>/', views.decrement, name='decrement'),
    path('cart/delete_all/', views.delete_all_products_from_cart, name='cart_delete_all'),
    path('cart/delete/', views.delete_single_product, name='cart_delete_single'),
    path('products/<int:id>/', views.product, name="product" ),
    path('categories/<str:category>', views.categories, name="categories"),
    path('user/add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('user/add_to_cart_with_amount/', views.add_to_cart_with_amount, name="add_to_cart"),
    path('leave_comment/', views.leave_comment, name="leave_comment"),
    path('payment/<int:sum>/', views.payment, name="payment"),
    path('create_order/', views.create_order, name="create_order"),
    path('all_orders/', views.all_orders, name="all_orders"),
    path('delete_order/<int:id>/', views.delete_order, name="delete_order"),
    path('confirm/', views.confirm, name="confirm")
    # path('register/', RegisterUser.as_view(), name="register")

]