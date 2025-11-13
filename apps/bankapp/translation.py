# apps/bankapp/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import (
    Bank, Card, Credit, Deposit, Currency,
    App, P2POffer
)

@register(Bank)
class BankTR(TranslationOptions):
    # Eslatma: bank nomi (name) unique=True — odatda tarjima qilinmaydi.
    # Kerak bo‘lsa, 'name'ni ham qo‘shing, lekin uniqueness bilan ehtiyot bo‘ling.
    fields = ('address', 'description',)

@register(Card)
class CardTR(TranslationOptions):
    fields = ('name',)

@register(Credit)
class CreditTR(TranslationOptions):
    fields = ('name', 'credit_type', 'documents_note',)

@register(Deposit)
class DepositTR(TranslationOptions):
    fields = ('name', 'deposit_type',)

@register(Currency)
class CurrencyTR(TranslationOptions):
    # Masalan: "US Dollar" / "Доллар США" / "AQSh dollari"
    fields = ('name',)

@register(App)
class AppTR(TranslationOptions):
    # App nomi ko‘p hollarda ko‘rsatiladigan matn — tarjima qilamiz.
    # Slug tarjima qilinmaydi (unique URL identifikatori).
    fields = ('name',)

@register(P2POffer)
class P2POfferTR(TranslationOptions):
    fields = ('description', 'commission_note',)
