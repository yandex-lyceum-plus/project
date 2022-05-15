from django.urls import path
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from users.views import signup, profile, MyLoginForm


urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=MyLoginForm), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
]
