from django.urls import path
from .views import event_list, event_create, event_update, event_delete,home

urlpatterns = [
    path('home',home,name="home"),
    path('', event_list, name='event_list'),
    path('create/', event_create, name='event_create'),
    path('update/<int:pk>/', event_update, name='event_update'),
    path('delete/<int:pk>/', event_delete, name='event_delete'),
]
