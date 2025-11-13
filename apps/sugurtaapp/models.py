# apps/insurance/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


# --------- Choice-lar ---------
class SugurtaTuri(models.TextChoices):
    OSAGO   = "osago",   _("Majburiy avtoulov (OSAGO)")
    KASKO   = "kasko",   _("KASKO")
    TRAVEL  = "travel",  _("Sayohat sug‘urtasi")
    HEALTH  = "health",  _("Sog‘liq sug‘urtasi")
    PROPERTY= "property",_("Mulk sug‘urtasi")
    LIFE    = "life",    _("Hayot sug‘urtasi")
    OTHER   = "other",   _("Boshqa")

class ShaxsRoli(models.TextChoices):
    JISMONIY = "individual", _("Jismoniy shaxs")
    YURIDIK  = "company",    _("Yuridik shaxs")


# --------- Kompaniya ---------
class SugurtaCompany(models.Model):
    name          = models.CharField(_("kompaniya nomi"), max_length=150)
    address       = models.CharField(_("manzil"), max_length=255, blank=True)
    company_about = models.TextField(_("kompaniya haqida"), blank=True)
    longitude     = models.DecimalField(_("longitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    latitude      = models.DecimalField(_("latitude"),  max_digits=9, decimal_places=6, blank=True, null=True)
    image         = models.ImageField(_("rasm / logo"), upload_to="insurance/companies/", blank=True, null=True)

    class Meta:
        db_table = "sugurta_company"
        verbose_name = _("Sug‘urta kompaniyasi")
        verbose_name_plural = _("Sug‘urta kompaniyalari")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# --------- Sug‘urta mahsuloti ---------
class Sugurta(models.Model):
    sugurta_company = models.ForeignKey(
        SugurtaCompany,
        on_delete=models.CASCADE,
        related_name="sugurtalar",
        verbose_name=_("sug‘urta kompaniyasi"),
    )
    name        = models.CharField(_("mahsulot nomi"), max_length=180)
    sugurta_turi= models.CharField(_("sug‘urta turi"), max_length=20, choices=SugurtaTuri.choices)
    shaxs_roli  = models.CharField(_("shaxs roli"), max_length=20, choices=ShaxsRoli.choices)
    link        = models.URLField(_("havola"), blank=True)
    image       = models.ImageField(_("rasm"), upload_to="insurance/products/", blank=True, null=True)

    class Meta:
        db_table = "sugurta"
        verbose_name = _("Sug‘urta")
        verbose_name_plural = _("Sug‘urtalar")
        ordering = ["sugurta_company__name", "name"]
        unique_together = [("sugurta_company", "name")]

    def __str__(self) -> str:
        return f"{self.name} — {self.sugurta_company.name}"
