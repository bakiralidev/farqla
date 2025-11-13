# apps/<your_app>/admin.py
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin  # <-- muhim
from .models import (
    Universitet, Fakultet, UniverYonalish,
    XususiyMaktab, Fan, MaktabYonalish
)

# ------- Inlines -------
class FakultetInline(admin.TabularInline):
    model = Fakultet
    extra = 0
    fields = ("name", "dekan", "telefon", "email", "tashkil_yili")
    show_change_link = True

class UniverYonalishInline(admin.TabularInline):
    model = UniverYonalish
    extra = 0
    fields = ("name", "talim_turi", "talim_muddati_y", "grant_mavjudmi")
    show_change_link = True

class MaktabYonalishInline(admin.TabularInline):
    model = MaktabYonalish
    extra = 0
    fields = ("name", "talim_muddati_o", "grant_mavjudmi")
    show_change_link = True


# ------- Universitet -------
@admin.register(Universitet)
class UniversitetAdmin(TabbedTranslationAdmin):
    list_display = ("name", "tashkil_yili", "address", "web_sayt", "image_preview", "created_at")
    list_filter = ("tashkil_yili",)
    search_fields = ("name", "desc", "address")
    ordering = ("name",)
    inlines = [FakultetInline]
    list_select_related = ()  # kerak bo'lsa qo'shasiz

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "tashkil_yili",
                "desc",
                "address",
                "web_sayt",
                "image",
            )
        }),
    )

    def image_preview(self, obj):
        if getattr(obj, "image", None):
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Rasm"


# ------- Fakultet -------
@admin.register(Fakultet)
class FakultetAdmin(TabbedTranslationAdmin):
    list_display = ("name", "universitet", "dekan", "telefon", "email", "tashkil_yili", "created_at")
    list_filter = ("tashkil_yili", "universitet")
    search_fields = ("name", "dekan", "telefon", "email", "desc", "universitet__name")
    ordering = ("universitet__name", "name")
    autocomplete_fields = ("universitet",)
    inlines = [UniverYonalishInline]
    list_select_related = ("universitet",)

    fieldsets = (
        (None, {
            "fields": (
                "universitet",
                "name",
                "dekan",
                "telefon",
                "email",
                "tashkil_yili",
                "desc",
            )
        }),
    )


# ------- UniverYonalish -------
@admin.register(UniverYonalish)
class UniverYonalishAdmin(TabbedTranslationAdmin):
    list_display = ("name", "fakultet", "get_universitet", "talim_turi", "talim_muddati_y", "grant_mavjudmi")
    list_filter = ("talim_turi", "grant_mavjudmi", "fakultet__universitet")
    search_fields = ("name", "desc", "fakultet__name", "fakultet__universitet__name")
    ordering = ("fakultet__universitet__name", "fakultet__name", "name")
    autocomplete_fields = ("fakultet",)
    list_select_related = ("fakultet", "fakultet__universitet")

    fieldsets = (
        (None, {
            "fields": (
                "fakultet",
                "name",
                "desc",
                "talim_turi",
                "talim_muddati_y",
                "grant_mavjudmi",
            )
        }),
    )

    def get_universitet(self, obj):
        return obj.fakultet.universitet
    get_universitet.short_description = "Universitet"
    get_universitet.admin_order_field = "fakultet__universitet__name"


# ------- XususiyMaktab -------
@admin.register(XususiyMaktab)
class XususiyMaktabAdmin(TabbedTranslationAdmin):
    list_display = ("name", "mudir", "tashkil_yili", "address", "web_sayt", "created_at")
    list_filter = ("tashkil_yili",)
    search_fields = ("name", "mudir", "desc", "address")
    ordering = ("name",)
    inlines = [MaktabYonalishInline]

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "mudir",
                "tashkil_yili",
                "desc",
                "address",
                "web_sayt",
            )
        }),
    )


# ------- Fan -------
@admin.register(Fan)
class FanAdmin(TabbedTranslationAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name",)}),
    )


# ------- MaktabYonalish -------
@admin.register(MaktabYonalish)
class MaktabYonalishAdmin(TabbedTranslationAdmin):
    list_display = ("name", "maktab", "talim_muddati_o", "oqish_summasi", "grant_mavjudmi", "created_at")
    list_filter = ("grant_mavjudmi", "maktab")
    search_fields = ("name", "desc", "maktab__name", "fanlar__name")
    ordering = ("maktab__name", "name")
    autocomplete_fields = ("maktab",)
    filter_horizontal = ("fanlar",)
    list_select_related = ("maktab",)

    fieldsets = (
        (None, {
            "fields": (
                "maktab",
                "name",
                "desc",
                "talim_muddati_o",
                "oqish_summasi",
                "grant_mavjudmi",
                "fanlar",
            )
        }),
    )
