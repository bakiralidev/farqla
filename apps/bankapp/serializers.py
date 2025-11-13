# apps/bankapp/serializers.py
from rest_framework import serializers
from .models import (
    Bank, Card, Credit, Deposit, Currency,
    App, P2POffer
)


# -------- Base Serializer --------
class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ["id", "is_active", "sort_order", "created_at", "updated_at"]


# -------- Bank --------
class BankSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Bank
        fields = "__all__"


# -------- Card --------
class CardSerializer(BaseModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Card
        fields = "__all__"


# -------- Credit --------
class CreditSerializer(BaseModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Credit
        fields = "__all__"


# -------- Deposit --------
class DepositSerializer(BaseModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Deposit
        fields = "__all__"


# -------- Currency --------
class CurrencySerializer(BaseModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Currency
        fields = "__all__"


# -------- App --------
class AppSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = App
        fields = "__all__"


# -------- P2P Offer --------
class P2POfferSerializer(BaseModelSerializer):
    app_name = serializers.CharField(source="app.name", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = P2POffer
        fields = "__all__"
