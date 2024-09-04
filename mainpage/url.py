from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexpage,name='indexpage'),
    path('productsearch',views.productsearch,name='productsearch'),
    path('productview/<int:myid>',views.productview,name='productview'),
    path('myaddtocart',views.myaddtocart,name='myaddtocart'),
    path('productview/myaddtocart',views.myaddtocart,name='myaddtocart'),
    path('mycart',views.mycart,name='mycart'),
    path('clearcart',views.clearcart,name='clearcart'),
    path('myaddtocarttcart',views.myaddtocarttcart,name='myaddtocarttcart'),
    path('myaddtocartcart',views.myaddtocartcart,name='myaddtocartcart'),
    path('removecatitem',views.removecatitem,name='removecatitem'),
    path('myorders',views.myorders,name='myorders'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('search',views.search,name='search'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('changepassword2',views.changepassword2,name='changepassword2'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
        name="password_reset_complete"),
    path('orderdone',views.orderdone,name='orderdone'),
    path('gopaljigift',views.gopaljigift,name='gopaljigift'),
    path('success',views.success,name='success')
  

]