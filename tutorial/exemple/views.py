from django.db import models
from rest_framework import viewsets
from .models import Category, Author, Book
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    BookListSerializer,
    BookDetailSerializer,
    CategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.filter(deleted=False)
    serializer_class = BookListSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = BookListSerializer
        return viewsets.ModelViewSet.list(self, request)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = BookDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, request)


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.filter(deleted=False)
    serializer_class = AuthorListSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = AuthorListSerializer
        return viewsets.ModelViewSet.list(self, request)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AuthorDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, request)
