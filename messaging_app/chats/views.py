from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])

        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"error": "participant_ids must be a list of user IDs."}, status=400)

        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response({"error": "Valid users required."}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.participants.add(request.user)  # include self
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."}, status=400)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."}, status=403)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)