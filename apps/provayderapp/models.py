# apps/catalog/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class InternetProvayder(models.Model):
    name        = models.CharField(_("nomi"), max_length=150)
    tarif       = models.CharField(_("tarif nomi"), max_length=150)
    tarif_narxi = models.DecimalField(_("tarif narxi"), max_digits=12, decimal_places=2)
    tavsifi     = models.TextField(_("tavsif"), blank=True)
    icon        = models.ImageField(_("ikon"), upload_to="provayderlar/icons/", blank=True, null=True)

    class Meta:
        db_table = "internet_provayderlar"
        verbose_name = _("Internet provayder")
        verbose_name_plural = _("Internet provayderlar")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.tarif}"


class Qurilma(models.Model):
    internet_provayder = models.ForeignKey(
        InternetProvayder,
        on_delete=models.CASCADE,
        related_name="qurilmalar",
        verbose_name=_("internet provayder")
    )
    name    = models.CharField(_("nomi"), max_length=150)
    model   = models.CharField(_("model"), max_length=150, blank=True)
    narxi   = models.DecimalField(_("narxi"), max_digits=12, decimal_places=2)
    tavsifi = models.TextField(_("tavsif"), blank=True)
    icon    = models.ImageField(_("ikon"), upload_to="qurilmalar/icons/", blank=True, null=True)

    class Meta:
        db_table = "qurilmalar"
        verbose_name = _("Qurilma")
        verbose_name_plural = _("Qurilmalar")
        ordering = ["internet_provayder__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.model})"
