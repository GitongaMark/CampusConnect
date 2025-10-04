from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product as Listing, Category
from .serializers import ListingSerializer, CategorySerializer

class IsSellerOrReadOnly(IsAuthenticatedOrReadOnly):
  def has_object_permission(self, request, view, obj):
    if request.method in ['GET', 'HEAD', 'OPTIONS']:
      return True
    
    return obj.seller == request.user

class CategoryListView(generics.ListAPIView):
  queryset = Category.objects.all().order_by('name')
  serializer_class = CategorySerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

class ListingListCreateView(generics.ListCreateAPIView):
  serializer_class = ListingSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_queryset(self):
    queryset = Listing.objects.all().order_by('-created_at')
    category_id = self.request.query_params.get('category')
    search_query = self.request.query_params.get('search')

    if category_id:
      queryset = queryset.filter(category_id=category_id)
      
      if search_query:
        queryset = queryset.filter(
          Q(title__icontains=search_query) |
          Q(description__icontains=search_query)
        )
      
      return queryset
    
    def perform_create(self, serializer):
      serializer.save(seller=self.request.user)

class ListingDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Listing.objects.all()
  serializer_class = ListingSerializer
  permission_classes = [IsSellerOrReadOnly]