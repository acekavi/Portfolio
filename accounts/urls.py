from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import context

from django.utils.translation import gettext_lazy as _

app_name = "accounts"

# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(template_name='registration/form.html', extra_context=context.login), name='login'),
#     path('profile/', views.profile, name='profile'),
#     path('profile/edit/', views.edit, name='edit'),

#     path('register/', views.account_register, name='register'),
#     path ('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/form.html'), name='PwdChange'),
#     path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
#     path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html",
#                                                                 form_class=PwdResetForm), name="password_reset"),
#     path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
#         template_name='registration/password_reset_confirm.html', form_class=PwdResetConfirmForm), name="pwdresetconfirm"),
#     path('password_reset/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'registration/feedback.html', extra_context={
#         'title' : "Reset link sent",
#         'context' : "Password reset link sent to your email! Check your inbox and the spam folder.",
#     })),                                                         
#     # path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html",
#                                                                 #    form_class=PwdChangeForm), name='pwdforgot'),
#     path('delete_user/', views.deleteUser, name='deleteuser')
# ]

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'layouts/forms.html', extra_context = context.login, redirect_authenticated_user = True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login') ,name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name = 'layouts/forms.html', extra_context = context.pwdChangeForm, success_url="/user/login/"), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'layouts/forms.html', extra_context = context.pwdResetForm, email_template_name = 'layouts/reset-email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'layouts/feedback.html', extra_context = context.pwdResetDone), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'layouts/forms.html', extra_context = context.pwdResetConfirm, success_url='/user/login/'), name='password_reset_confirm'),

    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('delete_user/', views.deleteUser, name='delete_user'),
]
