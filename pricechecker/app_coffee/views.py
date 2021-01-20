from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    action = 'Update'


class CoffeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Coffee
    fields = ['name', 'description', 'type', 'country_of_origin']
    action = 'Delete'
    success_url = reverse_lazy('coffee:list')

    def get(self, request, *args, **kwargs):
        # Delete immediately without confirmation
        return super(CoffeeDeleteView, self).post(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.success_url
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(CoffeeDeleteView, self).post(request, *args, **kwargs)
