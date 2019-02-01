from django.contrib import admin
from ChatApp.models import Message, Chat

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = 'id', 'chat_id', 'user_id', 'time', 'content'
    list_display = 'id', 'chat_id', 'user_id', 'time', 'content'
    search_fields = 'id', 'chat_id', 'user_id', 'time', 'content'

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fields = 'id', 'participants'
    list_display = 'id', 'participants'
    search_fields = 'id', 'participants'