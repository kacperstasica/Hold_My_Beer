from django.urls import path

from .views import (
    AddBeerView,
    ReviewDeleteView,
    BeerReviewListView,
    ReviewCreateView,
    ReviewUpdateView
)

app_name = 'beers'
urlpatterns = [
    path('add_beer/', AddBeerView.as_view(), name='add-beer'),
    path('detail/<int:pk>/', BeerReviewListView.as_view(), name='beer-detail'),
    path('review/<int:pk>/', ReviewCreateView.as_view(), name='create-review'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

]
