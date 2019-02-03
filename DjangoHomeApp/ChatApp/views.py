from django.contrib.auth.models import User
from rest_framework import viewsets, status
from ChatApp.models import Message, Chat
from ChatApp.serializers import MessageSerializer, ChatSerializer, UserSerializer

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import list_route

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def loggedinuser(self, request):
        tokenString = request.META['HTTP_AUTHORIZATION']

        tokenString = tokenString.split(' ')[1]

        try:
            user = Token.objects.get(key=tokenString).user
            serializer = UserSerializer(user)
            response = serializer.data
            return Response(response, status = status.HTTP_200_OK)

        except:
            return Response({'message': 'Could not match token with user'}, status = status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def friends(self, request):
        try:
            user_id = request.GET['user_id']

            content = Chat.objects.extra(where=['FIND_IN_SET({}, participants)'.format(user_id)])
            serializer = ChatSerializer(content, many=True)
            friends = []
            for chat in serializer.data:
                participants_ids = chat['participants'].split(",")
                for participants_id in participants_ids:
                    if user_id != participants_id:
                        friend_user_id = int(participants_id)
                # friend_user_id = int(chat['participants'].replace(",", "").replace(str(user_id), ""))
                content = User.objects.get(id=friend_user_id)
                serializer = UserSerializer(content, many=False)
                friend = serializer.data
                friends.append(friend)

            return Response({'friends': friends}, status = status.HTTP_200_OK)

        except:
            return Response({'message':'No friends found.'}, status = status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def chatMessages(self, request):
        # try:
        if True:
            user_id = request.GET['user_id']
            chat_id = request.GET['chat_id']

            participants = Chat.objects.get(id=chat_id).participants

            participants = participants.split(",")

            for participant in participants:
                if int(participant) != int(user_id):
                    friendUserInfo = User.objects.get(id=participant)

            serializer = UserSerializer(friendUserInfo)
            friendUserInfo = serializer.data

            content = Message.objects.filter(chat_id=chat_id).order_by('-id')[:50]
            serializer = MessageSerializer(content, many=True)

            messageObjects = serializer.data[::-1]

            for messageObject in messageObjects:
                messageObject['username'] = User.objects.get(id=messageObject['user_id']).username

            return Response({'friendUserInfo':friendUserInfo, 'messageObjects':messageObjects}, status = status.HTTP_200_OK)
            
        # except Exception as e:
        #     return Response({'message':str(e)}, status = status.HTTP_400_BAD_REQUEST)
            
    @list_route(methods=['post'])
    def sendMessage(self, request):
        try:
            user_id = request.data['user_id']
            chat_id = request.data['chat_id']
            messageContent = request.data['messageContent']

            Message(chat_id=chat_id, user_id=user_id, content=messageContent).save()
            return Response(status = status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'message':str(e)}, status = status.HTTP_400_BAD_REQUEST)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def lastChat(self, request):
        try:
            loggedinuser_id = request.GET['user_id']
            chat_id = Message.objects.extra(where=["time = (select max(time) from chatapp_message where user_id = {})".format(loggedinuser_id)])[0].chat_id
            return Response({'chat_id': chat_id}, status = status.HTTP_200_OK)

        except:
            return Response({'message': 'No chat found.'}, status = status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def newChat(self, request):
        username = request.data['username']
        friend_username = request.data['friend_username']

        if friend_username == username:
            return Response({'message':"User entered their own username."}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            friend_user = User.objects.get(username=friend_username)
        except:
            return Response({'message':"User not found."}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            # the second where clause can have a None when using dev mode.
            chat_id = Chat.objects.extra(where=['FIND_IN_SET({}, participants)'.format(friend_user.id)]).extra(where=['FIND_IN_SET({}, participants)'.format(user.id)])[0].id

        except:
            Chat(participants=str(friend_user.id)+","+str(user.id)).save()
            chat_id = Chat.objects.extra(where=["FIND_IN_SET({0}, participants)".format(user.id), "FIND_IN_SET({0}, participants)".format(friend_user.id)])[0].id

        return Response({'chat_id': chat_id}, status = status.HTTP_200_OK)