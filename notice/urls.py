from django.urls import path

from . import views

app_name = 'notice'
urlpatterns = [
    path('create/', views.NoticeCreateView.as_view(), name='create'),
    path('list/send/', views.NoticeSendListView.as_view(), name='list_send'),
    path('list/recv/', views.NoticeRecvListView.as_view(), name='list_recv')
]
