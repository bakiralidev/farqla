from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.filters import SearchFilter, OrderingFilter

# django-filter ixtiyoriy
try:
    from django_filters.rest_framework import DjangoFilterBackend
    HAS_DJANGO_FILTER = True
except Exception:
    DjangoFilterBackend = None
    HAS_DJANGO_FILTER = False

from .models import InternetProvayder, Qurilma
from .serializers import InternetProvayderSerializer, QurilmaSerializer


class InternetProvayderViewSet(ModelViewSet):
    """
    - GET    /api/catalog/provayderlar/
    - POST   /api/catalog/provayderlar/
    - GET    /api/catalog/provayderlar/{id}/
    - PUT    /api/catalog/provayderlar/{id}/
    - PATCH  /api/catalog/provayderlar/{id}/
    - DELETE /api/catalog/provayderlar/{id}/
    """
    queryset = InternetProvayder.objects.all().order_by("name")
    serializer_class = InternetProvayderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    base_backends = [SearchFilter, OrderingFilter]
    filter_backends = base_backends + ([DjangoFilterBackend] if HAS_DJANGO_FILTER else [])
    search_fields = ["name", "tarif", "tavsifi"]
    ordering_fields = ["name", "tarif_narxi"]
    ordering = ["name"]
    if HAS_DJANGO_FILTER:
        filterset_fields = ["name"]  # xohlasangiz kengaytiring


class QurilmaViewSet(ModelViewSet):
    """
    - GET    /api/catalog/qurilmalar/
    - POST   /api/catalog/qurilmalar/
    - GET    /api/catalog/qurilmalar/{id}/
    - PUT    /api/catalog/qurilmalar/{id}/
    - PATCH  /api/catalog/qurilmalar/{id}/
    - DELETE /api/catalog/qurilmalar/{id}/
    """
    queryset = Qurilma.objects.select_related("internet_provayder").all().order_by("internet_provayder__name", "name")
    serializer_class = QurilmaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    base_backends = [SearchFilter, OrderingFilter]
    filter_backends = base_backends + ([DjangoFilterBackend] if HAS_DJANGO_FILTER else [])
    search_fields = ["name", "model", "tavsifi", "internet_provayder__name"]
    ordering_fields = ["name", "model", "narxi", "internet_provayder__name"]
    ordering = ["internet_provayder__name", "name"]
    if HAS_DJANGO_FILTER:
        filterset_fields = ["internet_provayder"]  # ?internet_provayder=ID
