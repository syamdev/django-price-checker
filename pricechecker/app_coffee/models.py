from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel


class Coffee(TimeStampedModel):
    UNIQUE_COFFEE = 'UC'
    BLACK_COFFEE = 'BC'
    MILK_BASED_COFFEE = 'MC'
    ICED_COFFEE = 'IC'
    COFFEE_TYPE_CHOICES = [
        (UNIQUE_COFFEE, 'Unique Coffee'),
        (BLACK_COFFEE, 'Black Coffee'),
        (MILK_BASED_COFFEE, 'Milk Based Coffee'),
        (ICED_COFFEE, 'Iced Coffee'),
    ]
    name = models.CharField("Name of Coffee Drink", max_length=255)
    slug = AutoSlugField("Coffee Drink", unique=True, always_update=False, populate_from="name")
    description = models.TextField("Description", blank=True)
    type = models.CharField("Coffee Type", max_length=2, choices=COFFEE_TYPE_CHOICES, default=UNIQUE_COFFEE)

    def __str__(self):
        return self.name
