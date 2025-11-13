# apps/bankapp/models_clicks.py
from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = get_user_model()

class URLClickStat(models.Model):
    """
    Har qanday modeldagi har qanday URLField uchun kliklar hisoblagichi.
    Unikal kalit: (content_type, object_id, field_name)
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    object_id = models.PositiveBigIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    field_name = models.CharField(max_length=100, db_index=True)

    clicks = models.PositiveBigIntegerField(default=0)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    last_clicked_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    last_clicked_ip = models.GenericIPAddressField(null=True, blank=True)
    last_user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "url_click_stat"
        indexes = [
            models.Index(fields=["content_type", "object_id", "field_name"]),
            models.Index(fields=["updated_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "field_name"],
                name="unique_click_stat_per_field",
            ),
        ]

    def __str__(self):
        return f"{self.content_type.app_label}.{self.content_type.model}#{self.object_id}.{self.field_name} — {self.clicks}"

    @classmethod
    def get_or_create_for(cls, obj, field_name: str) -> "URLClickStat":
        ct = ContentType.objects.get_for_model(obj.__class__)
        stat, _ = cls.objects.get_or_create(
            content_type=ct, object_id=obj.pk, field_name=field_name
        )
        return stat

    def increment(
        self,
        by: int = 1,
        *,
        user: User | None = None,
        ip: str | None = None,
        user_agent: str | None = None,
        when=None,
    ) -> None:
        self.__class__.objects.filter(pk=self.pk).update(
            clicks=F("clicks") + by,
            last_clicked_at=when or timezone.now(),
            last_clicked_by=user if user else F("last_clicked_by"),
            last_clicked_ip=ip if ip else F("last_clicked_ip"),
            last_user_agent=user_agent if user_agent else F("last_user_agent"),
        )
        self.refresh_from_db(
            fields=[
                "clicks",
                "last_clicked_at",
                "last_clicked_by",
                "last_clicked_ip",
                "last_user_agent",
            ]
        )


def record_url_click(obj, field_name: str, request=None, user=None) -> URLClickStat:
    """
    Redirectdan oldin chaqiriladi. Stat yozadi va URLClickStat ni qaytaradi.
    """
    stat = URLClickStat.get_or_create_for(obj, field_name)
    ip = None
    ua = None
    if request is not None:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = (xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR"))
        ua = request.META.get("HTTP_USER_AGENT")
    stat.increment(user=user if getattr(user, "is_authenticated", False) else None, ip=ip, user_agent=ua)
    return stat


__all__ = ["URLClickStat", "record_url_click"]
