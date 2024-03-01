from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import FormView,ListView,View
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from pet.models import Pet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Create your views here.
class UserRegistrationView(FormView):
    template_name='account/user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('account')

    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_active=False
        user=form.save()
        
        email_subject="Confirm Your Account"

        token=default_token_generator.make_token(user)
        print("Token: " + str(token))
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        print("UID: "+str(uid))
        domain=get_current_site(self.request).domain
        confirm_link=f"{domain}/account/active/{uid}/{token}"
        
        email_body=render_to_string('account/confirmation_mail.html',{"confirm_link":confirm_link})
        email=EmailMultiAlternatives(email_subject,'',to=[user.email])
        email.attach_alternative(email_body,'text/html')
        if email.send():
            messages.success(self.request,'You Have Registered Successfully, Check Your Email To Activate Account')
        else:
            messages.error(self.request,f'Problem Sending Mail to {user.email}, Check For Typos')
        return super().form_valid(form)

def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Thank You For Your Confirmation. Now You Can Log into Your Account')
        return redirect('login')
    else:
        messages.error(request,'Activation Link Is Invalid or Expired')
    return redirect('home')

class UserLoginView(LoginView):
    template_name="account/user_login.html"

    def form_valid(self,form):
        messages.success(self.request,'You Have Logged In Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account')

class UserLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

class UserAccountView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'account/user_account.html'
    context_object_name = 'data'

    def get_queryset(self):
        return Pet.objects.filter(adopter=self.request.user)

class UserUpdateView(LoginRequiredMixin,View):
    template_name = 'account/edit_account.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': user_form})

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            messages.success(self.request,'You Have Successfully Updated Your Account!')
            user_form.save()
            return redirect('account')
        return redirect('account')
    
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            pass_form = PasswordChangeForm(user=request.user, data=request.POST)
            if pass_form.is_valid():
                pass_form.save()
                update_session_auth_hash(
                    request, pass_form.user
                )  # pass will get updated
                messages.success(request, "Password Changed Successfully")
                return redirect("account")
        else:
            pass_form = PasswordChangeForm(user=request.user)
        return render(request, "account/user_change_password.html", {"form": pass_form})
    else:
        messages.warning(request, "Please Log In to Your Account")
        return redirect("login")