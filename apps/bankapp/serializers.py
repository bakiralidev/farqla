# apps/bankapp/serializers.py
from rest_framework import serializers
from decimal import Decimal, ROUND_HALF_UP
from .models import (
    Bank, Card, Credit, Deposit, Currency,
    App, P2POffer, CurrencyCode
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

class CurrencyConvertSerializer(serializers.Serializer):
    bank_id     = serializers.IntegerField()
    from_code   = serializers.ChoiceField(choices=CurrencyCode.choices)
    to_code     = serializers.ChoiceField(choices=CurrencyCode.choices)
    amount      = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )

    # Sotish / sotib olishni tanlash uchun
    operation   = serializers.ChoiceField(
        choices=(
            ("sell", "Sotish"),        # bank mijozga valyuta sotadi -> sell_rate
            ("buy", "Sotib olish"),    # bank mijozdan valyuta sotib oladi -> buy_rate
        )
    )

    bank_name   = serializers.CharField(read_only=True)
    result      = serializers.DecimalField(max_digits=18, decimal_places=4, read_only=True)

    def validate_bank_id(self, value):
        try:
            bank = Bank.objects.get(pk=value, is_active=True)
        except Bank.DoesNotExist:
            raise serializers.ValidationError("Bunday bank topilmadi.")
        self._bank = bank
        return value

    def validate(self, attrs):
        from_code = attrs["from_code"]
        to_code   = attrs["to_code"]

        if from_code == to_code:
            raise serializers.ValidationError("from_code va to_code bir xil bo‘lishi mumkin emas.")

        bank = getattr(self, "_bank", None)
        if bank is None:
            try:
                bank = Bank.objects.get(pk=attrs["bank_id"], is_active=True)
            except Bank.DoesNotExist:
                raise serializers.ValidationError({"bank_id": "Bunday bank topilmadi."})

        try:
            from_currency = Currency.objects.get(
                bank=bank,
                code=from_code,
                is_active=True
            )
        except Currency.DoesNotExist:
            raise serializers.ValidationError({"from_code": "Bu valyuta uchun kurs topilmadi."})

        try:
            to_currency = Currency.objects.get(
                bank=bank,
                code=to_code,
                is_active=True
            )
        except Currency.DoesNotExist:
            raise serializers.ValidationError({"to_code": "Bu valyuta uchun kurs topilmadi."})

        attrs["bank"] = bank
        attrs["from_currency"] = from_currency
        attrs["to_currency"] = to_currency
        return attrs

    def calculate(self):
        data       = self.validated_data
        amount     = Decimal(data["amount"])
        from_code  = data["from_code"]
        to_code    = data["to_code"]
        from_cur   = data["from_currency"]
        to_cur     = data["to_currency"]
        operation  = data["operation"]   # "sell" yoki "buy"

        # Qaysi kursni ishlatamiz
        def get_rate(cur):
            return cur.sell_rate if operation == "sell" else cur.buy_rate

        # 1) UZS -> Valyuta
        if from_code == CurrencyCode.UZS and to_code != CurrencyCode.UZS:
            rate = get_rate(to_cur)
            result = amount / rate

        # 2) Valyuta -> UZS
        elif to_code == CurrencyCode.UZS and from_code != CurrencyCode.UZS:
            rate = get_rate(from_cur)
            result = amount * rate

        # 3) Valyuta -> Valyuta (UZS orqali)
        else:
            # hozircha eski: from uchun buy_rate, to uchun sell_rate
            amount_in_uzs = amount * from_cur.buy_rate
            result = amount_in_uzs / to_cur.sell_rate

        result = result.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        return {
            "bank": data["bank"].name,
            "from_code": from_code,
            "to_code": to_code,
            "amount": amount,
            "operation": operation,
            "result": result,
        }
