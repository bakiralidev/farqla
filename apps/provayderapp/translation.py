from modeltranslation.translator import register, TranslationOptions
from .models import InternetProvayder, Qurilma


@register(InternetProvayder)
class InternetProvayderTranslationOptions(TranslationOptions):
    fields = ('name', 'tarif', 'tavsifi',)


@register(Qurilma)
class QurilmaTranslationOptions(TranslationOptions):
    fields = ('name', 'model', 'tavsifi',)
