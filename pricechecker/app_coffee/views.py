from django.views.generic import ListView, DetailView, CreateView
from .models import Coffee


class CoffeeListView(ListView):
    model = Coffee


class CoffeeDetailView(DetailView):
    model = Coffee


class CoffeeCreateView(CreateView):
    model = Coffee
    fields = ['name', 'description', 'type', 'country_of_origin']
