from django.urls import path, include

from apps.resource.views import InfluxStorage, router

urlpatterns = [
    path("", include(router.urls)),
    path('influx/', InfluxStorage.as_view(), name='influx'),
]
