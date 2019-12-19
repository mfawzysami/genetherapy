from django import forms
from captcha import fields as recaptcha

class RegisterForm(forms.Form):

    fullname = forms.CharField(max_length=1000,required=True,widget=forms.TextInput(attrs={"id":"fullname","name":"fullname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"id":"email","name":"email"}),required=True)
    mobile = forms.CharField(max_length=20,widget=forms.TextInput(attrs={"id":"mobile","name":"mobile"}),required=True)
    company = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"id":"company","name":"company"}),required=True)
    domain = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"id": "domain", "name": "domain"}),
                              required=True)
    username = forms.CharField(max_length=500,widget=forms.TextInput(attrs={"id":"username","name":"username"}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","name":"password"}),required=True)
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={"id":"confirm","name":"confirm"}),required=True)
    captcha = recaptcha.ReCaptchaField()