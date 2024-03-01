from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegistrationView,UserUpdateView,UserAccountView,change_password,activate
urlpatterns = [
    path('',UserAccountView.as_view(),name='account'),
    path('edit/',UserUpdateView.as_view(),name='edit_account'),
    path('change_password/',change_password,name='change_password'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('active/<str:uid64>/<str:token>/', activate, name='activate'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
]