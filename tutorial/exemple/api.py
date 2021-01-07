from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
)


class AuthorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Author.objects.all()
        serializer = AuthorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Author.objects.all()
        author = get_object_or_404(queryset, pk=pk)
        serializer = AuthorDetailSerializer(author)
        # print(self.retrieve.u)
        return Response(serializer.data)



class Author(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer


class AuthorModelViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorListSerializer
    queryset = Author.objects.all()

    # @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    # def my_list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'put']) #, renderer_classes=[renderers.AdminRenderer])
    def example(self, request, *args, **kwargs):
        author = self.get_object()
        serializer = AuthorDetailSerializer(author)
        print(self.reverse_action('highlight'))
        self.reverse_action("author", args=['1']),
        return Response(serializer.data)
