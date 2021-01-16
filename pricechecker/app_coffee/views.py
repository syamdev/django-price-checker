from django.views.generic import ListView, DetailView
from .models import Coffee


class CoffeeListView(ListView):
    model = Coffee
