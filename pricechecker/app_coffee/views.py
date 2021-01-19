from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Coffee


class CoffeeListView(ListView):
    model = Coffee


class CoffeeDetailView(DetailView):
    model = Coffee


class CoffeeCreateView(LoginRequiredMixin, CreateView):
    model = Coffee
    fields = ['name', 'description', 'type', 'country_of_origin']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CoffeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Coffee
    fields = ['name', 'description', 'type', 'country_of_origin']
    action = "Update"
