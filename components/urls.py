from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'new/$',new_component,name='new-component')
]