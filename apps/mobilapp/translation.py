from modeltranslation.translator import register, TranslationOptions
from .models import Simkarta


@register(Simkarta)
class SimkartaTranslationOptions(TranslationOptions):
    fields = ('name', 'tarif', 'tavsif',)
