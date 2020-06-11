from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import AddBeerForm
from .models import Beer


class BeerListView(ListView):
    model = Beer
    context_object_name = 'beers'
    template_name = 'beers/home.html'
    # paginate_by = 1



class AddBeerView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Beer
    permission_required = 'beers.can_add_beer'
    template_name = 'beers/add_beer.html'
    form_class = AddBeerForm
    success_url = reverse_lazy(
        'beer-list'
    )