# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils import get_base_context

@login_required
def new_component(request):
    base_context = get_base_context()
    post_data = {
        "title" : request.POST.get('component_title',"N/A"),
        "description" : request.POST.get('component_description','N/A')
    }
    base_context['data'] = post_data
    return render(request,"new_component.html",context=base_context)


