from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Favorite
from .serializers import ProductSerializer, CategorySerializer, FavoriteSerializer


class IsSellerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.seller == request.user


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")
        category_id = self.request.query_params.get("category")
        search = self.request.query_params.get("search")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if search:
            queryset = queryset.filter(
              Q(title__icontains=search) |
              Q(description__icontains=search))

        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]


class FavoriteListView(generics.ListAPIView):
    """List all favorite products of the logged-in user"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("product", "product__seller")


class ToggleFavoriteView(APIView):
    """Add or remove a product from user's favorites"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)

        serializer = FavoriteSerializer(favorite, context={"request": request})
        return Response({"message": "Added to favorites", "data": serializer.data}, status=status.HTTP_201_CREATED)
