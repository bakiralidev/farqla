from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.filters import SearchFilter, OrderingFilter

try:
    # Agar django-filter o‘rnatilgan bo‘lsa
    HAS_DJANGO_FILTER = True
except Exception:
    DjangoFilterBackend = None
    HAS_DJANGO_FILTER = False

from .models import Simkarta
from .serializers import SimkartaSerializer


class SimkartaViewSet(ModelViewSet):
    """
    CRUD:
      - GET    /api/catalog/simkartalar/           (list)
      - POST   /api/catalog/simkartalar/           (create)
      - GET    /api/catalog/simkartalar/{id}/      (retrieve)
      - PUT    /api/catalog/simkartalar/{id}/      (update)
      - PATCH  /api/catalog/simkartalar/{id}/      (partial_update)
      - DELETE /api/catalog/simkartalar/{id}/      (destroy)
    """
    queryset = Simkarta.objects.all().order_by("name")
    serializer_class = SimkartaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # JSON + multipart (rasm upload uchun)
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    # qidirish / tartiblash / filter
    filter_backends = [SearchFilter, OrderingFilter] 
    search_fields = ["name", "tarif", "tavsif"]
    ordering_fields = ["name", "tarif_narxi", "created_at", "updated_at"]
    ordering = ["name"]
    if HAS_DJANGO_FILTER:
        filterset_fields = ["simkarta_turi"]
