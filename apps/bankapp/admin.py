# apps/bankapp/admin.py
from django.contrib import admin
from django.utils import timezone
from django.db import models
from .models_clicks import URLClickStat

from .models import (
    Bank, Card, Credit, Deposit, Currency,
    App, P2POffer
)

# modeltranslation admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline


# --------- Universal actions ---------
@admin.action(description="🔓 Activate selected items")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="🔒 Deactivate selected items")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(URLClickStat)
class URLClickStatAdmin(admin.ModelAdmin):
    list_display = (
        "content_type", "object_id", "field_name", "clicks",
        "last_clicked_at", "last_clicked_by", "last_clicked_ip"
    )
    list_filter = ("content_type", "field_name")
    search_fields = ("content_type__model", "object_id", "field_name")
    readonly_fields = ("clicks", "last_clicked_at", "last_clicked_by", "last_clicked_ip", "last_user_agent")

    ordering = ("-last_clicked_at",)

# --------- Base admin ---------
class BaseAdmin(TranslationAdmin):
    list_filter = ("is_active",)
    actions = [make_active, make_inactive]
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 50
    # sluglarni aynan o‘zbekcha nomdan yasashni xohlasangiz:
    prepopulated_fields_language = 'uz'


# --------- Inline blocks ---------
class CardInline(TranslationTabularInline):
    model = Card
    extra = 0
    fields = ("name", "system", "currency_code", "interest_rate", "fast_issuance", "is_active")
    show_change_link = True

class CreditInline(TranslationTabularInline):
    model = Credit
    extra = 0
    fields = ("name", "purpose", "interest_rate", "period_months", "amount", "is_active")
    show_change_link = True

class DepositInline(TranslationTabularInline):
    model = Deposit
    extra = 0
    fields = ("name", "interest_rate", "period_months", "min_amount", "is_active")
    show_change_link = True

# Currency.name tarjima bo‘lsa ham inline’da ko‘rsatmayapmiz, shuning uchun odatiy TabularInline ham bo‘ladi.
class CurrencyInline(admin.TabularInline):
    model = Currency
    extra = 0
    fields = ("code", "buy_rate", "sell_rate", "change_percent", "updated_at_api")
    readonly_fields = ("updated_at_api",)
    show_change_link = True


# --------- Bank admin ---------
@admin.register(Bank)
class BankAdmin(BaseAdmin):
    list_display = ("id","name", "rating", "number_of_branches", "number_of_satisfied_customers", "is_active")
    search_fields = ("name", "address", "description")
    list_filter = ("is_active", "opening_date")
    inlines = [CardInline, CreditInline, DepositInline, CurrencyInline]
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ()
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "description", "image", "website", "phone")
        }),
        ("Statistics", {
            "fields": ("number_of_branches", "number_of_satisfied_customers", "rating")
        }),
        ("Location & Dates", {
            "fields": ("address", "longitude", "latitude", "opening_date")
        }),
        ("System Fields", {
            "fields": ("is_active", "sort_order", "created_at", "updated_at")
        }),
    )


# --------- Card admin ---------
@admin.register(Card)
class CardAdmin(BaseAdmin):
    list_display = ("name", "bank", "system", "currency_code", "interest_rate", "fast_issuance", "is_active")
    list_filter = ("bank", "system", "currency_code", "card_type", "is_active")
    search_fields = ("name", "bank__name", "system")
    autocomplete_fields = ("bank",)
    list_editable = ("is_active",)
    date_hierarchy = "created_at"
    list_select_related = ("bank",)


# --------- Credit admin ---------
@admin.register(Credit)
class CreditAdmin(BaseAdmin):
    list_display = ("name", "bank", "purpose", "interest_rate", "period_months", "amount", "is_active")
    list_filter = ("bank", "purpose", "is_active")
    search_fields = ("name", "bank__name", "purpose")
    autocomplete_fields = ("bank",)
    date_hierarchy = "created_at"
    list_select_related = ("bank",)


# --------- Deposit admin ---------
@admin.register(Deposit)
class DepositAdmin(BaseAdmin):
    list_display = ("name", "bank", "interest_rate", "period_months", "currency_code", "is_active")
    list_filter = ("bank", "currency_code", "payout_frequency", "is_active")
    search_fields = ("name", "bank__name")
    autocomplete_fields = ("bank",)
    date_hierarchy = "created_at"
    list_select_related = ("bank",)


# --------- Currency admin ---------
@admin.register(Currency)
class CurrencyAdmin(BaseAdmin):
    list_display = ("bank", "code", "buy_rate", "sell_rate", "change_percent", "updated_at_api")
    list_filter = ("bank", "code")
    search_fields = ("bank__name", "code")
    autocomplete_fields = ("bank",)
    readonly_fields = ("updated_at_api",)
    date_hierarchy = "created_at"
    list_select_related = ("bank",)


# --------- App admin ---------
@admin.register(App)
class AppAdmin(BaseAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = []


# --------- Custom filter: P2P offer validity ---------
class OfferValidityFilter(admin.SimpleListFilter):
    title = "validity (by date)"
    parameter_name = "validity"

    def lookups(self, request, model_admin):
        return (
            ("active_today", "Active today"),
            ("expired", "Expired"),
            ("upcoming", "Upcoming"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        today = timezone.localdate()
        if self.value() == "active_today":
            # starts_at <= today <= ends_at (yoki null’lar ruxsat)
            return queryset.filter(
                models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=today),
                models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=today),
            )
        if self.value() == "expired":
            return queryset.filter(ends_at__lt=today)
        if self.value() == "upcoming":
            return queryset.filter(starts_at__gt=today)
        return queryset


# --------- P2P Offers admin ---------
@admin.register(P2POffer)
class P2POfferAdmin(BaseAdmin):
    list_display = (
        "app", "from_scheme", "to_scheme", "commission_type",
        "commission_value", "per_txn_min", "per_txn_max",
        "starts_at", "ends_at", "is_active"
    )
    list_filter = (
        "app", "from_scheme", "to_scheme", "commission_type", "is_active", OfferValidityFilter
    )
    search_fields = ("app__name", "from_scheme", "to_scheme")
    autocomplete_fields = ("app",)
    list_editable = ("is_active",)
    date_hierarchy = "created_at"
    list_select_related = ("app",)
    fieldsets = (
        ("Main Info", {
            "fields": (
                "app", "from_scheme", "to_scheme",
                "commission_type", "commission_value", "commission_note"
            )
        }),
        ("Limits", {
            "fields": ("per_txn_min", "per_txn_max", "monthly_cap", "daily_cap")
        }),
        ("Period & Status", {
            "fields": ("starts_at", "ends_at", "is_active", "sort_order")
        }),
        ("Description", {
            "fields": ("description",)
        }),
        ("System", {
            "fields": ("created_at", "updated_at")
        }),
    )
