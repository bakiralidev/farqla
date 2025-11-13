# apps/catalog/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from apps.bankapp.models_clicks import URLClickStat, record_url_click

class SimkartaTuri(models.TextChoices):
    PREPAID  = "prepaid",  _("Oldindan to‘lov (Prepaid)")
    POSTPAID = "postpaid", _("Keyin to‘lov (Postpaid)")
    ESIM     = "esim",     _("Elektron SIM (eSIM)")


class Simkarta(models.Model):
    name          = models.CharField(_("nomi"), max_length=100)
    tarif         = models.CharField(_("tarif nomi"), max_length=100)
    tarif_narxi   = models.DecimalField(_("tarif narxi (so‘m)"), max_digits=10, decimal_places=2)
    tavsif        = models.TextField(_("tavsif"), blank=True)
    icon          = models.ImageField(_("ikonka"), upload_to="simkartalar/icons/", blank=True, null=True)
    simkarta_turi = models.CharField(_("simkarta turi"), max_length=20, choices=SimkartaTuri.choices)
    link          = models.URLField(_("maʼlumotlar sahifasi"), blank=True)
    url_clicks = GenericRelation(URLClickStat, related_query_name="app_clicks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "simkartalar"
        verbose_name = _("Simkarta")
        verbose_name_plural = _("Simkartalar")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.tarif}"
