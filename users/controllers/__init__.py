from users.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import add_message
from genetherapy.settings import SESSION_COOKIE_AGE
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q
from genetherapy.tasks import send_email_msg
from users.utilities import AccountTokenManager
from django.shortcuts import resolve_url
import pyotp as otp
from utils.recaptcha import validate_recaptcha


class UserController(object):
    def __init__(self, request):
        self.request = request
        self.token_manager = AccountTokenManager()


    def rest_login(self,username,password):
        if username is None or password is None:
            raise Exception("Invalid userName and/or password")
        current_user = authenticate(username=username, password=password)
        if not current_user:
            add_message(self.request, message="Invalid Login,  Please Try again", level=messages.INFO)
            return False
        else:
            if not current_user.is_active:
                add_message(self.request, message="You are inactive, please contact your system administrator",
                            level=messages.INFO)
                logout(self.request)
                return False
            login(self.request, current_user)
            remember_me = self.request.POST.get('remember-me', None)
            if remember_me is None or not remember_me == 'on':
                self.request.session.set_expiry(0)
            else:
                self.request.session.set_expiry(SESSION_COOKIE_AGE)
            return True


    def login(self):
        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password', None)
        if username is None or password is None:
            raise Exception("Invalid userName and/or password")
        current_user = authenticate(username=username, password=password)
        if not current_user:
            add_message(self.request,message="Invalid Login,  Please Try again",level=messages.INFO)
            return False
        else:
            if not current_user.is_active:
                add_message(self.request, message="You are inactive, please contact your system administrator",
                            level=messages.INFO)
                logout(self.request)
                return False
            login(self.request, current_user)
            remember_me = self.request.POST.get('remember-me', None)
            if remember_me is None or not remember_me == 'on':
                self.request.session.set_expiry(0)
            else:
                self.request.session.set_expiry(SESSION_COOKIE_AGE)
            return True


    def logout(self):
        logout(self.request)
        return True

    def perform_forgot_password(self):
        _ , current_user = self.verify_link()
        password = self.request.POST.get('password')
        confirm_password = self.request.POST.get('confirm_password')
        if not password == confirm_password:
            raise Exception("Password does not match")
        if not current_user:
            raise Exception("Invalid User")
        current_user.set_password(password)
        current_user.is_active = True
        current_user.save()
        return True

    def verify_link(self):
        code = self.request.GET.get('code',None)
        result , username = self.token_manager.verify_link_token(code)
        if not result:
            raise Exception("Invalid Link")
        return result , User.objects.filter(Q(username=username)).first()


    def forgot_password(self):
        user_email = self.request.POST.get('email',None)
        if not user_email:
            raise Exception("Invalid User Email")
        current_user = User.objects.filter(Q(email=user_email)).first()
        if not current_user:
            raise Exception("Invalid User Email")
        secret_hash = otp.random_base32()
        otpValue = self.token_manager.generate_temporary_token(secret_hash)
        current_user.secret_otp = otpValue
        current_user.secret_hash = secret_hash
        current_user.save()
        current_context = {
            "user" : current_user,
            'external_link': self.token_manager.generateExternalLink(current_user.username,
                                                                                  otpValue,resolve_url('users:perform-forgot-password'))
        }
        template = get_template('emails/forgot-password-email.html')
        html_message = template.render(current_context)
        send_email_msg.delay(subject="GeneTherapy - Forgot Password Email", message=html_message,
                             recipient_list=[current_user.email], html_message=True)
        return True


    def register_account(self):
        full_name = self.request.POST.get('fullname', None)
        email = self.request.POST.get('email', None)
        if User.objects.filter(Q(email=email)).exists():
            raise Exception("Email Address is already in use.")
        username = self.request.POST.get('username', None)
        if User.objects.filter(Q(username=username)).exists():
            raise Exception("Username is already in use.")
        password = self.request.POST.get('password', None)
        confirm_password = self.request.POST.get('confirm', None)
        agree_terms = self.request.POST.get('agree_terms', None)
        mobile = self.request.POST.get('mobile', None)
        company = self.request.POST.get('company', None)
        if User.objects.filter(Q(company=company)).exists():
            raise Exception("Company name already exists, please choose a different company name.")
        domain = self.request.POST.get('domain',None)
        if None in [full_name, email, username, password, confirm_password, mobile, company,domain]:
            raise Exception("Please fill all required fields")
        if password != confirm_password:
            raise Exception("Password does not match")
        # if agree_terms != 'on':
        #     raise Exception("Please agree on our Terms and conditions before proceeding")
        names = full_name.split(" ")
        firstname, lastname = names[0], " ".join(names[1:])
        new_user = User(first_name=firstname, last_name=lastname, email=email, username=username, mobile=mobile,
                        company=company,domain=domain)
        new_user.set_password(password)
        new_user.is_active = False
        new_user.save()
        add_message(self.request, messages.INFO,
                    "Account has been created , An email with activation link shall be sent to your email shortly")
        self.__send_activation_link__(new_user)
        return True


    def __send_activation_link__(self,current_user):
        secret_hash = otp.random_base32()
        otpValue = self.token_manager.generate_temporary_token(secret_hash)
        current_user.secret_otp = otpValue
        current_user.secret_hash = secret_hash
        current_user.save()
        current_context = {
            "user": current_user,
            'external_link': self.token_manager.generateExternalLink(current_user.username,
                                                                     otpValue,resolve_url("users:activate-account"))
        }
        template = get_template('emails/account_activation_email.html')
        html_message = template.render(current_context)
        send_email_msg.delay(subject="GeneTherapy - Account Activation Email", message=html_message,
                             recipient_list=[current_user.email], html_message=True)



    def activate_account(self):
        code = self.request.GET.get('code',None)
        if code is None or len(code) <= 1:
            raise Exception("Invalid or Expired Activation Link")
        result , username = self.token_manager.verify_link_token(code)
        if result:
            current_user = User.objects.filter(Q(username=username)).first()
            if not current_user:
                raise Exception("Invalid Activation Link - Bad User")
            current_user.is_active = True
            current_user.save()
            add_message(self.request,messages.INFO,"Account has been activated successfully")
            return True
        else:
            add_message(self.request,messages.ERROR,"Invalid or Expired Activation Link - Bad Token")
            return False
