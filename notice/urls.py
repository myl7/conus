from django.urls import path

from . import views

app_label = 'notice'
urlpatterns = [
    path('create/', views.NoticeCreateView.as_view(), name='create')
]
