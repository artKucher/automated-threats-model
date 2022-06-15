from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('assets-types', views.AssetTypeViewSet)
router.register('assets/ids', views.AssetsIdsViewSet)
router.register('assets', views.AssetsViewSet)
router.register('negative-consequences', views.NegativeConsequencesViewSet)
router.register('systems/classes/ispdn', views.ISPDNClassesViewSet)
router.register('systems/classes/asutp', views.ASUTPClassesViewSet)
router.register('systems/classes/gis', views.GISClassesViewSet)
router.register('systems/classes/kii', views.KIIClassesViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]