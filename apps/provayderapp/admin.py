from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import InternetProvayder, Qurilma


@admin.register(InternetProvayder)
class InternetProvayderAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "tarif", "tarif_narxi")
    search_fields = ("name", "tarif", "tavsifi")
    ordering = ("name",)
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "tarif",
                "tarif_narxi",
                "tavsifi",
                "icon",
            )
        }),
    )


@admin.register(Qurilma)
class QurilmaAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "model", "narxi", "internet_provayder")
    list_filter = ("internet_provayder",)
    search_fields = ("name", "model", "tavsifi", "internet_provayder__name")
    ordering = ("internet_provayder__name", "name")
    fieldsets = (
        (None, {
            "fields": (
                "internet_provayder",
                "name",
                "model",
                "narxi",
                "tavsifi",
                "icon",
            )
        }),
    )
