from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('validate/', views.validate_view, name='validate'),
    path('logout/', views.logout_view, name='logout'),
    path('contact-info/email/validate/', views.validate_email_view, name='validate_email'),
    path('contact-info/email/update/', views.ContactInfoUpdateEmailView.as_view(), name='update_email')
]
