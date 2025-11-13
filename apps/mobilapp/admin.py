from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin   # 🔹 Tillar uchun tablar
from django.utils.html import format_html
from .models import Simkarta


@admin.register(Simkarta)
class SimkartaAdmin(TabbedTranslationAdmin):
    list_display = (
        "id",
        "name",
        "tarif",
        "tarif_narxi",
        "simkarta_turi",
        "created_at",
        "updated_at",
        "icon_preview",
    )
    list_filter = ("simkarta_turi", "created_at")
    search_fields = ("name", "tarif", "tavsif")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "tarif",
                "tarif_narxi",
                "tavsif",
                "icon",
                "simkarta_turi",
            )
        }),
        ("Tizim maʼlumotlari", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:6px;" />', obj.icon.url
            )
        return "—"

    icon_preview.short_description = "Ikonka"
