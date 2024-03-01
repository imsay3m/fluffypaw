from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount


class UserRegistrationForm(UserCreationForm):
    image=forms.ImageField(required=False)
    class Meta:
        model=User
        fields=['username','password1','password2','first_name','last_name','email','image']
        widgets = {
            'username': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your username',
                'name':'username',
            }),
            'password1': forms.PasswordInput(attrs={
                'type':'password',
                'name':'password',
                'placeholder':'Enter Password*',
            }),
            'password2': forms.PasswordInput(attrs={
                'type':'password',
                'name':'confirmpassword',
                'placeholder':'Enter Confirm Password*',
            }),
            'first_name': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your First name',
                'name':'first_name',
            }),
            'last_name': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Enter your Last name',
                'name':'last_name',
            }),
            'email': forms.EmailInput(attrs={
                'type':'email', 
                'placeholder': 'Enter email address',
                'name':'email'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].initial = 'images/profile/user_avatar.png'

    def save(self,commit=True):
        our_user=super().save(commit=False)
        if commit==True:
            our_user.save()
            image = self.cleaned_data.get('image', 'images/profile/user_avatar.png')
            UserAccount.objects.create(
                user=our_user,
                image=image,
                account_no=100000+int(our_user.id),
            )
        return our_user


class UserUpdateForm(forms.ModelForm):
    image=forms.ImageField(required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # if user have an account
        if self.instance:
            try:
                user_account=self.instance.account
            except UserAccount.DoesNotExist:
                user_account=None
            if user_account:
                self.fields['image'].initial=user_account.image

    def save(self,commit=True):
        our_user=super().save(commit=False)
        if commit:
            our_user.save()

            user_account,created=UserAccount.objects.get_or_create(user=our_user)
            user_account.image=self.cleaned_data['image']
            user_account.save()
        return our_user