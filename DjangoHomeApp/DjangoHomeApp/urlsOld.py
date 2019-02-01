from django.contrib import admin
from django.urls import path
import DjangoHomeApp.views
import ChatApp.views

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', ChatApp.views.UserViewSet)

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/', router.urls),

    # path('chat/api/', ChatApp.views.index),

    # path('chat', TemplateView.as_view(template_name="index.html")),
    # path('chat', DjangoHomeApp.views.index),
    # path('chat/login', DjangoHomeApp.views.index),
    # path('chat/register', DjangoHomeApp.views.index),
    path('chat/authenticate/', ObtainAuthToken.as_view())

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)