from modeltranslation.translator import register, TranslationOptions
from .models import SugurtaCompany, Sugurta


@register(SugurtaCompany)
class SugurtaCompanyTranslationOptions(TranslationOptions):
    # Ko'p tilda kiritiladigan maydonlar
    fields = ("name", "address", "company_about",)


@register(Sugurta)
class SugurtaTranslationOptions(TranslationOptions):
    # Mahsulot nomini tarjima qilamiz
    fields = ("name",)
