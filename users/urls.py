from django.conf.urls import url
from users.views import *

users_patterns = [
    url(r'^login/$',login,name='login'),
    url(r'^logout/$',logout,name="logout"),
    url(r'^forgot-password/$',forgot_password,name='forgot-password'),
    url(r'^activate/$',account_activate,name="activate-account"),
    url(r'^register/$',register_account,name='register'),
    url(r'^get-account/$',perform_forgot_password,name='perform-forgot-password'),
    url(r'^profile/$',user_profile,name='profile')
]