from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import SugurtaCompany, Sugurta

class SugurtaCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SugurtaCompany
        fields = [
            "id", "name", "address", "company_about",
            "longitude", "latitude", "image",
        ]


class SugurtaSerializer(serializers.ModelSerializer):
    # Qo'shimcha o‘qish uchun qulay maydonlar
    company_name = serializers.CharField(source="sugurta_company.name", read_only=True)
    sugurta_turi_label = serializers.CharField(source="get_sugurta_turi_display", read_only=True)
    shaxs_roli_label   = serializers.CharField(source="get_shaxs_roli_display", read_only=True)

    class Meta:
        model = Sugurta
        fields = [
            "id", "sugurta_company", "company_name",
            "name", "sugurta_turi", "sugurta_turi_label",
            "shaxs_roli", "shaxs_roli_label", "link", "image",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Sugurta.objects.all(),
                fields=("sugurta_company", "name"),
                message="Ushbu kompaniyada shu nomdagi sug‘urta allaqachon mavjud."
            )
        ]
