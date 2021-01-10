from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exemple import views

from .views import AuthorViewSet, BookViewSet, CategoryViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('authors/<int:pk>/books/', views.BooksByAuthorViewSet.as_view({'get': 'list'})),
    path('category/<int:pk>/books/', views.BooksByCategoryViewSet.as_view({'get': 'list'})),
    path('category/<int:pk>/authors/', views.AuthorsByCategoryViewSet.as_view({'get': 'list'})),

]