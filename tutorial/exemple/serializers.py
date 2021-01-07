from rest_framework import serializers
from .models import Book, Author, Category
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import (CharField)
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        category, created = Category.objects.update_or_create(
            name=validated_data.get('name', None),
            defaults={'name': validated_data.get('name', None)})
        return category

    class Meta:
        model = Category
        fields = ('id', 'name')


class AuthorListSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    category = CategorySerializer(write_only=True)
    class Meta:
        model = Author
        exclude = ("deleted", "who", "delete_date")
        extra_kwargs = {

            'citizenship': {'write_only': True},
            'dob': {'write_only': True},
            'dod': {'write_only': True},
            'bpl': {'write_only': True},
            'bio': {'write_only': True},
            'category': {'write_only': True},
        }


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ("deleted", "delete_date")


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ("deleted", "who", "delete_date")
        extra_kwargs = {

            'pub_date': {'write_only': True},
            'description': {'write_only': True},
        }


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ("deleted", "who", "delete_date")
