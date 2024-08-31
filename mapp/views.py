from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import*
from django.shortcuts import render
from django.contrib import messages
import razorpay
from datetime import datetime,timedelta

# Create your views here.
def about(re):
    return render(re,'about.html')
def registration(re):
    if re.method == "POST":
        a = re.POST['name']
        b = re.POST['ph_no']
        g = re.POST['address']
        c = re.POST['email']
        d = re.POST['username']
        e = re.POST['password']
        f = re.POST['confirm_password']
        if reg.objects.filter(username=d).exists():
            return HttpResponse("<script>alert('Username already taken.')</script>")
        else:
            if e==f:
                data=reg.objects.create(name=a,ph_no=b, address=g , email=c,username=d,password=e)
                data.save()
                return HttpResponse("<script>alert('Registered Successfull')</script>")
            else:
                return HttpResponse("<script>alert('Password do not match.')</script>")
    return render(re, 'registration.html')

def customer_contact(re):
    if re.method == "POST":
        a = re.POST['name']
        b = re.POST['email']
        c = re.POST['subject']
        d = re.POST['message']
        data=contact.objects.create(name=a,email=b,subject=c,message=d)
        data.save()
        return HttpResponse("<script>alert('message registered successfully')</script>")
    return render(re,'contact.html')
def index(re):
    return render(re,'index.html')
def shop(re):
        data = product.objects.all()
        print(data)
        return render(re, 'shop.html', {'data': data})
def service(re):
    return render(re,'service.html')

def companylogin(re):

        if re.method == "POST":
            p = re.POST['company_username']
            q = re.POST['company_password']
            try:
                    data = company_reg.objects.get(company_username=p)
                    print(data)

                    if q == data.company_password:
                            re.session['company'] = p
                            print(data.company_password)
                            if data.status == "approved":
                                return redirect('company_home')
                            else:
                                # messages.success(re, 'Company Registration not yet Approved')
                                return HttpResponse("<script>alert('Company Registration not yet Approved')</script>")
                    else:
                        return HttpResponse("incorrect password")

            except Exception:
                return HttpResponse("invalid username")
        else:
          return render(re, 'companylogin.html')


def login(re):
    if re.method=="POST":
        p=re.POST['username']
        q=re.POST['password']
        try:
            data=reg.objects.get(username=p)
            print(data)
            if q==data.password:
                re.session['user']=p
                print(data.password)
                return redirect('userlogin')

            return HttpResponse("incorrect password")
        except Exception:
            if p == 'Mnaturals' and q == 'Mm1206':
                re.session['admin']=p
                return redirect('adminlogin')
            else:
                return HttpResponse("invalid username or invalid username and  password for admin")
    else:
        return render(re,'login.html')
def userlogin(re):
    return render(re,'user/userlogin.html')
def adminlogin(re):
    return render(re,'admin/adminlogin.html')
def company_registration(re):
    if re.method == "POST":
        a = re.POST['company_name']
        b = re.POST['company_address']
        c = re.POST['company_email']
        d = re.POST['company_condactno']
        e = re.POST['owner_name']
        f = re.FILES['owner_adharphoto']
        g = re.POST['company_username']
        h = re.POST['company_password']
        i = re.POST['company_confirmpassword']
        if company_reg.objects.filter(company_username=g).exists():
            return HttpResponse("<script>alert('Username already taken.')</script>")
        else:
            if h==i:
                data=company_reg.objects.create(company_name=a,company_address=b,company_email=c,company_condactno=d,owner_name=e,owner_adharphoto=f,company_username=g,company_password=h,)
                data.save()
                return HttpResponse("<script>alert('registered successfully')</script>")
            else:
                return HttpResponse("password does not match")
    return render(re, 'company_registration.html')
def company_home(re):
    return render(re,'company/company_home.html')
def usershop(re):
    if 'user' in re.session:
        data = product.objects.all()
        print(data)
        return render(re,'user/usershop.html',{'data': data })
    return render(re,'login.html')
def usercart(re):
    if 'user' in re.session:

        data = reg.objects.get(username=re.session['user'])
        cart_items = cart.objects.filter(user_details=data)
        qty = 0
        total = 0
        for i in cart_items:
            qty += i.quantity
            total += i.product_details.cost* i.quantity
        if not cart_items:
            return render(re, 'user/usercart.html')

        return render(re, 'user/usercart.html', {'cart_items': cart_items, 'total': total, 'qty': qty})
    return redirect(login)

def userprofile(re):
    if 'user' in re.session:
            data = reg.objects.get(username=re.session['user'])

            print(data)
            return render(re, 'user/profile.html', {'data': data})
    return redirect(userlogin)
def bookingdetails(re):
    if 'user' in re.session:
        u=reg.objects.get(username=re.session['user'])
        data = order.objects.filter(user=u)
        bata=order_cart.objects.filter(user=u)
        return render(re, 'user/bookingdetails.html', {'data': data,'bata':bata})
    return redirect(userlogin)
def userwishlist(re):
    if 'user' in re.session:
        bata = reg.objects.get(username=re.session['user'])
        data = wish.objects.filter(user_details=bata)
        print(data)
        qty = 0
        total = 0
        for i in data:
            qty += i.quantity
            total += i.product_details.cost* i.quantity

        if not data:
            return render(re, 'user/userwishlist.html')

        return render(re, 'user/userwishlist.html', {'data': data})
    return render(re, 'login.html')


def logout(re):
    if 'user' in re.session:
        re.session.flush()
        return redirect(login)
    elif 'company' in re.session:
        re.session.flush()
        return redirect(companylogin)
    return redirect(index)
def addproduct(re):
    if 'company' in re.session:
        print(re.session['company'])
        data = company_reg.objects.get(company_username=re.session['company'])
        if data.payment_status == "paid":
            if re.method == 'POST':
                a = re.POST['pname']
                c = re.POST['cost']
                d = re.POST['stock']
                e = re.FILES['image']
                f = re.POST['definition']
                product.objects.create(pname=a, cost=c, stock=d, image=e, definition=f, company_details=data).save()
                messages.success(re, 'DATA SAVED')
            return render(re, 'company/addproduct.html')
        else:
            return redirect(companyprofile)

    return redirect(companylogin)

def customerdetails(re):
    if 'company' in re.session:
        print(re.session['company'])
        g=company_reg.objects.get(company_username=re.session['company'])
        data = order.objects.filter(company_details=g)
        print(data)
        return render(re, 'company/customerdetails.html',{'data':data} )
    return redirect(companylogin)
def companyprofile(re):
    if 'company' in re.session:
            data = company_reg.objects.get(company_username=re.session['company'])
            print(data)
            return render(re, 'company/companyprofile.html', {'data': data})
    return redirect(companylogin)

def manageproduct(re):
    if 'company' in re.session:
        data = company_reg.objects.get(company_username=re.session['company'])
        d = product.objects.filter(company_details=data)
        print(data)
        return render(re,'company/manageproduct.html',{'d':d})
    return redirect(companylogin)
def adminaddproduct(re):
    if 'admin' in re.session:
        print(re.session['admin'])
        data = company_reg.objects.get(company_username=re.session['admin'])
        if re.method == 'POST':
            a = re.POST['pname']
            c = re.POST['cost']
            d = re.POST['stock']
            e = re.FILES['image']
            f = re.POST['definition']
            product.objects.create(pname=a, cost=c, stock=d, image=e, definition=f, company_details=data).save()
            messages.success(re, 'DATA SAVED')
        return render(re, 'admin/adminaddproduct.html')

    return redirect(login)
def adminmanageproduct(re):
    if 'admin' in re.session:
        # data = company_reg.objects.get(company_username=re.session['admin'])
        d = product.objects.all()
        return render(re, 'admin/adminmanageproduct.html', {'d': d})
    return redirect(login)
def aprovals(re):
    if 'admin' in re.session:
        data = company_reg.objects.all()
        print(data)
        return render(re,'admin/aprovals.html',{'data':data})
    return redirect(login)
def condactinformation(re):
    if 'admin' in re.session:
        data = contact.objects.all()
        data2=user_contact.objects.all()
        data3=company_contact.objects.all()
        print(data)
        return render(re, 'admin/condactinformation.html', {'data': data,'data2':data2,'data3':data3})
    return redirect(userlogin)
def delete(re,d):
    if 'company' in re.session:
        data=product.objects.get(pk=d)
        data.delete()
        messages.success(re,'product delete successfully')
        return redirect(manageproduct)
    return redirect(companylogin)
from .forms import *

def update(re,d):
    if 'company' in re.session:
        data=product.objects.get(pk=d)
        n=model_form(instance=data)
        if re.method=="POST":
            n=model_form(re.POST,re.FILES,instance=data)
            if n.is_valid():
                n.save()
                return redirect(manageproduct)
        return render(re, 'company/updateproduct.html', {'data':n})
    return redirect(companylogin)

def updateproduct(re):
    return render(re,'company/updateproduct.html')
def add_cart(re,d):
    if 'user' in re.session:
        u=reg.objects.get(username=re.session['user'])
        p=product.objects.get(pk=d)
        # v=company_reg.objects.get(company_username=p.company_details)
        print(p.company_details)
        if cart.objects.filter(user_details=u,product_details=p,company_details=p.company_details).exists():
            messages.success(re,'item already exist')
        else:
            cart.objects.create(user_details=u,product_details=p,company_details=p.company_details).save()
            messages.success(re,'item added to cart successfully')
        return redirect(usercart)
    return redirect(login)
def wish_list(re,d):
    if 'user' in re.session:
        u=reg.objects.get(username=re.session['user'])
        p=product.objects.get(pk=d)
        # v=company_reg.objects.get(pk=d)
        if wish.objects.filter(user_details=u,product_details=p,company_details=p.company_details).exists():
            messages.success(re,'item already exist')
        else:
            wish.objects.create(user_details=u,product_details=p,company_details=p.company_details).save()
            messages.success(re,'item added to wishlist successfully')
        return redirect(userwishlist)
    return redirect(login)
def deletewish(re,d):
    if 'user' in re.session:
        data=wish.objects.get(pk=d)
        data.delete()
        messages.success(re,'product delete  from  wishlist successfully')
        return redirect(userwishlist)
    return redirect(userlogin)
def increment(re,d):
    if 'user' in re.session:
        data=cart.objects.get(pk=d)
        print(data)
        data.quantity+=1
        data.save()
        return redirect(usercart)
    return redirect(login)
def decrement(re,d):
    if 'user' in re.session:
        data=cart.objects.get(pk=d)
        print(data)
        data.quantity-=1
        data.save()
        return redirect(usercart)
    return redirect(login)
def update_profile(re):
    if 'user' in re.session:
        data=reg.objects.get(username=re.session['user'])
        n=reg_form(instance=data)
        print(n)
        if re.method=="POST":
            n=reg_form(re.POST,re.FILES,instance=data)
            if n.is_valid():
                n.save()
                return redirect(userprofile)
        return render(re, 'user/update_profile.html', {'data':n})
    return redirect(userlogin)

def update_myprofile(re):
    return render(re,'user/update_profile.html')
def add_order(request,d):
    user_reg = reg.objects.get(username=request.session['user'])
    print(user_reg.username)
    pro = product.objects.get(pk=d)
    print(pro)
    # bro = company_reg.objects.get(pk=d)
    if request.method=='POST':
        a = request.POST.get('name')
        b= request.POST.get('email')
        c = request.POST.get('address')
        # m = request.POST.get('city')
        # e = request.POST.get('state')
        # f = request.POST.get('country')
        g = request.POST.get('zip_code')
        h = request.POST.get('phone')
        k = int(request.POST.get('quantity'))
        l = int(request.POST.get('total_price'))
        p=datetime.now()
        ten_days = timedelta(days=10)
        j= p + ten_days
        if pro.stock >= 1:
            val = order.objects.create(user=user_reg, name=a, email=b,address=c,  zip_code=g, phone=h,purchase_date=str(p),delivery_date=j, product_order=pro,company_details=pro.company_details,quantity=k,total_price=l)
            val.save()
            request.session['order_name']= pro.pname
            print("add"+str(val.pk))
            request.session['order_id'] = val.pk
            return redirect(payment,l,d,k)
        else:
            messages.error(request,'Low Stock')
            return redirect(usershop)
    return render(request, 'add_order.html',{'data':pro, 'user_reg':user_reg })
def payment(request,l,d,k):
    pro = product.objects.get(pk=d)
    amount = l * 100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    if pro.stock >=1:
        product.objects.filter(pk=pro.id).update(stock =pro.stock-k)
    a = request.session['order_id']
    d = order.objects.filter(pk=a).update(payment_status="PAID")
    return render(request, "payment.html",{'amount':amount})
@csrf_exempt

def paymentsuccess(request):
    # if 'user' in request.session:
    #     user = reg.objects.get(username='Mithun')
    #     print(user)
    #     a = request.session['order_id']
    #     print(a)
    #     c = request.session['order_name']
    #     print(c)
        # d = order.objects.filter.update(pk=a)(payment_status="PAID")
        return render(request, "payment_success.html")
    # else:
    #     return render(request,'login.html')

# def payment_success(request):
#
#     user=reg.objects.get(username=request.session['user'])
#     # a = request.session['order_id']
#     # print(a)
#     b = 'PAID'
#     # c = request.session['order_name']
#     # print(c)
#     # order.objects.filter(pk=a).update(payment_status=b)
#     # send_mail('Payment Successful',
#     #           f'Hey {user.name}, Your payment was successful and order for {c} has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
#     #           'settings.EMAIL_HOST_USER', [user.email], fail_silently=False)
#     # send_mail('New Order',
#     #           f' {user.name}, has placed a new order for {c}\nPlease review and update the order status',
#     #           'settings.EMAIL_HOST_USER', ['gmrznadmn@gmail.com'], fail_silently=False)
#     return render(request, "payment_success.html")

def add_order_cart(request,total,qty):
    # user = register.objects.get(email=request.session['user'])
    user_reg= reg.objects.get(username=request.session['user'])
    print(user_reg.username)
    print(user_reg.name)
    pro=cart.objects.filter(user_details=user_reg)
    order_ids = []
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('address')
        # d = request.POST.get('city')
        # e = request.POST.get('state')
        # f = request.POST.get('country')
        g = request.POST.get('zip_code')
        h = request.POST.get('phone')
        p = datetime.now()
        l=int(request.POST.get('total_pprice'))
        m=request.POST.get('total_quantity')
        ten_days = timedelta(days=10)
        j = p + ten_days
        for i in pro:
            cn = i.product_details
            cq = i.quantity
            ct = i.product_details.cost * i.quantity
            v=order_cart.objects.create(user=user_reg, name=a,email=b,address=c, zip_code=g, phone=h,delivery_date=j,purchase_date=p, product_order=cn,company_details=i.company_details,total_pprice=l,total_quantity=m)
            v.save()
            value1 = v.pk
            order_ids.append(value1)
            if i.product_details.stock >=1:
                product.objects.filter(pk=i.product_details.pk).update(stock=i.product_details.stock-cq)
                request.session['order_ids'] = v.pk
                return redirect(paymentcart, l)
            else:
                messages.error(request,'Low Stock')
                return redirect(usercart)


    return render(request,'add_order_cart.html',{'data':pro,'total':total,'qty':qty, 'user_reg':user_reg})

def paymentcart(request,l):
    amount = l * 100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    a = request.session['order_ids']
    d = order_cart.objects.filter(pk=a).update(payment_status="PAID")
    return render(request, "paymentcart.html",{'amount':amount})
@csrf_exempt

def paymentsuccess_cart(request):
    # usr = reg.objects.get(username=request.session['user'])
    # order_ids = request.session.get('order_ids', [])
    # for i in order_ids:
    #     c = i
    #     b = 'PAID'
    #     order.objects.filter(pk=c).update(payment_status=b)
    # send_mail('Payment Successful',
    #           f'Hey {usr.name}, Your payment was successful and your ordered items has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
    #           'settings.EMAIL_HOST_USER', [usr.email], fail_silently=False)
    # send_mail('New Order',
    #           f' {usr.name}, has placed a some new orders\nPlease review and update the order status',
    #           'settings.EMAIL_HOST_USER', ['aninaabraham01@gmail.com'], fail_silently=False)
    return render(request, "paymentsuccess_cart.html")

def cancel_order(re,d):
    if 'user' in re.session:
        order.objects.filter(pk=d).update(product_status="cancelled")
        return redirect(bookingdetails)
def cancel_order_cart(re,d):
    if 'user' in re.session:
        order_cart.objects.filter(pk=d).update(product_status="cancelled")
        return redirect(bookingdetails)


def add_companyorder(request):
    v = company_reg.objects.get(company_username=request.session['company'])
    subscription.objects.create(company_details=v,amount=5000).save
    data=subscription.objects.filter(company_details=v,amount=5000)
    return render(request,'company/add_companyorder.html',{'data':data})




def companypayment(request):
    amount = 5000 * 100
    print(amount)
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    data = company_reg.objects.get(company_username=request.session['company'])
    data.payment_status='paid'
    data.save()
    return render(request, "company/companypayment.html", {'amount': amount})
@csrf_exempt


def companypaymentsuccess(request):
    # user=company_reg.objects.get(company_username=request.session['company'])
    # order_ids = request.session.get('order_ids', [])
    # for i in order_ids:
    #     c = i
    #     b = 'PAID'
    #     order.objects.filter(pk=c).update(payment_status=b)
    # send_mail('Payment Successful',
    #           f'Hey {usr.name}, Your payment was successful and your ordered items has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
    #           'settings.EMAIL_HOST_USER', [usr.email], fail_silently=False)
    # send_mail('New Order',
    #           f' {usr.name}, has placed a some new orders\nPlease review and update the order status',
    #           'settings.EMAIL_HOST_USER', ['aninaabraham01@gmail.com'], fail_silently=False)
    return render(request, "company/companypayment_success.html")


def allorders(re):
    if 'admin' in re.session:
        d = order.objects.all()
        b=order_cart.objects.all()
        return render(re, 'admin/allorders.html', {'d': d,'b':b})
    return redirect(login)
def adminupdate(re,d):
    if 'admin' in re.session:
        data=product.objects.get(pk=d)
        n=model_form(instance=data)
        if re.method=="POST":
            n=model_form(re.POST,re.FILES,instance=data)
            if n.is_valid():
                n.save()
                return redirect(adminmanageproduct)
        return render(re, 'admin/adminupdateproduct.html', {'data':n})
    return redirect(companylogin)

def adminupdateproduct(re):
    return render(re,'admin/adminupdateproduct.html')

def admindelete(re,d):
    if 'admin' in re.session:
        data=product.objects.get(pk=d)
        data.delete()
        messages.success(re,'product delete successfully')
        return redirect(adminmanageproduct)
    return redirect(login)
def deletecart(re,d):
    if 'user' in re.session:
        data=cart.objects.get(pk=d)
        data.delete()
        messages.success(re,'product delete  from  cart successfully')
        return redirect(usercart)
    return redirect(userlogin)

def reject(re,d):
    if 'admin' in re.session:
        data = company_reg.objects.get(pk=d)
        data.delete()
        messages.success(re, 'product delete successfully')
        return redirect(aprovals)
    return redirect(login)
def accept(re,d):
    if 'admin' in re.session:
       d= company_reg.objects.filter(pk=d).update(status="approved")
       return redirect(aprovals)
    return redirect(login)
def update_company_profile(re):
    if 'company' in re.session:
        data=company_reg.objects.get(company_username=re.session['company'])
        n=com_form(instance=data)
        print(n)
        if re.method=="POST":
            n=com_form(re.POST,re.FILES,instance=data)
            if n.is_valid():
                n.save()
                return redirect(companyprofile)
        return render(re, 'company/update_profile.html', {'data':n})
    return redirect(companylogin)

def update_companyprofile(re):
    return render(re,'company/_profile.html')
def usercontact(re):
    if 'user' in re.session:
        if re.method == "POST":
            a = re.POST['name']
            b = re.POST['email']
            c = re.POST['subject']
            d = re.POST['message']
            data =user_contact.objects.create(name=a, email=b, subject=c, message=d)
            data.save()
            return HttpResponse("<script>alert('message registered successfully')</script>")
        return render(re, 'user/user_condact.html')
    return redirect(login)
def companycontact(re):
    if 'company' in re.session:
        if re.method == "POST":
            a = re.POST['name']
            b = re.POST['email']
            c = re.POST['subject']
            d = re.POST['message']
            data =company_contact.objects.create(name=a, email=b, subject=c, message=d)
            data.save()
            return HttpResponse("<script>alert('message registered successfully')</script>")
        return render(re, 'company/company_contact.html')
    return redirect(login)
def vieworder(re,d):
    if 'admin' in re.session:
        data = order.objects.get(pk=d)
        n = order_form(instance=data)
        if re.method == "POST":
            n = order_form(re.POST, re.FILES, instance=data)
            if n.is_valid():
                n.save()
                return redirect(allorders)
        return render(re, 'admin/vieworder.html', {'data': n})
    return redirect(login)
def vieworder_cart(re,d):
    if 'admin' in re.session:
        data = order_cart.objects.get(pk=d)
        n = order_cart_form(instance=data)
        if re.method == "POST":
            n = order_cart_form(re.POST, re.FILES, instance=data)
            if n.is_valid():
                n.save()
                return redirect(allorders)
        return render(re, 'admin/vieworder_cart.html', {'data': n})
    return redirect(login)
def vieworderproduct(re):
    return render(re,'admin/vieworder.html')
def vieworder_cartproduct(re):
    return render(re,'admin/vieworder_cart.html')

def refund(request,d):
    amount = 500 * 100
    print(amount)
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    data=order.objects.get(pk=d)
    data.refund_status = 'paid'
    data.save()
    return render(request, "admin/refund.html", {'amount': amount})
def refund_cart(request,l,d):
        data=order_cart.objects.get(pk=l)
        amount = data.total_pprice * 100
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        data = order_cart.objects.get(pk=d)
        data.refund_status = 'paid'
        data.save()
        return render(request, "admin/refund_cart.html", {'amount': amount})
@csrf_exempt

def refundsuccess_cart(request):
    # usr = reg.objects.get(username=request.session['user'])
    # order_ids = request.session.get('order_ids', [])
    # for i in order_ids:
    #     c = i
    #     b = 'PAID'
    #     order.objects.filter(pk=c).update(payment_status=b)
    # send_mail('Payment Successful',
    #           f'Hey {usr.name}, Your payment was successful and your ordered items has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
    #           'settings.EMAIL_HOST_USER', [usr.email], fail_silently=False)
    # send_mail('New Order',
    #           f' {usr.name}, has placed a some new orders\nPlease review and update the order status',
    #           'settings.EMAIL_HOST_USER', ['aninaabraham01@gmail.com'], fail_silently=False)
    return render(request, "admin/refundpayment.html")


def refundsuccess(request):
    # order_ids = request.session.get('order_ids', [])
    # for i in order_ids:
    #     c = i
    #     b = 'PAID'
    #     order.objects.filter(pk=c).update(refund_status=b)
    # send_mail('Payment Successful',
    #           f'Hey {usr.name}, Your payment was successful and your ordered items has been successfully placed. \nWe are working on your order. \nOrder status will be updated soon.\n\nTHANK YOU.. \n\nBest regards,\nGAMER ZONE',
    #           'settings.EMAIL_HOST_USER', [usr.email], fail_silently=False)
    # send_mail('New Order',
    #           f' {usr.name}, has placed a some new orders\nPlease review and update the order status',
    #           'settings.EMAIL_HOST_USER', ['aninaabraham01@gmail.com'], fail_silently=False)
    return render(request, "admin/refundpayment.html")


from django.utils.crypto import get_random_string
from django.core.mail import send_mail
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            user = reg.objects.get(email=email)
            print(user)
        except:
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forget.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset =PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})


def forgot_password_c(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            company =company_reg.objects.get(company_email=email)
            print(company)
        except:
            messages.info(request, "Email id not registered")
            return redirect(forgot_password_c)
        # Generate and save a unique token
        token_c = get_random_string(length=4)
        PasswordReset_c.objects.create(company=company, token_c=token_c)

        # Send email with reset link
        reset_link1 = f'http://127.0.0.1:8000/reset/{token_c}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link1}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password_c)

    return render(request,'forget_c.html')

def reset_password_c(request,token_c):
    # Verify token and reset the password
    print(token_c)
    password_reset =PasswordReset_c.objects.get(token_c=token_c)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.company.company_password=new_password
            print(new_password)
            password_reset.company.save()
            # password_reset.delete()
            return redirect(companylogin)
    return render(request, 'reset_password_c.html', {'token_c': token_c})


# def all_products(re):
#     if 'admin' in re.session:
#         d = product.objects.all()
#         return render(re,'admin/all_products.html',{'d':d})
#     return redirect(companylogin)
def product_del(re,d):
    if 'admin' in re.session:
        data=product.objects.get(pk=d)
        data.delete()
        messages.success(re,'product delete successfully')
        return redirect(all_products)
    return redirect(login)
def search(re):
    item= re.POST['query']
    products = product.objects.filter(pname=item)
    print(products)
    print(item)
    return render(re, 'shop.html', {'data': products })