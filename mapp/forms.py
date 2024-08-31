from django import forms
from .models import*

class model_form(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'
class reg_form(forms.ModelForm):
    class Meta:
        model=reg
        fields='__all__'
class com_form(forms.ModelForm):
    class Meta:
        model=company_reg
        fields='__all__'

class order_form(forms.ModelForm):
    class Meta:
        model=order
        fields='__all__'
class order_cart_form(forms.ModelForm):
    class Meta:
        model=order_cart
        fields='__all__'