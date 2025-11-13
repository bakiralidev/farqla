from rest_framework import serializers
from .models import Simkarta, SimkartaTuri


class SimkartaSerializer(serializers.ModelSerializer):
    # Choice label (o‘qishda qulaylik uchun)
    simkarta_turi_display = serializers.CharField(
        source="get_simkarta_turi_display", read_only=True
    )
    # Rasmga absolut URL (Frontend uchun qulay)
    icon_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Simkarta
        fields = [
            "id",
            "name",
            "tarif",
            "tarif_narxi",
            "tavsif",
            "icon",
            "icon_url",
            "simkarta_turi",
            "simkarta_turi_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "simkarta_turi_display", "icon_url"]

    def get_icon_url(self, obj):
        request = self.context.get("request")
        if obj.icon and hasattr(obj.icon, "url"):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None

    def validate_tarif_narxi(self, value):
        if value is None:
            return value
        if value < 0:
            raise serializers.ValidationError("Tarif narxi manfiy bo‘lishi mumkin emas.")
        return value
