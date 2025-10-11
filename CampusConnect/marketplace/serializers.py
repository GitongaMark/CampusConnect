from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Favorite


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    seller_details = SellerSerializer(source="seller", read_only=True)
    category_name = serializers.ReadOnlyField(source="category.name")
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "seller_details",
            "title",
            "description",
            "price",
            "category",
            "category_name",
            "created_at",
            "is_favorite",
        ]
        read_only_fields = ["seller", "created_at", "is_favorite"]

    def get_is_favorite(self, obj):
        """Check if the current user has favorited this product"""
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.favorited_by.filter(user=user).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = Favorite
        fields = [
          "id",
          "user",
          "product",
          "product_details",
          "created_at",
        ]
        read_only_fields = ["user", "created_at"]
