from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Universitet, Fakultet, UniverYonalish,
    XususiyMaktab, Fan, MaktabYonalish
)
from .serializers import (
    UniversitetSerializer, FakultetSerializer, UniverYonalishSerializer,
    XususiyMaktabSerializer, FanSerializer, MaktabYonalishSerializer
)

class BasePermFilterMixin:
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class UniversitetViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = Universitet.objects.all().order_by("name")
    serializer_class = UniversitetSerializer
    filterset_fields = ["tashkil_yili"]
    search_fields = ["name", "desc", "address", "web_sayt"]
    ordering_fields = ["name", "tashkil_yili", "created_at"]

class FakultetViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = Fakultet.objects.select_related("universitet").all().order_by("universitet__name", "name")
    serializer_class = FakultetSerializer
    filterset_fields = ["universitet", "tashkil_yili"]
    search_fields = ["name", "dekan", "telefon", "email", "desc", "universitet__name"]
    ordering_fields = ["name", "tashkil_yili", "universitet__name", "created_at"]

class UniverYonalishViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = (
        UniverYonalish.objects
        .select_related("fakultet", "fakultet__universitet")
        .all()
        .order_by("fakultet__universitet__name", "fakultet__name", "name")
    )
    serializer_class = UniverYonalishSerializer
    filterset_fields = ["fakultet", "talim_turi", "grant_mavjudmi"]
    search_fields = ["name", "desc", "fakultet__name", "fakultet__universitet__name"]
    ordering_fields = ["name", "talim_muddati_y", "kontrakt_summasi", "fakultet__universitet__name"]

class XususiyMaktabViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = XususiyMaktab.objects.all().order_by("name")
    serializer_class = XususiyMaktabSerializer
    filterset_fields = ["tashkil_yili"]
    search_fields = ["name", "mudir", "desc", "address", "web_sayt"]
    ordering_fields = ["name", "tashkil_yili", "created_at"]

class FanViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = Fan.objects.all().order_by("name")
    serializer_class = FanSerializer
    filterset_fields = []
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]

class MaktabYonalishViewSet(BasePermFilterMixin, ModelViewSet):
    queryset = (
        MaktabYonalish.objects
        .select_related("maktab")
        .prefetch_related("fanlar")
        .all()
        .order_by("maktab__name", "name")
    )
    serializer_class = MaktabYonalishSerializer
    filterset_fields = ["maktab", "grant_mavjudmi", "fanlar"]
    search_fields = ["name", "desc", "maktab__name", "fanlar__name"]
    ordering_fields = ["name", "talim_muddati_o", "oqish_summasi", "maktab__name"]
