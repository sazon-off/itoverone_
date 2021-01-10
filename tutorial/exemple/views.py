from django.utils import timezone
from rest_framework import viewsets
from .models import Category, Author, Book
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    BookListSerializer,
    BookDetailSerializer,
    CategorySerializer,
    BooksSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.filter(parent=None)
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

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.deleted_by = self.request.user
        instance.deleted_at = timezone.now()
        instance.save()


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.filter(deleted=False)
    serializer_class = AuthorListSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = AuthorListSerializer
        return viewsets.ModelViewSet.list(self, request)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AuthorDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, request)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.deleted_by = self.request.user
        instance.deleted_at = timezone.now()
        instance.save()


class BooksByAuthorViewSet(viewsets.ModelViewSet):

    serializer_class = BooksSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']

        return Book.objects.filter(author_id=pk)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BooksByCategoryViewSet(viewsets.ModelViewSet):

    serializer_class = BooksSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Book.objects.filter(category_id=pk)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AuthorsByCategoryViewSet(viewsets.ModelViewSet):

    serializer_class = AuthorListSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Author.objects.filter(category_id=pk)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)