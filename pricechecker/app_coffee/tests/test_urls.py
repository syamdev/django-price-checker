import pytest

from django.urls import reverse, resolve

from .factories import CoffeeFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def coffee():
    return CoffeeFactory()


def test_list_reverse():
    """coffee:list should reverse to /coffees/."""
    assert reverse('coffee:list') == '/coffees/'


def test_list_resolve():
    """/coffees/ should resolve to coffee:list."""
    assert resolve('/coffees/').view_name == 'coffee:list'


def test_add_reverse():
    """coffee:add should reverse to /coffees/add/."""
    assert reverse('coffee:add') == '/coffees/add/'


def test_add_resolve():
    """/coffees/add/ should resolve to coffee:add."""
    assert resolve('/coffees/add/').view_name == 'coffee:add'


def test_detail_reverse(coffee):
    """coffee:detail should reverse to /coffees/coffeeslug/."""
    url = reverse('coffee:detail', kwargs={'slug': coffee.slug})
    assert url == f'/coffees/{coffee.slug}/'


def test_detail_resolve(coffee):
    """/coffees/coffeeslug/ should resolve to coffee:detail."""
    url = f'/coffees/{coffee.slug}/'
    assert resolve(url).view_name == 'coffee:detail'
