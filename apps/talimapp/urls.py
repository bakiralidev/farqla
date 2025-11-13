from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversitetViewSet, FakultetViewSet, UniverYonalishViewSet,
    XususiyMaktabViewSet, FanViewSet, MaktabYonalishViewSet
)

router = DefaultRouter()
router.register(r"universitetlar", UniversitetViewSet, basename="universitet")
router.register(r"fakultetlar", FakultetViewSet, basename="fakultet")
router.register(r"univer-yonalishlar", UniverYonalishViewSet, basename="univer-yonalish")
router.register(r"xususiy-maktablar", XususiyMaktabViewSet, basename="xususiy-maktab")
router.register(r"fanlar", FanViewSet, basename="fan")
router.register(r"maktab-yonalishlar", MaktabYonalishViewSet, basename="maktab-yonalish")

urlpatterns = [
    path("", include(router.urls)),
]
