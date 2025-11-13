from rest_framework import serializers
from .models import (
    Universitet, Fakultet, UniverYonalish,
    XususiyMaktab, Fan, MaktabYonalish
)

# ------- Universitet -------
class UniversitetSerializer(serializers.ModelSerializer):
    fakultetlar_soni = serializers.IntegerField(source="fakultetlar.count", read_only=True)

    class Meta:
        model = Universitet
        fields = [
            "id", "name", "tashkil_yili", "desc", "image",
            "address", "longitude", "latitude", "web_sayt",
            "created_at", "updated_at",
            "fakultetlar_soni",
        ]
        read_only_fields = ["created_at", "updated_at", "fakultetlar_soni"]


# ------- Fakultet -------
class FakultetSerializer(serializers.ModelSerializer):
    universitet_name = serializers.CharField(source="universitet.name", read_only=True)

    class Meta:
        model = Fakultet
        fields = [
            "id", "universitet", "universitet_name",
            "name", "dekan", "telefon", "email",
            "tashkil_yili", "desc",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# ------- UniverYonalish -------
class UniverYonalishSerializer(serializers.ModelSerializer):
    fakultet_name     = serializers.CharField(source="fakultet.name", read_only=True)
    universitet_name  = serializers.CharField(source="fakultet.universitet.name", read_only=True)
    talim_turi_label  = serializers.CharField(source="get_talim_turi_display", read_only=True)

    class Meta:
        model = UniverYonalish
        fields = [
            "id", "fakultet", "fakultet_name", "universitet_name",
            "name", "talim_turi", "talim_turi_label",
            "talim_muddati_y", "kontrakt_summasi", "grant_mavjudmi", "desc",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# ------- XususiyMaktab -------
class XususiyMaktabSerializer(serializers.ModelSerializer):
    class Meta:
        model = XususiyMaktab
        fields = [
            "id", "name", "tashkil_yili", "mudir", "desc",
            "address", "longitude", "latitude", "web_sayt",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# ------- Fan -------
class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


# ------- MaktabYonalish -------
class MaktabYonalishSerializer(serializers.ModelSerializer):
    maktab_name = serializers.CharField(source="maktab.name", read_only=True)
    fanlar_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name", source="fanlar"
    )

    class Meta:
        model = MaktabYonalish
        fields = [
            "id", "maktab", "maktab_name",
            "name", "fanlar", "fanlar_names",
            "talim_muddati_o", "oqish_summasi", "grant_mavjudmi", "desc",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
