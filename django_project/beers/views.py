from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from .forms import AddBeerForm, ReviewForm
from .models import Beer, Review


class BeerListView(ListView):
    model = Beer
    context_object_name = 'beers'
    template_name = 'beers/home.html'


class AddBeerView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Beer
    permission_required = 'beers.can_add_beer'
    template_name = 'beers/add_beer.html'
    form_class = AddBeerForm
    success_url = reverse_lazy(
        'beer-list'
    )


class BeerDetailView(LoginRequiredMixin, DetailView):
    model = Beer
    template_name = 'beers/beer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        average_rating = Review.count_rating(beer_id=self.kwargs.get('pk'))
        if average_rating is not None:
            context['average_rating'] = round(average_rating, 2)
            context['rating_as_int'] = int(average_rating)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'beers/review_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.beer = Beer.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('beers:beer-detail', kwargs={'pk': self.kwargs['pk']})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['content', 'rating']

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        beer = self.object.beer
        return reverse('beers:beer-detail', kwargs={'pk': beer.id})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    def get_success_url(self):
        beer = self.object.beer
        return reverse('beers:beer-detail', kwargs={'pk': beer.id})
