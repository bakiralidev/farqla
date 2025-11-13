from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimkartaViewSet
from apps.bankapp.views_clicks import go_redirect 
router = DefaultRouter()
router.register(r"simkartalar", SimkartaViewSet, basename="simkarta")

urlpatterns = [
    path("", include(router.urls)),
    path("go/<str:model_name>/<int:pk>/<str:field_name>/", go_redirect, name="mobilapp_go_redirect"),
]
