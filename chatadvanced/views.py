from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        return render(request, 'base1.html')


class UserListView(LoginRequiredMixin, ListView):
    def get(self, request, *args):
        return render(request, 'user-list.html')


class ChatView(LoginRequiredMixin, ListView):
    def get(self, request, **kwargs):
        username = kwargs['username']
        return render(request, 'chat1.html')

