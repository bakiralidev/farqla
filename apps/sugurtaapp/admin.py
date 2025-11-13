from django.contrib import admin
from django.utils.html import format_html
from .models import SugurtaCompany, Sugurta

@admin.register(SugurtaCompany)
class SugurtaCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "logo_preview")
    search_fields = ("name", "address", "company_about")
    ordering = ("name",)

    def logo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"
    logo_preview.short_description = "Logo"

@admin.register(Sugurta)
class SugurtaAdmin(admin.ModelAdmin):
    list_display = (
        "name", "sugurta_company", "sugurta_turi", "shaxs_roli", "link_short", "image_preview"
    )
    list_filter = ("sugurta_turi", "shaxs_roli", "sugurta_company")
    search_fields = ("name", "link", "sugurta_company__name")
    ordering = ("sugurta_company__name", "name")
    autocomplete_fields = ("sugurta_company",)

    def link_short(self, obj):
        return (obj.link[:45] + "…") if obj.link and len(obj.link) > 45 else (obj.link or "—")
    link_short.short_description = "Havola"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Rasm"
