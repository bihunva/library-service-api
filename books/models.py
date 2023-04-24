from enum import Enum

from django.db import models


class CoverType(Enum):
    HARD = "hard"
    SOFT = "soft"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(choices=[(tag, tag.value) for tag in CoverType], max_length=4)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"