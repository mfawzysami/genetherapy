# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render , redirect , resolve_url
from django.contrib.auth.decorators import login_required
from utils import get_base_context
from datetime import datetime
from core import CoreDBManager
import json , time


@login_required
def new_component(request):
    base_context = get_base_context()
    full_submitted = request.POST.get('full',"0")
    if full_submitted and full_submitted == "1":
        title = request.POST.get('component_title','N/A')
        description = request.POST.get('component_description','N/A')
        component_type = request.POST.get('component_type','N/A')
        component_data = request.POST.get('component_data',None)
        base_context['data'] = {
            "title": title,
            "description": description,
            "component_type": component_type
        }
        if component_data:
            author = request.user.get_user_details()
            insertion_date =  time.mktime(datetime.now().timetuple())
            modified_date = insertion_date
            last_accessed = insertion_date
            component = json.loads(component_data)
            component['title'] = title
            component['description'] = description
            component['author'] = author
            component['insertion_date'] = insertion_date
            component['modified_date'] = modified_date
            component['last_accessed'] = last_accessed
            component['rating_count'] = 0
            component['views_count'] = 0
            component['type'] = component_type
            db_manager = CoreDBManager()
            results = db_manager.insert("genetherapy", "components", component)
            if results:
                return redirect(resolve_url("home"))

        return render(request, "new_component.html", context=base_context)




    else:
        post_data = {
            "title" : request.POST.get('component_title',"N/A"),
            "description" : request.POST.get('component_description','N/A'),
            "component_type": request.POST.get('component_type','N/A')
        }
        base_context['data'] = post_data

        return render(request,"new_component.html",context=base_context)


