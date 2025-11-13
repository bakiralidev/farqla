from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternetProvayderViewSet, QurilmaViewSet

router = DefaultRouter()
router.register(r"provayderlar", InternetProvayderViewSet, basename="internet-pro")
router.register(r"qurilmalar", QurilmaViewSet, basename="qurilma")

urlpatterns = [
    path("", include(router.urls)),
]
