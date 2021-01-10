from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/v1/', include('exemple.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]