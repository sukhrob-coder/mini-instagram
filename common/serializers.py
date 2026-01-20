import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):

        if isinstance(data, str):
            if "data:image" in data and ";base64," in data:
                try:
                    format, imgstr = data.split(";base64,")
                    ext = format.split("/")[-1]

                    if ";" in ext:
                        ext = ext.split(";")[0]

                    decoded_file = base64.b64decode(imgstr)
                    data = ContentFile(decoded_file, name=f"{uuid.uuid4()}.{ext}")
                except (ValueError, TypeError, IndexError):
                    raise serializers.ValidationError("Invalid base64 image format")
            elif data.startswith("http"):
                pass
            elif not data:
                return None

        return super().to_internal_value(data)
