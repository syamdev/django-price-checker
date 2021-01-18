from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Coffee


class CoffeeListView(ListView):
    model = Coffee


class CoffeeDetailView(DetailView):
    model = Coffee


class CoffeeCreateView(LoginRequiredMixin, CreateView):
    model = Coffee
    fields = ['name', 'description', 'type', 'country_of_origin']
