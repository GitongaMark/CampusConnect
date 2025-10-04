from django.urls import path
from .views import CategoryListView, ListingListCreateView, ListingDetailUpdateDestroyView

urlpatterns = [
  path('api/marketplace/categories/', CategoryListView.as_view(), name='category-list'),
  path('api/marketplace/listings/', ListingListCreateView.as_view(), name='listing-list-create'),
  path('api/marketplace/listings/<int:pk>/', ListingDetailUpdateDestroyView.as_view(), name='listing-detail-update-destroy'),
]