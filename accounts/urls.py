from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts.views import CustomLoginView, SignUpView, profile_view, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile_view, name='profile_view'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
]