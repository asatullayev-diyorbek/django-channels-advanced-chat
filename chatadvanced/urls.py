from django.urls import path
from .views import DashboardView, UserListView, ChatView


app_name = 'chatadvanced'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-list/<str:username>/', ChatView.as_view(), name='chat'),
]
