from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import SugurtaCompany, Sugurta
from .serializers import SugurtaCompanySerializer, SugurtaSerializer

class BasePermissionMixin:
    permission_classes = [IsAuthenticatedOrReadOnly]

class BaseFilterMixin:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

class SugurtaCompanyViewSet(BasePermissionMixin, BaseFilterMixin, ModelViewSet):
    queryset = SugurtaCompany.objects.all().order_by("name")
    serializer_class = SugurtaCompanySerializer
    filterset_fields = ["name"]
    search_fields = ["name", "address", "company_about"]
    ordering_fields = ["name"]

class SugurtaViewSet(BasePermissionMixin, BaseFilterMixin, ModelViewSet):
    queryset = (
        Sugurta.objects
        .select_related("sugurta_company")
        .all()
        .order_by("sugurta_company__name", "name")
    )
    serializer_class = SugurtaSerializer
    # filter (CRUD uchun qulay) — kompaniya bo‘yicha, turlar, shaxs roli
    filterset_fields = ["sugurta_company", "sugurta_turi", "shaxs_roli"]
    # qidiruv — nom va havola
    search_fields = ["name", "link", "sugurta_company__name"]
    # tartiblash — kerakli ustunlar
    ordering_fields = ["name", "sugurta_company__name"]
