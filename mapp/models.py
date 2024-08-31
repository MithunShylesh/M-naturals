from django.db import models


# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=20)
    ph_no=models.IntegerField()
    address=models.CharField(max_length=100)
    email=models.EmailField()
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.username
class company_reg(models.Model):
    company_name=models.CharField(max_length=20)
    company_address=models.CharField(max_length=100)
    company_email=models.EmailField()
    company_condactno=models.IntegerField()
    owner_name=models.CharField(max_length=20)
    owner_adharphoto=models.FileField()
    company_username=models.CharField(max_length=20)
    company_password=models.CharField(max_length=10)
    status=models.CharField(max_length=20)
    payment_status=models.CharField(max_length=20)
class contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
class product(models.Model):
    pname=models.CharField(max_length=20)
    company_details=models.ForeignKey(company_reg,on_delete=models.CASCADE)
    cost=models.IntegerField()
    stock=models.IntegerField()
    image=models.FileField()
    definition=models.CharField(max_length=500)
    status=models.CharField(max_length=20,default="pending")
class cart(models.Model):
    user_details=models.ForeignKey(reg,on_delete=models.CASCADE)
    product_details=models.ForeignKey(product,on_delete=models.CASCADE)
    company_details=models.ForeignKey(company_reg,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1,null=True)
    total_price=models.IntegerField(default=500,)
class wish(models.Model):
    user_details = models.ForeignKey(reg, on_delete=models.CASCADE)
    product_details = models.ForeignKey(product, on_delete=models.CASCADE)
    company_details = models.ForeignKey(company_reg, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True)
    total_price = models.IntegerField(default=500, )
class order(models.Model):
    user = models.ForeignKey(reg, on_delete=models.CASCADE)
    company_details=models.ForeignKey(company_reg, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=50)
    delivery_date = models.CharField(max_length=50)
    product_order = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20,null=True)
    purchase_date = models.CharField(max_length=50)
    product_status = models.CharField(max_length=50,null=True, default='Order Placed')
    shipping_status=models.CharField(max_length=30,null=True, default="at factory")
    instruction = models.CharField(max_length=50,null=True, default='Your Order Has Been Successfully Placed')
    refund_status = models.CharField(max_length=30, null=True, default="none")
class order_cart(models.Model):
    user = models.ForeignKey(reg, on_delete=models.CASCADE)
    company_details=models.ForeignKey(company_reg, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=50)
    delivery_date = models.CharField(max_length=50)
    product_order = models.ForeignKey(product, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=1)
    # total_price = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20,null=True)
    purchase_date = models.CharField(max_length=50)
    product_status = models.CharField(max_length=50,null=True, default='Order Placed')
    shipping_status=models.CharField(max_length=30,null=True, default="at factory")
    instruction = models.CharField(max_length=50,null=True, default='Your Order Has Been Successfully Placed')
    refund_status = models.CharField(max_length=30, null=True, default="none")
    total_pprice = models.IntegerField(default=0)
    total_quantity = models.CharField(max_length=10, null=True)
class subscription(models.Model):
    company_details = models.ForeignKey(company_reg, on_delete=models.CASCADE)
    amount=models.IntegerField()
    status = models.CharField(max_length=20, default="pending")

class user_contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=200)

class company_contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
class PasswordReset(models.Model):
    user=models.ForeignKey(reg, on_delete=models.CASCADE)
    token=models.CharField(max_length=10)
class PasswordReset_c(models.Model):
    company=models.ForeignKey(company_reg, on_delete=models.CASCADE)
    token_c=models.CharField(max_length=10)

