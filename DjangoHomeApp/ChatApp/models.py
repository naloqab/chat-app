from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
	participants = models.TextField()

	def number_of_participants(self):
		allParticipantsList = self.participants.split(",")
		return len(allParticipantsList)

class Message(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()