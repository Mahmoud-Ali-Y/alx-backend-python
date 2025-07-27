from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter  # ✅ Now included

from .views import ConversationViewSet, MessageViewSet

# ✅ Base router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# ✅ Nested router: messages nested under conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),  # ✅ nested message routes
]