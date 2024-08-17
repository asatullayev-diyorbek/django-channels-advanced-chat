from django.contrib import admin
from .models import Profile, Message, ChatGroup


admin.site.register([Profile, Message, ChatGroup])
