from django.contrib.auth.models import AbstractUser
from django.db import models
import json
from django.core.exceptions import ValidationError

class User(AbstractUser):
    def validate_json(value):
        try:
            if isinstance(value, str):
                json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format")

    favorite_artists = models.JSONField(
        default=list,
        validators=[validate_json],
        help_text="Enter artists as JSON array"
    )
    disliked_artists = models.JSONField(
        default=list,
        validators=[validate_json],
        help_text="Enter artists as JSON array"
    )