from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from ChatApp.models import Message, Chat
from ChatApp.serializers import MessageSerializer, ChatSerializer, UserSerializer
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from django.views.decorators.csrf import csrf_protect, requires_csrf_token
# from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import get_token

# @csrf_protect
# @requires_csrf_token
# @csrf_exempt

# {"method":"register", "username":"test", "password":"test", "firstName":"test", "lastName":"test", "email":"test"}
# {"method":"logout"}

@api_view(['GET', 'POST'])
def index(request):
	if request.method == 'POST':
		# body_unicode = request.body.decode('utf-8')
		# body = json.loads(body_unicode)
		body = request.data

		if 'method' in body:
			method = body['method']
			
			if method == 'login':
				username = body['username']
				password = body['password']
				
				user = authenticate(username=username, password=password)
				
				if user is not None:
					if user.is_active:
						login(request, user)
						return Response({'success':True, 'username':request.user.username})
					else:
						return Response({'success':False, 'message':'User is inactive.'})
				else:
					return Response({'success':False, 'message':'No backend authenticated the credentials.'})

			
			elif method == 'logout':
				try:
					logout(request)
					return Response({'success':True})
					
				except Exception as e:
					return Response({'success':False, 'message':str(e)})
				

			elif method == 'register':
				firstName = body['firstName']
				lastName = body['lastName']
				email = body['email']
				username = body['username']
				password = body['password']
				
				try:
					user = User.objects.create_user(first_name=firstName, last_name=lastName, email=email, username=username.lower(), password=password)
					return Response({'success':True})
					
				except Exception as e:
					return Response({'success':False, 'message':str(e)})
				

			elif method == 'sendMessage_dev':
				content = body['content']
				
				try:
					Message(chat_id=1, user_id=9, content=content).save()
					return Response({'success':True})
					
				except Exception as e:
					return Response({'success':False, 'message':str(e)})
				

			elif method == 'sendMessage':
				chatID = body['chatID']
				content = body['content']
				
				try:
					Message(chat_id=chatID, user_id=request.user.id, content=content).save()
					return Response({'success':True})
					
				except Exception as e:
					return Response({'success':False, 'message':str(e)})


			elif method == 'delete':
				User.objects.get(username=request.user.username).delete()
				

			else:
				return Response({'success':False, 'message':"Method unavailable."})
		else:
			return Response({'success':False, 'message':"No post method requested."})
			

	elif request.method == 'GET':
		body = request.GET
		
		if 'method' in body:
			method = body['method']

			if method == 'new_chat':
				friend_username = body['friend_username']

				if friend_username == request.user.username:
					return Response({'success':False, 'message':"User entered their own username."})

				try:
					friend_user = User.objects.get(username=friend_username)
				except:
					return Response({'success':False, 'message':"User not found."})
				
				try:
					# the second where clause can have a None when using dev mode.
					chat_id = Chat.objects.extra(where=['FIND_IN_SET({}, participants)'.format(friend_user.id)]).extra(where=['FIND_IN_SET({}, participants)'.format(request.user.id)])[0].id

				except:
					Chat(participants=str(friend_user.id)+","+str(request.user.id)).save()
					chat_id = Chat.objects.extra(where=["FIND_IN_SET({0}, participants)".format(request.user.id), "FIND_IN_SET({0}, participants)".format(friend_user.id)])[0].id

				return Response({'success':True, 'chatID':chat_id})

			elif method == 'new_chat_dev':
				friend_username = body['friend_username']

				try:
					friend_user = User.objects.get(username=friend_username)
				except:
					return Response({'success':False, 'message':"User not found."})
				
				try:
					chat_id = Chat.objects.extra(where=['FIND_IN_SET({}, participants)'.format(friend_user.id)]).extra(where=['FIND_IN_SET({}, participants)'.format(9)])[0].id

				except:
					Chat(participants=str(friend_user.id)+","+str(9)).save()
					chat_id = Chat.objects.extra(where=["FIND_IN_SET({0}, participants)".format(9), "FIND_IN_SET({0}, participants)".format(friend_user.id)])[0].id

				return Response({'success':True, 'chatID':chat_id})


			elif method == 'get_messages':
				chatID = body['chatID']
				try:
					participants = Chat.objects.get(id=chatID).participants

					participants = participants.split(",")

					if participants[0] == str(request.user.id):
						friendFirstName = User.objects.get(id=participants[1]).first_name
					else:
						friendFirstName = User.objects.get(id=participants[0]).first_name

					content = Message.objects.filter(chat_id=chatID).order_by('-id')[:100]
					serializer = MessageSerializer(content, many=True)

					messageObjects = serializer.data[::-1]

					for messageObject in messageObjects:
						messageObject['username'] = User.objects.get(id=messageObject['user_id']).username

					return Response({'success':True, 'friendFirstName':friendFirstName, 'messageObjects':messageObjects})
					
				except Exception as e:
					return Response({'success':False, 'message':str(e)})


			elif method == 'get_loggedin_user_dev':

				userObject = {"id": 9, "username": "naloqab", "first_name": "Naser", "last_name": "Aloqab", "email": "n.aloqab@gmail.com"}
				return Response({'success':True, 'user':userObject})


			elif method == 'get_loggedin_user':

				content = request.user
				serializer = UserSerializer(content, many=False)

				if request.user.username != "":
					return Response({'success':True, 'user':serializer.data})
				else:
					return Response({'success':False, 'message':'No user logged in.'})


			elif method == 'get_last_chat_dev':
				try:
					chat_id = Message.objects.extra(where=["time = (select max(time) from chatapp_message where user_id = {})".format(9)])[0].chat_id
					return Response({'success':True, 'chatID':chat_id})

				except:
					return Response({'success':False, 'message':'No chat found.'})


			elif method == 'get_last_chat':
				try:
					chat_id = Message.objects.extra(where=["time = (select max(time) from chatapp_message where user_id = {})".format(request.user.id)])[0].chat_id
					return Response({'success':True, 'chatID':chat_id})

				except:
					return Response({'success':False, 'message':'No chat found.'})

			elif method == 'get_friends':
				try:
					content = Chat.objects.extra(where=['FIND_IN_SET({}, participants)'.format(request.user.id)])
					serializer = ChatSerializer(content, many=True)
					friends = []
					for chat in serializer.data:
						friend_user_id = int(chat['participants'].replace(",", "").replace(str(request.user.id), ""))
						content = User.objects.get(id=friend_user_id)
						serializer = UserSerializer(content, many=False)
						friend = serializer.data
						friends.append(friend)

					return Response({'success':True, 'friends':friends})

				except:
					return Response({'success':False, 'message':'No friends found.'})


			elif method == 'check_other_chats':
				try:
					chat_id = Message.objects.extra(where=["time = (select max(time) from chatapp_message where user_id = {})".format(request.user.id)])[0].chat_id
					return Response({'success':True, 'chatID':chat_id})

				except:
					return Response({'success':False, 'message':'No chat found.'})


			
		else:
			return Response({'success':False, 'message':"No get method requested."})
		
		
		
		
		
		
		
		
		














		
		
		
		# {"method":"login", "username":"naloqab", "password":"Kaka2233!"}
		
		
		# {"method":"send"}
		
		
			
			# if method == 'create':
				# Message(chat_id=1, user_id=1, content='testing').save()
				# user = User.objects.create_user(username="naloqab", password="Kaka2233!", email="n.aloqab@gmail.com")
				# content = None
		
				# if request.user.is_authenticated:
					# content = request.META['REMOTE_USER']
					# content = 'User authenticated.'
				# else:
					# content = 'User not authenticated.'
		
		
		# Message(chat_id=1, user_id=1, content=body_unicode).save()
		
		# if content:
			# serializer = ChatAppSerializer(content, many=True)
			# return Response(serializer.data)
			
		# else:
			# return Response("No get method requested.")
	
	
	
	
	
	

			# method_requested = request.GET['method']
			# Message(chat_id=1, user_id=1, content='testing').save()
		
		# if 'value' in request.GET:
			# value = request.GET['value']
		# else:
			# value = ''
		
		# Message.objects.all().delete()
		
		# for object in result:
			# object.delete()
			# object.save()