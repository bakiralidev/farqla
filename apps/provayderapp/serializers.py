from rest_framework import serializers
from .models import InternetProvayder, Qurilma


class InternetProvayderSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InternetProvayder
        fields = [
            "id", "name", "tarif", "tarif_narxi", "tavsifi",
            "icon", "icon_url",
        ]

    def get_icon_url(self, obj):
        request = self.context.get("request")
        if obj.icon and hasattr(obj.icon, "url"):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None


class QurilmaSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField(read_only=True)
    internet_provayder_name = serializers.CharField(
        source="internet_provayder.name", read_only=True
    )

    class Meta:
        model = Qurilma
        fields = [
            "id",
            "internet_provayder",        # writable FK (ID)
            "internet_provayder_name",   # read-only label
            "name", "model", "narxi", "tavsifi",
            "icon", "icon_url",
        ]

    def get_icon_url(self, obj):
        request = self.context.get("request")
        if obj.icon and hasattr(obj.icon, "url"):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None

    def validate_narxi(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Narx manfiy bo‘lishi mumkin emas.")
        return value
