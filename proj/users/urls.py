from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from users.views import signup, profile, MyLoginForm, contribution, delete_profile

urlpatterns = [
    path('signup/', signup, name='signup'),
    
    path('profile/', profile, name='profile'),
    path('profile/contribution/', contribution, name='contribution'),
    path('profile/delete/', delete_profile, name='delete_profile'),

    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=MyLoginForm), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', PasswordChangeView.as_view(template_name='users/password_change.html'),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
]
