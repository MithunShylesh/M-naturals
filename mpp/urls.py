"""
URL configuration for mpp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about',views.about),
    path('registration',views.registration),
    path('cont',views.customer_contact),
    path('',views.index),
    path('shop',views.shop),
    path('service',views.service),
    path('login',views.login),
    path('companylogin',views.companylogin),
    path('userlogin',views.userlogin,name='userlogin'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('company_registration',views.company_registration),
    path('company_home',views.company_home, name='company_home'),
    path('usershop',views.usershop),
    path('usercart',views.usercart),
    path('userwishlist',views.userwishlist),
    path('userprofile',views.userprofile),
    path('bookingdetails',views.bookingdetails),
    path('logout',views.logout),
    path('addproduct',views.addproduct),
    path('manageproduct',views.manageproduct),
    path('customerdetails',views.customerdetails),
    path('companyprofile', views.companyprofile),
    path('adminaddproduct',views.adminaddproduct),
    path('adminmanageproduct',views.adminmanageproduct),
    path('aprovals',views.aprovals),
    path('condactinformation',views.condactinformation),
    path('delete/<int:d>',views.delete),
    path('update/<int:d>',views.update),
    path('updateproduct',views.updateproduct),
    path('add_cart/<int:d>',views.add_cart),
    path('wish_list/<int:d>',views.wish_list),
    path('increment/<int:d>', views.increment),
    path('decrement/<int:d>', views.decrement),
    path('update_profile/',views.update_profile),
    path('update_myprofile',views.update_myprofile),
    path('add_order/<int:d>',views.add_order),
    path('payment/<int:l>/<int:d>/<int:k>', views.payment),
    path('paymentsuccess', views.paymentsuccess),
    # path('paymentsuccess/<int:d>/', views.paymentsuccess,name='payment_success'),
    path('add_order_cart/<int:total>/<int:qty>', views.add_order_cart),
    path('payment_cart/<int:l>', views.paymentcart),
    path('paymentsuccess_cart', views.paymentsuccess_cart),
    path('cancel_order/<int:d>', views.cancel_order),
    path('cancel_order_cart/<int:d>', views.cancel_order_cart),
    path('companypayment', views.companypayment),
    path('companypayment_success', views.companypaymentsuccess),
    path('allorders', views.allorders),
    path('adminupdate/<int:d>', views.adminupdate),
    path('adminupdateproduct',views.adminupdateproduct),
    path('admindelete/<int:d>', views.admindelete),
    path('deletecart/<int:d>', views.deletecart),
    path('add_companyorder', views.add_companyorder),
    path('reject/<int:d>', views.reject),
    path('accept/<int:d>', views.accept),
    path('update_company_profile/', views.update_company_profile),
    path('update_companyprofile', views.update_companyprofile),
    path('usercondact', views.usercontact),
    path('companycontact', views.companycontact),
    path('vieworder/<int:d>', views.vieworder),
    path('vieworder_cart/<int:d>', views.vieworder_cart),
    path('vieworderproduct', views.vieworderproduct),
    path('vieworder_cartproduct', views.vieworder_cartproduct),
    path('refund/<int:d>', views.refund),
    path('refund_cart/<int:l>/<int:d>', views.refund_cart),
    path('refund_payment', views.refundsuccess),
    path('refund_cart_payment', views.refundsuccess_cart),
    path('forgot', views.forgot_password),
    path('reset/<token>', views.reset_password),
    path('forgot_c', views.forgot_password_c),
    path('reset/<token_c>', views.reset_password_c),
    path('deletewish/<int:d>', views.deletewish),
    # path('all_products', views.all_products),
    path('product_del/<int:d>', views.product_del),
    path('search', views.search),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

