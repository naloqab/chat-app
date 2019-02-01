from rest_framework import serializers
from ChatApp.models import Message, Chat
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = 'id', 'chat_id', 'user_id', 'time', 'content'

class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = 'id', 'participants', 'number_of_participants'

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = 'id', 'username', 'first_name', 'last_name', 'email', 'password'
		extra_kwargs = {'password': {'write_only':True, 'required':True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user