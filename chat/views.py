from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ChatGroup
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def chat(request, username):
    users = User.objects.exclude(id=request.user.id)
    user1 = User.objects.get(username=request.user.username)
    user2 = User.objects.get(username=username)

    chat_group = ChatGroup.objects.filter(users=user1).filter(users=user2).first()

    if not chat_group:
        chat_group = ChatGroup.objects.create(
            name=f"chat_between_{user1.username}_and_{user2.username}"
        )
        chat_group.users.add(user1, user2)

    context = {
        'users': users,
        'user1': user1,
        'user2': user2,
        'chatgroup': chat_group
    }
    return render(request, 'chat.html', context)
