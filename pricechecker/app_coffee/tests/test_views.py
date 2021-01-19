import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from ...users.models import User
from ..models import Coffee
from ..views import CoffeeCreateView, CoffeeListView, CoffeeDetailView
from .factories import CoffeeFactory

pytestmark = pytest.mark.django_db


# def test_good_coffee_list_view_expanded(rf):
#     # Determine the URL
#     url = reverse("coffee:list")
#     # rf is pytest shortcut to django.test.RequestFactory
#     # We generate a request as if from a user accessing the coffee list view
#     request = rf.get(url)
#     # Call as_view() to make a callable object
#     # callable_obj is analogous to a function-based view
#     callable_obj = CoffeeListView.as_view()
#     # Pass in the request into the callable_obj to get an HTTP response served up by Django
#     response = callable_obj(request)
#     # Test that the HTTP response has 'Coffee List' in the HTML and has a 200 response code
#     assertContains(response, 'Coffee List')


def test_good_coffee_list_view(rf):
    # Get the request
    request = rf.get(reverse("coffee:list"))
    # Use the request to get the response
    response = CoffeeListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Coffee List')


def test_good_coffee_detail_view(rf):
    # Order some coffee from the CoffeeFactory
    coffee = CoffeeFactory()

    # Make a request for our new coffee
    url = reverse("coffee:detail", kwargs={'slug': coffee.slug})
    request = rf.get(url)

    # Use the request to get the response
    callable_obj = CoffeeDetailView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Test that the response is valid
    assertContains(response, coffee.name)


def test_good_coffee_create_view(rf, admin_user):
    # Order some coffee from the CoffeeFactory
    coffee = CoffeeFactory()

    # Make a request for our new coffee
    request = rf.get(reverse("coffee:add"))

    # Add an authenticated user
    request.user = admin_user

    # Use the request to get the response
    response = CoffeeCreateView.as_view()(request)

    # Test that the response is valid
    assert response.status_code == 200


def test_coffee_list_contains_2_coffees(rf):
    # Let's create a couple coffees
    coffee1 = CoffeeFactory()
    coffee2 = CoffeeFactory()

    # Create a request and then a response for a list of coffee
    request = rf.get(reverse('coffee:list'))
    response = CoffeeListView.as_view()(request)

    # Assert that the response contains both coffee names in the template.
    assertContains(response, coffee1.name)
    assertContains(response, coffee2.name)


def test_detail_contains_coffee_data(rf):
    coffee = CoffeeFactory()

    # Make a request for our new coffee
    url = reverse("coffee:detail", kwargs={'slug': coffee.slug})
    request = rf.get(url)

    # Use the request to get the response
    callable_obj = CoffeeDetailView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Test the Coffee details
    assertContains(response, coffee.name)
    assertContains(response, coffee.get_type_display())
    assertContains(response, coffee.country_of_origin.name)


def test_coffee_create_form_valid(rf, admin_user):
    # Submit the coffee add form
    form_data = {
        "name": "Ristretto",
        "description": "It is an espresso shot with half the amount of water.",
        "type": Coffee.BLACK_COFFEE
    }
    request = rf.post(reverse("coffee:add"), form_data)
    request.user = admin_user
    response = CoffeeCreateView.as_view()(request)

    # Get the coffee based on the name
    coffee = Coffee.objects.get(name="Ristretto")

    # Test that the coffee matches our form
    assert coffee.description == "It is an espresso shot with half the amount of water."
    assert coffee.type == Coffee.BLACK_COFFEE
    assert coffee.author == admin_user
