from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICES = (
        (CREATOR, "Créateur"),
        (SUBSCRIBER, "Abonné"),
    )

    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default=CREATOR
    )
    follows = models.ManyToManyField(
        "self",
        limit_choices_to={"role": CREATOR},
        symmetrical=False,
        verbose_name="suit",
    )
