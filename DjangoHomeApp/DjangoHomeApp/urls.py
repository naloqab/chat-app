from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
import ChatApp.views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import ObtainAuthToken

from django.views.generic import TemplateView, RedirectView



router = routers.DefaultRouter()

router.register(r'users', ChatApp.views.UserViewSet)
router.register(r'messages', ChatApp.views.MessageViewSet)
router.register(r'chats', ChatApp.views.ChatViewSet)

urlpatterns = [
    path('admin', admin.site.urls),
    path('', RedirectView.as_view(url='chat')),
    path('chat', TemplateView.as_view(template_name="index.html")),
    path('chat/login', TemplateView.as_view(template_name="index.html")),
    path('chat/register', TemplateView.as_view(template_name="index.html")),
    path('chat/api/authenticate/', ObtainAuthToken.as_view()),
    path('chat/api/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)