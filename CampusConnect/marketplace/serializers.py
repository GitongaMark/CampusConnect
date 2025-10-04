from rest_framework import serializers
from .models import Category, Product as Listing
from django.contrib.auth.models import User

class SellerSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name']

class ListingSerializer(serializers.ModelSerializer):
  seller_details = SellerSerializer(source='seller', read_only=True)
  category_name = serializers.CharField(source='category.name', read_only=True)

  class Meta:
    model = Listing
    fields = ['id', 'seller_details', 'title', 'description', 'price', 'category', 'category_name', 'created_at']

    read_only_fields = ['seller', 'created_at']