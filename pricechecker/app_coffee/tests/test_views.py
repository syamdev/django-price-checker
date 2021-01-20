import pytest
from django.http import HttpResponseRedirect
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse, resolve
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, Client

from ...users.models import User
from ..models import Coffee
from ..views import CoffeeCreateView, CoffeeListView, CoffeeDetailView, CoffeeUpdateView, CoffeeDeleteView
from .factories import CoffeeFactory, coffee

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


def test_good_coffee_detail_view(rf, coffee):
    # Make a request for our new coffee
    url = reverse("coffee:detail", kwargs={'slug': coffee.slug})
    request = rf.get(url)

    # Use the request to get the response
    callable_obj = CoffeeDetailView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Test that the response is valid
    assertContains(response, coffee.name)


def test_good_coffee_create_view(rf, admin_user):
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


def test_detail_contains_coffee_data(rf, coffee):
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


def test_coffee_create_correct_title(rf, admin_user):
    """Page title for CoffeeCreateView should be Add Coffee."""
    request = rf.get(reverse('coffee:add'))
    request.user = admin_user
    response = CoffeeCreateView.as_view()(request)
    assertContains(response, 'Add Coffee')


def test_good_coffee_update_view(rf, admin_user, coffee):
    url = reverse("coffee:update", kwargs={'slug': coffee.slug})

    # Make a request for our new coffee
    request = rf.get(url)

    # Add an authenticated user
    request.user = admin_user

    # Use the request to get the response
    callable_obj = CoffeeUpdateView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Test that the response is valid
    assertContains(response, "Update Coffee")


def test_coffee_update(rf, admin_user, coffee):
    """POST request to CoffeeUpdateView updates a coffee and redirects."""
    # Make a request for our new coffee
    form_data = {
        'name': coffee.name,
        'description': 'Something new',
        'type': coffee.BLACK_COFFEE
    }
    url = reverse("coffee:update", kwargs={'slug': coffee.slug})
    request = rf.post(url, form_data)
    request.user = admin_user
    callable_obj = CoffeeUpdateView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Check that the coffee has been changed
    coffee.refresh_from_db()
    assert coffee.description == 'Something new'


def test_good_coffee_delete_view(rf, admin_user, coffee):
    url = reverse("coffee:delete", kwargs={'slug': coffee.slug})

    # Make a request for our new coffee
    request = rf.get(url)

    # Add an authenticated user
    request.user = admin_user

    # Use the request to get the response
    callable_obj = CoffeeDeleteView.as_view()
    response = callable_obj(request, slug=coffee.slug)

    # Go to success url page after delete
    expected_url = reverse("coffee:list")

    # Test that the response is valid
    assert response.status_code == 302
    assert response.url == expected_url


def test_coffee_delete(rf, admin_user, coffee):
    """POST request to CoffeeDeleteView delete a coffee and redirects."""
    # Submit the coffee add form
    request = rf.get(reverse("coffee:add"))
    request.user = admin_user
    response_create = CoffeeCreateView.as_view()(request)

    url = reverse("coffee:delete", kwargs={'slug': coffee.slug})
    request = rf.delete(url)
    request.user = admin_user
    callable_obj = CoffeeDeleteView.as_view()
    response_delete = callable_obj(request, slug=coffee.slug)

    # Check that the coffee has been deleted
    assert list(Coffee.objects.all()) == list(Coffee.objects.none())
    assert Coffee.objects.count() == 0

# def test_good_coffee_delete_view(rf, admin_user, coffee):
#     url = reverse("coffee:delete", kwargs={'slug': coffee.slug})
#
#     # Make a request for our new coffee
#     request = rf.get(url)
#
#     # Add an authenticated user
#     request.user = admin_user
#
#     # Use the request to get the response
#     callable_obj = CoffeeDeleteView.as_view()
#     response = callable_obj(request, slug=coffee.slug)
#
#     # Test that the response is valid
#     assertContains(response, "Confirm")


# def test_coffee_delete(rf, admin_user, coffee):
#     """POST request to CoffeeDeleteView delete a coffee and redirects."""
#     # Submit the coffee add form
#     request = rf.get(reverse("coffee:add"))
#     request.user = admin_user
#     response = CoffeeCreateView.as_view()(request)
#
#     url = reverse("coffee:delete", kwargs={'slug': coffee.slug})
#     request = rf.delete(url)
#     request.user = admin_user
#     callable_obj = CoffeeDeleteView.as_view()
#     response = callable_obj(request, slug=coffee.slug)
#
#     # Go to success url page after delete
#     expected_url = reverse("coffee:list")
#     response.client = Client()
#
#     response.client.delete(url)
#
#     url = '/coffees/'
#     # resp = response.client.get(expected_url)
#
#     # Check that the coffee has been deleted
#     assert response.status_code == 302
#     assert response.url == expected_url
#     assert list(Coffee.objects.all()) == list(Coffee.objects.none())
#     assert resolve(url).view_name == 'coffee:list'
#     # assert resp.status_code == 200
#     assert Coffee.objects.count() == 0
