import pytest

from ..models import Coffee
from .factories import CoffeeFactory

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    coffee = CoffeeFactory()
    assert coffee.__str__() == coffee.name
    assert str(coffee) == coffee.name
