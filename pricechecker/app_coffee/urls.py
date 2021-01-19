from django.urls import path
from . import views


app_name = "app_coffee"
urlpatterns = [
    path(route='', view=views.CoffeeListView.as_view(), name='list'),
    path(route='add/', view=views.CoffeeCreateView.as_view(), name='add'),
    path(route='<slug:slug>/', view=views.CoffeeDetailView.as_view(), name='detail'),
    path(route='<slug:slug>/update/', view=views.CoffeeUpdateView.as_view(), name='update'),
    path(route='<slug:slug>/delete/', view=views.CoffeeDeleteView.as_view(), name='delete'),
]
