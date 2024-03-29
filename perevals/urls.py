from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'pereval', PerevalViewset, basename='pereval')
router.register(r'user', UserViewset, basename='user')
# router.register(r'coords', CoordsViewset)
# router.register(r'level', LevelViewset)
# router.register(r'images', ImagesViewset)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
