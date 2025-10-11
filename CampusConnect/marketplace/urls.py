from django.urls import path
from .views import (
    CategoryListView,
    ProductListCreateView,
    ProductDetailUpdateDestroyView,
    FavoriteListView,
    ToggleFavoriteView,
)

urlpatterns = [
    path(
      "api/marketplace/categories/", CategoryListView.as_view(), name="category-list",
    ),

    path(
      "api/marketplace/products/", ProductListCreateView.as_view(), name="product-list-create",
    ),

    path(
      "api/marketplace/products/<int:pk>/", ProductDetailUpdateDestroyView.as_view(), name="product-detail-update-destroy",
    ),

    path(
      "api/marketplace/favorites/",
      FavoriteListView.as_view(), name="favorite-list",
    ),

    path(
      "api/marketplace/products/<int:pk>/favorite/", ToggleFavoriteView.as_view(), name="toggle-favorite",
    ),
]
