from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WallProfileViewSet

router = DefaultRouter()
router.register(r'profiles', WallProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
