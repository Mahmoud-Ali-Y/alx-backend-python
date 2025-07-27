from django.shortcuts import render
from rest_framework import viewsets, status, filters  # ✅ filters added here
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name']  # ✅ optional search

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])
        if not isinstance(participant_ids, list):
            return Response({"error": "participant_ids must be a list."}, status=400)

        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants:
            return Response({"error": "No valid participants found."}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.participants.add(request.user)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."}, status=400)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({"error": "Not a participant."}, status=403)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)