from django.urls import path, reverse_lazy
from .views import my_profile_view
from .views import UserFormView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'profiles'

urlpatterns = [
    path('', my_profile_view, name='my'),
    path('register/', UserFormView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(template_name='profiles/password_reset_form.html',
                                                      email_template_name='profiles/password_reset_email.html',
                                                      success_url='password-reset-done'
                                                      ),
         name='password-reset'),
    path('password-reset/password-reset-done/', PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html',
                                                                                      success_url=reverse_lazy('profiles:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), name='password_reset_complete'),
]

