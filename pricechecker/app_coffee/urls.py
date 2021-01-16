from django.urls import path
from . import views


app_name = "app_coffee"
urlpatterns = [
    path(route='', view=views.CoffeeListView.as_view(), name='list'),
    path(route='<slug:slug>/', view=views.CoffeeDetailView.as_view(), name='detail'),
]
