from django.urls import path
from .views import event_list, event_detail, event_create, event_update, event_delete, home,event_create_file, admin_login, admin_dashboard

urlpatterns = [
    path('home/', home, name="home"),
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('events/create/', event_create, name='event_create'),
    path('events/update/<int:pk>/', event_update, name='event_update'),
    path('events/delete/<int:pk>/', event_delete, name='event_delete'),
    path('events/create_file/', event_create_file, name='event_create_file'),
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]
