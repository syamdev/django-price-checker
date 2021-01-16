from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from ..models import Coffee


class CoffeeFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=False)
    type = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Coffee.COFFEE_TYPE_CHOICES]
    )

    class Meta:
        model = Coffee
