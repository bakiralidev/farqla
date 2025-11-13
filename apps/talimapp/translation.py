# apps/<your_app>/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Universitet, Fakultet, UniverYonalish, XususiyMaktab, Fan, MaktabYonalish

@register(Universitet)
class UniversitetTr(TranslationOptions):
    fields = ("name", "desc", "address",)

@register(Fakultet)
class FakultetTr(TranslationOptions):
    fields = ("name", "desc",)

@register(UniverYonalish)
class UniverYonalishTr(TranslationOptions):
    fields = ("name", "desc",)

@register(XususiyMaktab)
class XususiyMaktabTr(TranslationOptions):
    fields = ("name", "desc", "address",)

@register(Fan)
class FanTr(TranslationOptions):
    fields = ("name",)

@register(MaktabYonalish)
class MaktabYonalishTr(TranslationOptions):
    fields = ("name", "desc",)
