from django.urls import path, include
from rest_framework.routers import DefaultRouter  # ✅ Now included

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # ✅ Now declared
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]