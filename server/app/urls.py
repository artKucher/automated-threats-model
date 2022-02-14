from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('assets', views.AssetViewSet)
router.register('interfaces', views.InterfaceViewSet)

urlpatterns = [
    path('', include(router.urls))
]