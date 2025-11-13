# apps/education/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import date


# ---- Yordamchi validatorlar ----
def current_year() -> int:
    return date.today().year

def max_value_current_year(value: int):
    return MaxValueValidator(current_year())(value)


# ---- Umumiy mixinlar ----
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LocationMixin(models.Model):
    address = models.CharField(_("manzil"), max_length=255, blank=True)
    longitude = models.DecimalField(_("longitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    latitude  = models.DecimalField(_("latitude"),  max_digits=9, decimal_places=6, blank=True, null=True)
    web_sayt  = models.URLField(_("web-sayt"), blank=True)

    class Meta:
        abstract = True


# ---- Choice-lar ----
class StudyType(models.TextChoices):
    KUNDUZGI   = "kunduzgi", _("Kunduzgi")
    SIRTQI     = "sirtqi",   _("Sirtqi")
    KECHKI     = "kechki",   _("Kechki")
    MASOFAVIY  = "online",   _("Masofaviy (onlayn)")


# ---- Asosiy modellar ----
class Universitet(TimeStampedModel, LocationMixin):
    name         = models.CharField(_("nomi"), max_length=200)
    tashkil_yili = models.PositiveSmallIntegerField(
        _("tashkil topgan yili"),
        validators=[MinValueValidator(1800), max_value_current_year],
        blank=True, null=True
    )
    desc  = models.TextField(_("tavsif"), blank=True)
    image = models.ImageField(upload_to="universitetlar/", blank=True, null=True)

    class Meta:
        db_table = "universitetlar"
        verbose_name = _("Universitet")
        verbose_name_plural = _("Universitetlar")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Fakultet(TimeStampedModel):
    universitet  = models.ForeignKey(Universitet, on_delete=models.CASCADE, related_name="fakultetlar")
    name         = models.CharField(_("nomi"), max_length=200)
    dekan        = models.CharField(_("dekan"), max_length=200, blank=True)
    telefon      = models.CharField(_("telefon"), max_length=32, blank=True)
    email        = models.EmailField(_("email"), blank=True)
    tashkil_yili = models.PositiveSmallIntegerField(
        _("tashkil yili"),
        validators=[MinValueValidator(1800), max_value_current_year],
        blank=True, null=True
    )
    desc = models.TextField(_("tavsif"), blank=True)

    class Meta:
        db_table = "fakultetlar"
        verbose_name = _("Fakultet")
        verbose_name_plural = _("Fakultetlar")
        unique_together = [("universitet", "name")]
        ordering = ["universitet__name", "name"]

    def __str__(self):
        return f"{self.name} — {self.universitet.name}"


class UniverYonalish(TimeStampedModel):
    fakultet         = models.ForeignKey(Fakultet, on_delete=models.CASCADE, related_name="yonalishlar")
    name             = models.CharField(_("yo‘nalish nomi"), max_length=200)
    talim_turi       = models.CharField(_("ta'lim turi"), max_length=20, choices=StudyType.choices, default=StudyType.KUNDUZGI)
    talim_muddati_y  = models.PositiveSmallIntegerField(_("ta'lim muddati (yil)"), validators=[MinValueValidator(1)], help_text=_("yillarda"))
    kontrakt_summasi = models.DecimalField(_("kontrakt summasi"), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    grant_mavjudmi   = models.BooleanField(_("grant mavjudmi"), default=False)
    desc             = models.TextField(_("tavsif"), blank=True)

    class Meta:
        db_table = "univer_yonalishlar"
        verbose_name = _("Universitet yo‘nalishi")
        verbose_name_plural = _("Universitet yo‘nalishlari")
        unique_together = [("fakultet", "name", "talim_turi")]
        ordering = ["fakultet__universitet__name", "fakultet__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.fakultet.universitet.name})"


class XususiyMaktab(TimeStampedModel, LocationMixin):
    name         = models.CharField(_("nomi"), max_length=200)
    tashkil_yili = models.PositiveSmallIntegerField(
        _("tashkil topgan yili"),
        validators=[MinValueValidator(1900), max_value_current_year],
        blank=True, null=True
    )
    mudir = models.CharField(_("rahbar (mudir)"), max_length=200, blank=True)
    desc  = models.TextField(_("tavsif"), blank=True)

    class Meta:
        db_table = "xususiy_maktablar"
        verbose_name = _("Xususiy maktab")
        verbose_name_plural = _("Xususiy maktablar")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Fan(TimeStampedModel):
    name = models.CharField(_("fan nomi"), max_length=120, unique=True)

    class Meta:
        db_table = "fanlar"
        verbose_name = _("Fan")
        verbose_name_plural = _("Fanlar")
        ordering = ["name"]

    def __str__(self):
        return self.name


class MaktabYonalish(TimeStampedModel):
    maktab          = models.ForeignKey(XususiyMaktab, on_delete=models.CASCADE, related_name="yonalishlar")
    name            = models.CharField(_("yo‘nalish nomi"), max_length=200)
    fanlar          = models.ManyToManyField(Fan, blank=True, related_name="maktab_yonalishlari")
    talim_muddati_o = models.PositiveSmallIntegerField(_("ta'lim muddati (oy)"), validators=[MinValueValidator(1)], help_text=_("oylarda"))
    oqish_summasi   = models.DecimalField(_("o‘qish summasi"), max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    grant_mavjudmi  = models.BooleanField(_("grant mavjudmi"), default=False)
    desc            = models.TextField(_("tavsif"), blank=True)

    class Meta:
        db_table = "maktab_yonalishlar"
        verbose_name = _("Maktab yo‘nalishi")
        verbose_name_plural = _("Maktab yo‘nalishlari")
        unique_together = [("maktab", "name")]
        ordering = ["maktab__name", "name"]

    def __str__(self):
        return f"{self.name} — {self.maktab.name}"
