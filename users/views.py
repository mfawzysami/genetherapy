# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils import get_base_context
from django.shortcuts import render
from users.controllers import UserController
from django.shortcuts import redirect, HttpResponseRedirect, resolve_url
from django.contrib import messages
from django.contrib.messages import add_message
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm



@login_required
def user_profile(request):
    context = get_base_context()
    context['user'] = request.user
    return render(request, 'profile.html', context=context)


def login(request):
    context = get_base_context()
    controller = UserController(request)
    if request.method == 'POST' and controller.login():
        next = request.POST.get('next', None)
        if next is None or len(next) <= 0:
            return redirect(resolve_url('home'))
        else:
            return HttpResponseRedirect(next)
    return render(request, 'login.html', context=context)


def logout(request):
    controller = UserController(request)
    controller.logout()
    return redirect(resolve_url('home'))


def forgot_password(request):
    context = get_base_context()
    controller = UserController(request)
    try:
        if request.method == 'POST' and controller.forgot_password():
            add_message(request, messages.INFO, "An Email has been sent With instructions to recover your account.")
            return redirect(resolve_url("users:login"))
    except Exception as e:
        add_message(request, messages.ERROR, e.message)
    return render(request, "forgotpasswd.html", context)


def perform_forgot_password(request):
    base_context = get_base_context()
    controller = UserController(request)
    try:
        if request.method == 'POST' and controller.perform_forgot_password():
            add_message(request, messages.INFO, "Account Credentials has been changed Successfully , You may now login")
            return redirect(resolve_url("users:login"))
        if request.method == 'GET':
            _, user = controller.verify_link()
            base_context['user'] = user
            return render(request, "perform_forgot_password.html", context=base_context)

    except Exception as e:
        add_message(request, messages.ERROR, e.message)
        return redirect(resolve_url("users:login"))


def account_activate(request):
    controller = UserController(request)
    controller.activate_account()
    return redirect(resolve_url("users:login"))


def register_account(request):
    registerForm = RegisterForm(request.POST)
    context = get_base_context()
    context['form'] = registerForm
    controller = UserController(request)
    try:
        if request.method == 'POST' and registerForm.is_valid() and controller.register_account():
            return redirect(resolve_url("users:login"))
    except Exception as e:
        add_message(request, messages.ERROR, e.message)

    return render(request, "register_account.html", context=context)
