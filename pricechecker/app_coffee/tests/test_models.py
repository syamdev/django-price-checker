import pytest

from ..models import Coffee
from .factories import CoffeeFactory

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    coffee = CoffeeFactory()
    assert coffee.__str__() == coffee.name
    assert str(coffee) == coffee.name


def test_get_absolute_url():
    coffee = CoffeeFactory()
    url = coffee.get_absolute_url()
    assert url == f'/coffees/{coffee.slug}/'
