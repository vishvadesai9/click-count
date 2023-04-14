from django.contrib.postgres import fields
from rest_framework import serializers
from .models import ClickCount

class ClickCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickCount
        fields = (
            "id",
            "city",
            "country",
            "count",
            "created_at",
            "updated_at"
        )