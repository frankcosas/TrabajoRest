from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import LoginTokenView, PlatoViewSet

router = DefaultRouter()
router.register('platos', PlatoViewSet, basename='api-plato')

urlpatterns = [
    path('token/', LoginTokenView.as_view(), name='api-token'),
    path('', include(router.urls)),
]
