from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SugurtaCompanyViewSet, SugurtaViewSet

router = DefaultRouter()
router.register(r"companies", SugurtaCompanyViewSet, basename="insurance-company")
router.register(r"sugurtalar", SugurtaViewSet, basename="insurance")

urlpatterns = [
    path("", include(router.urls)),
]
