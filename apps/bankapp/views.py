# apps/bankapp/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Bank, Card, Credit, Deposit, Currency,
    App, P2POffer
)
from .serializers import (
    BankSerializer, CardSerializer, CreditSerializer,
    DepositSerializer, CurrencySerializer,
    AppSerializer, P2POfferSerializer
)
from .filters import (
    BankFilter, CardFilter, CreditFilter,
    DepositFilter, CurrencyFilter, P2PFilter
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencyConvertSerializer

# -------- Universal ruxsatlar --------
class DefaultPermissionMixin:
    permission_classes = [permissions.AllowAny]


# -------- Bank --------
class BankViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = Bank.objects.all().order_by("name")
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BankFilter
    search_fields = ["name", "address", "description", "phone", "website"]
    ordering_fields = ["name", "rating", "number_of_branches",
                       "number_of_satisfied_customers", "opening_date", "created_at"]
    ordering = ["-rating", "name"]


# -------- Card --------
class CardViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = Card.objects.select_related("bank").all()
    serializer_class = CardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CardFilter
    search_fields = ["name", "bank__name", "system"]
    ordering_fields = ["interest_rate", "period_months", "amount",
                       "cashback_percent", "issuance_fee", "monthly_service_fee", "created_at"]
    ordering = ["bank__name", "name"]


# -------- Credit --------
class CreditViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = Credit.objects.select_related("bank").all()   # ✅ to'g'ri: select_related
    serializer_class = CreditSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CreditFilter
    search_fields = ["name", "bank__name", "purpose", "credit_type", "documents_note"]
    ordering_fields = ["interest_rate", "period_months", "amount", "down_payment",
                       "grace_period_months", "early_repayment_fee_percent", "created_at"]
    ordering = ["interest_rate"]


# -------- Deposit --------
class DepositViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = Deposit.objects.select_related("bank").all()
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = DepositFilter
    search_fields = ["name", "bank__name", "deposit_type"]
    ordering_fields = ["interest_rate", "period_months", "min_amount", "max_amount", "created_at"]
    ordering = ["-interest_rate"]


# -------- Currency --------
class CurrencyViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = Currency.objects.select_related("bank").all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CurrencyFilter
    search_fields = ["bank__name", "code", "name"]
    ordering_fields = ["buy_rate", "sell_rate", "change_percent", "updated_at_api", "created_at"]
    ordering = ["code"]


# -------- App --------
class AppViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # Agar App uchun maxsus FilterSet kerak bo'lsa, alohida qo'shamiz.
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


# -------- P2P Offer --------
class P2POfferViewSet(DefaultPermissionMixin, viewsets.ModelViewSet):
    queryset = P2POffer.objects.select_related("app").all()
    serializer_class = P2POfferSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = P2PFilter
    search_fields = ["app__name", "from_scheme", "to_scheme", "commission_note", "description"]
    ordering_fields = ["commission_value", "sort_order", "starts_at", "ends_at", "created_at"]
    ordering = ["app__name", "sort_order"]




class CurrencyConvertAPIView(APIView):
    """
    POST /api/currency/convert/
    """
    def post(self, request, *args, **kwargs):
        serializer = CurrencyConvertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result_data = serializer.calculate()

        return Response(result_data, status=status.HTTP_200_OK)
