import pytest

from ..models import Coffee

# Connects our tests with our database
pytestmark = pytest.mark.django_db


def test___str__():
    coffee = Coffee.objects.create(
        name='Instant Coffee',
        description='Instant coffee is a drink derived from brewed coffee beans. Through various manufacturing '
                    'processes the coffee is dehydrated into the form of powder or granules. These can be rehydrated '
                    'with hot water to provide a drink similar (though not identical) to conventional coffee.',
        type=Coffee.UNIQUE_COFFEE
    )

    assert coffee.__str__() == "Instant Coffee"
    assert str(coffee) == "Instant Coffee"
