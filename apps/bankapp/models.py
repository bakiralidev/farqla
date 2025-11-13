# apps/bankapp/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from .models_clicks import URLClickStat
# -------------------- Base --------------------

class BaseModel(models.Model):
    is_active  = models.BooleanField(default=True, db_index=True)
    sort_order = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -------------------- Bank & helpers --------------------

class Bank(BaseModel):
    name               = models.CharField(max_length=150, unique=True)
    slug               = models.SlugField(unique=True)
    address            = models.TextField(blank=True)
    longitude          = models.FloatField(null=True, blank=True)
    latitude           = models.FloatField(null=True, blank=True)
    description        = models.TextField(blank=True)
    number_of_branches = models.PositiveIntegerField(default=0)
    number_of_satisfied_customers = models.PositiveIntegerField(default=0)
    opening_date       = models.DateField(null=True, blank=True)
    website            = models.URLField(blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="bank_clicks")
    phone              = models.CharField(max_length=40, blank=True)
    rating             = models.DecimalField(
        max_digits=3, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    image              = models.ImageField(upload_to="bank_images/", blank=True, null=True)

    class Meta:
        db_table = "bank"
        ordering = ["name"]
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active", "sort_order"]),
        ]

    def __str__(self):
        return self.name


class CurrencyCode(models.TextChoices):
    UZS = "UZS", _("UZS")
    USD = "USD", _("USD")
    EUR = "EUR", _("EUR")
    RUB = "RUB", _("RUB")
    KZT = "KZT", _("KZT")


# -------------------- Cards --------------------

class CardSystem(models.TextChoices):
    UZCARD     = "uzcard", _("Uzcard")
    HUMO       = "humo",   _("Humo")
    VISA       = "visa",   _("VISA")
    MASTERCARD = "mc",     _("Mastercard")


class CardType(models.TextChoices):
    VIRTUAL = "virtual", _("Virtual")
    PLASTIC = "plastic", _("Plastic")


class Card(BaseModel):
    bank          = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="cards")
    name          = models.CharField(max_length=120)
    system        = models.CharField(max_length=20, choices=CardSystem.choices, db_index=True)
    currency_code = models.CharField(max_length=3, choices=CurrencyCode.choices, default=CurrencyCode.UZS)
    # Ba'zi kartalarda foiz yo‘q bo‘lishi mumkin (0–100)
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    period_months = models.PositiveIntegerField(null=True, blank=True)
    amount        = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    card_type     = models.CharField(max_length=20, choices=CardType.choices)
    fast_issuance = models.BooleanField(default=False)

    issuance_fee          = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_service_fee   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cashback_percent      = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    open_link     = models.URLField(blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="card_clicks")

    image         = models.ImageField(upload_to="card_images/", blank=True, null=True)

    class Meta:
        db_table = "card"
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")
        ordering = ["bank__name", "name"]
        indexes = [
            models.Index(fields=["bank", "system", "card_type"]),
            models.Index(fields=["currency_code"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="card_amount_nonneg",
                check=models.Q(amount__isnull=True) | models.Q(amount__gte=0),
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.bank.name}"


# -------------------- Credits --------------------

class CreditPurpose(models.TextChoices):
    CONSUMER = "consumer", _("Consumer")
    AUTO     = "auto",     _("Auto")
    MORTGAGE = "mortgage", _("Mortgage")
    BUSINESS = "business", _("Business")


class Credit(BaseModel):
    bank              = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="credits")
    name              = models.CharField(max_length=120)
    purpose           = models.CharField(max_length=20, choices=CreditPurpose.choices, default=CreditPurpose.CONSUMER)
    credit_type       = models.CharField(max_length=100, blank=True)  # matndagi "kredit turi"
    down_payment      = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,
                                            validators=[MinValueValidator(0)])
    interest_rate     = models.DecimalField(max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    period_months     = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amount            = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])

    collateral_required = models.BooleanField(default=False)
    grace_period_months = models.PositiveIntegerField(null=True, blank=True)
    early_repayment_fee_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    official_income_required = models.BooleanField(default=False)
    online_apply_link        = models.URLField(blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="credit_clicks")
    documents_note           = models.CharField(max_length=255, blank=True)
    image                    = models.ImageField(upload_to="credit_images/", blank=True, null=True)

    class Meta:
        db_table = "credit"
        verbose_name = _("Credit")
        verbose_name_plural = _("Credits")
        ordering = ["bank__name", "purpose", "name"]
        indexes = [models.Index(fields=["bank", "purpose", "period_months"])]

    def __str__(self):
        return f"{self.name} — {self.bank.name}"


# -------------------- Deposits --------------------

class PayoutFrequency(models.TextChoices):
    MONTHLY     = "monthly", _("Monthly")
    QUARTERLY   = "quarterly", _("Quarterly")
    AT_MATURITY = "maturity", _("At maturity")


class Deposit(BaseModel):
    bank          = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="deposits")
    name          = models.CharField(max_length=120)
    deposit_type  = models.CharField(max_length=100)  # masalan: Jamg‘arma, Bolalar, Onlayn va h.k.
    min_amount    = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    max_amount    = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,
                                        validators=[MinValueValidator(0)])
    period_months = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])
    currency_code = models.CharField(max_length=3, choices=CurrencyCode.choices, default=CurrencyCode.UZS)

    payout_frequency         = models.CharField(max_length=10, choices=PayoutFrequency.choices,
                                                default=PayoutFrequency.MONTHLY)
    capitalization           = models.BooleanField(default=True)
    early_withdrawal_allowed = models.BooleanField(default=True)
    auto_renewal             = models.BooleanField(default=False)

    online_open_link = models.URLField(blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="deposit_clicks")
    image           = models.ImageField(upload_to="deposit_images/", blank=True, null=True)

    class Meta:
        db_table = "deposit"
        verbose_name = _("Deposit")
        verbose_name_plural = _("Deposits")
        ordering = ["bank__name", "interest_rate", "period_months"]
        indexes = [
            models.Index(fields=["bank", "currency_code"]),
            models.Index(fields=["interest_rate"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="deposit_min_le_max_nullable",
                check=(
                    models.Q(max_amount__isnull=True) |
                    models.Q(min_amount__lte=models.F("max_amount"))
                ),
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.bank.name}"


# -------------------- Currency rates per bank --------------------

class Currency(BaseModel):
    bank          = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="currencies")
    code          = models.CharField(max_length=3, choices=CurrencyCode.choices)
    name          = models.CharField(max_length=50)
    buy_rate      = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])  # 1 birlik = so‘m
    sell_rate     = models.DecimalField(max_digits=12, decimal_places=4, validators=[MinValueValidator(0)])
    change_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    link          = models.URLField(blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="currency_clicks")
    updated_at_api = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "currency"
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ["bank__name", "code"]
        unique_together = [("bank", "code")]
        indexes = [
            models.Index(fields=["bank", "code"]),
            models.Index(fields=["updated_at_api"]),
        ]

    def __str__(self):
        return f"{self.code} @ {self.bank.name}"


# -------------------- P2P (Apps) --------------------

class CommissionType(models.TextChoices):
    PERCENT = "percent", _("Percent")
    FIXED   = "fixed",   _("Fixed")
    MIXED   = "mixed",   _("Mixed")


class App(BaseModel):
    name     = models.CharField(max_length=120)
    slug     = models.SlugField(unique=True)
    logo     = models.ImageField(upload_to="apps_logos/", blank=True, null=True)
    site_url = models.URLField(blank=True, null=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="app_clicks")

    class Meta:
        db_table = "app"
        verbose_name = _("App")
        verbose_name_plural = _("Apps")
        ordering = ["name"]

    def __str__(self):
        return self.name


class P2POffer(BaseModel):
    app        = models.ForeignKey(App, on_delete=models.CASCADE, related_name="offers")
    from_scheme = models.CharField(max_length=10, choices=CardSystem.choices)
    to_scheme   = models.CharField(max_length=10, choices=CardSystem.choices)

    commission_type  = models.CharField(max_length=10, choices=CommissionType.choices)
    commission_value = models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(0)])
    commission_note  = models.CharField(max_length=255, blank=True)

    per_txn_min = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,
                                      validators=[MinValueValidator(0)])
    per_txn_max = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,
                                      validators=[MinValueValidator(0)])
    monthly_cap = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,
                                      validators=[MinValueValidator(0)])
    daily_cap   = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,
                                      validators=[MinValueValidator(0)])

    description = models.TextField(blank=True)

    # Amal qilish davri
    starts_at = models.DateField(null=True, blank=True)
    ends_at   = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "p2p_offer"
        verbose_name = _("P2P Offer")
        verbose_name_plural = _("P2P Offers")
        ordering = ["app__name", "sort_order", "id"]
        indexes = [models.Index(fields=["app", "from_scheme", "to_scheme"])]
        constraints = [
            models.CheckConstraint(
                name="p2p_offer_min_le_max_nullable",
                check=(
                    models.Q(per_txn_min__isnull=True) |
                    models.Q(per_txn_max__isnull=True) |
                    models.Q(per_txn_min__lte=models.F("per_txn_max"))
                ),
            ),
            models.CheckConstraint(
                name="p2p_offer_validity_order",
                check=(
                    models.Q(starts_at__isnull=True) |
                    models.Q(ends_at__isnull=True) |
                    models.Q(starts_at__lte=models.F("ends_at"))
                ),
            ),
        ]
        unique_together = [
            ("app", "from_scheme", "to_scheme", "commission_type", "sort_order"),
        ]

    def __str__(self):
        return f"{self.app.name}: {self.from_scheme} → {self.to_scheme}"
