from django.template.defaultfilters import slugify

import factory
import factory.fuzzy
import pytest

from ..models import Coffee
from ...users.tests.factories import UserFactory


@pytest.fixture
def coffee():
    return CoffeeFactory()


class CoffeeFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=False)
    type = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Coffee.COFFEE_TYPE_CHOICES]
    )
    country_of_origin = factory.Faker('country_code')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Coffee
