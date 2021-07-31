from typing import Dict

from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


def drop_none_fields(d: Dict):
    return {
        k: drop_none_fields(v) if isinstance(v, dict) else v
        for k, v in d.items()
        if v is not None
    }
